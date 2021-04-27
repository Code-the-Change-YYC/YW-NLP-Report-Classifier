from enum import Enum

from datetime import timezone, datetime
from dateutil.relativedelta import relativedelta
import server.schemas.submit as submit_schema
from typing import List, Tuple
import yagmail

from server.schemas.submit import Form

import server.risk_scores.risk_scores as risk_scores
from server.connection import collection
from server.credentials import credentials

yag = yagmail.SMTP(credentials.gmail_username, credentials.gmail_password)
email_format = ("""
    <h2>A high risk assessment was determined in a critical incident report recently filled out</h2>
    Contents of report form:
    {form_values}
    """)
MAX_PREVIOUS_INCIDENTS = 3


class RiskAssessment(Enum):
    UNDEFINED = 'UNDEFINED'
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'


AssessmentRange = Tuple[float, RiskAssessment]
"""
The first value indicates the maximum percentage (inclusive) of the maximum
possible risk score for which a risk score could be classified as the second
value.
"""
assessment_ranges: List[AssessmentRange] = [(1 / 3, RiskAssessment.LOW),
                                            (1 / 3 * 2, RiskAssessment.MEDIUM),
                                            (1, RiskAssessment.HIGH)]
assessment_ranges.sort(key=lambda range: range[0])


def get_incident_similarity(prev_incident: submit_schema.Form, current_incident: submit_schema.Form):
    """
    Returns a value between min_value and 1 depending on the previous incident type's similarity to the current incident type.
    """
    min_value = 0.2
    similarity = min_value

    similar_fields = {
        'client_secondary': 1,
        'location': 1,
        'incident_type_primary': 2,
        'incident_type_secondary': 1,
        'child_involved': 1,
        'program': 1,
    }

    total_field_sum = sum(similar_fields.values())

    for field, score in similar_fields.items():
        if getattr(current_incident, field) == getattr(prev_incident, field):
            similarity += score / total_field_sum

    return similarity


def get_incident_recency(prev_incident: submit_schema.Form, current_incident: submit_schema.Form, timeframe: int):
    """
    Returns a value between min_value and 1 depending on the previous incident type's recency scaled by the timeframe.
    """
    min_value = 0.3
    # TODO: Standardize all dates in the databse
    prev_incident.occurrence_time = prev_incident.occurrence_time.replace(
        tzinfo=timezone.utc)
    delta = (current_incident.occurrence_time -
             prev_incident.occurrence_time).days/30
    incident_recency = 1 - (1 - min_value) * (delta/timeframe)
    # avoid potential off-by-one month errors by dividing by 30
    return max(min_value, incident_recency)


def previous_risk_score_func(incident_score: float, incident_recency: float, incident_similarity: float) -> float:
    return incident_score * incident_recency * incident_similarity


def get_previous_incident_risk_score(curr_incident: submit_schema.Form, prev_incident: submit_schema.Form, timeframe: int):
    incident_score = get_current_risk_score(prev_incident)
    incident_similarity = get_incident_similarity(prev_incident, curr_incident)
    incident_recency = get_incident_recency(
        prev_incident, curr_incident, timeframe)

    return previous_risk_score_func(incident_score, incident_recency, incident_similarity)


def normalize_previous_risk_score(total_prev_risk_score: float):
    """
    Normalizes the total_prev_risk_score by the maximum potential risk score of incidents, returning a value between 0 and 1.
    Params:
        total_prev_risk_score: Risk score based on a past Critical Incident Report.
    """
    # Submitting the same form twice guarantees maximum similarity and recency
    same_form = submit_schema.Form(description='', client_primary='', client_secondary='', location='', services_involved=[], occurrence_time=datetime.utcfromtimestamp(
        0), incident_type_primary='incident-type', incident_type_secondary='incident-type', child_involved=False, program='program', immediate_response=[], staff_name='staff', program_supervisor_reviewer_name='reviewer')
    incident_similarity = get_incident_similarity(same_form, same_form)
    incident_recency = get_incident_recency(
        same_form, same_form, timeframe=1)
    max_prev_risk_score = previous_risk_score_func(
        risk_scores.max_risk_score, incident_recency, incident_similarity)

    max_total_prev_risk_score = max_prev_risk_score * MAX_PREVIOUS_INCIDENTS
    return total_prev_risk_score / max_total_prev_risk_score


def normalize_current_risk_score(risk_score: float):
    """
    Normalizes the risk_score by the maximum potential incident risk score, returning a value between 0 and 1.
    Params:
        risk_score: Risk score based on the Critical Incident Report.
    """
    return risk_score / risk_scores.max_risk_score


def get_previous_risk_score(form: submit_schema.Form, timeframe: int):
    """
    Returns a risk score number between 0 and 1 based on the last MAX_PREVIOUS_INCIDENTS by that client
    with the same primary initials in the database.

    Params:
        form: Data submitted in through the endpoint.
        timeframe: Number of months to search over, i.e., months before previous incidents become irrelevant.
    """
    query = {
        "client_primary": form.client_primary,
        "occurrence_time": {
            "$gte": (form.occurrence_time - relativedelta(months=timeframe)).strftime("%Y-%m-%d %H:%M:%S")
        }
    }
    sort_order = {"occurrence_time": 1}
    prev_incidents = list(collection.find(query).sort(
        sort_order))[-MAX_PREVIOUS_INCIDENTS:]
    total_prev_risk_score = 0
    for incident_dict in prev_incidents:
        incident_dict = {key: (val.lower() if type(val) == str else val)
                         for key, val in incident_dict.items()}

        incident = Form(**incident_dict)
        total_prev_risk_score += get_previous_incident_risk_score(
            form, incident, 1)

    return normalize_previous_risk_score(total_prev_risk_score)


def get_current_risk_score(form: submit_schema.Form):
    risk_score = (risk_scores.program_to_risk_map.get_risk_score(form.program) +
                  risk_scores.incident_type_to_risk_map.get_risk_score(
                      form.incident_type_primary) +
                  risk_scores.response_to_risk_map.get_risk_score(
                      form.immediate_response) +
                  risk_scores.occurrence_time_to_risk_map.get_risk_score(
                      form.occurrence_time))

    return normalize_current_risk_score(risk_score)


def get_risk_assessment(form: submit_schema.Form, timeframe: int) -> RiskAssessment:
    total_risk_score = get_current_risk_score(form)
    + get_previous_risk_score(form, timeframe)

    for max_percent, assessment in assessment_ranges:
        if total_risk_score <= max_percent:
            if assessment == RiskAssessment.HIGH and credentials.PYTHON_ENV != "development":
                email_high_risk_alert(form.dict())    # TODO: make async
            return assessment
    else:
        return RiskAssessment.UNDEFINED


def email_high_risk_alert(form_values: dict):
    form_values = (
        f"<b>{field}</b>: {value}" for field, value in form_values.items())
    yag.send(credentials.gmail_username,
             subject="Recent high risk assessment",
             contents=email_format.format(form_values="\n".join(form_values)))
