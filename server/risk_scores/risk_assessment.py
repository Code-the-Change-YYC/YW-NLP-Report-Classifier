from enum import Enum

from datetime import timezone
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
    similarity = 0
    coefficient = 1

    similar_fields = {
        'client_secondary': 1,
        'location': 1,
        'incident_type_primary': 2,
        'incident_type_secondary': 1,
        'child_involved': 1,
        'program': 1,
    }

    for field, score in similar_fields.items():
        if getattr(current_incident, field) == getattr(prev_incident, field):
            similarity += score

    return coefficient * similarity


def get_incident_recency(prev_incident: submit_schema.Form, current_incident: submit_schema.Form, timeframe):
    # TODO: Standardize all dates in the databse
    prev_incident.occurrence_time = prev_incident.occurrence_time.replace(
        tzinfo=timezone.utc)
    delta = (current_incident.occurrence_time -
             prev_incident.occurrence_time).days/30
    recency_of_incident = 1 - delta/timeframe
    return recency_of_incident


def get_previous_risk_score(form: submit_schema.Form, timeframe):
    query = {
        "client_primary": form.client_primary,
        "occurrence_time": {
            '$gte': (form.occurrence_time - relativedelta(months=timeframe)).strftime("%Y-%m-%d %H:%M:%S")
        }
    }
    prev_incidents = collection.find(query)
    total_prev_risk_score = 0
    for incident_dict in prev_incidents:
        incident_dict = {key: (val.lower() if type(val) == str else val)
                         for key, val in incident_dict.items()}

        incident = Form(**incident_dict)
        incident_score = get_current_risk_score(incident)
        incident_similarity = get_incident_similarity(incident, form)
        incident_recency = get_incident_recency(incident, form, timeframe)

        total_prev_risk_score += incident_score + \
            incident_recency * incident_similarity

    return total_prev_risk_score


def get_current_risk_score(form: submit_schema.Form):
    risk_score = (risk_scores.program_to_risk_map.get_risk_score(form.program) +
                  risk_scores.incident_type_to_risk_map.get_risk_score(
                      form.incident_type_primary) +
                  risk_scores.response_to_risk_map.get_risk_score(
                      form.immediate_response) +
                  risk_scores.occurrence_time_to_risk_map.get_risk_score(
                      form.occurrence_time))

    max_risk_score = (
        risk_scores.program_to_risk_map.max_risk_score() +
        risk_scores.incident_type_to_risk_map.max_risk_score() +
        risk_scores.response_to_risk_map.max_risk_score_with_value_count(
            len(form.immediate_response)) +
        risk_scores.occurrence_time_to_risk_map.max_risk_score())

    percent_of_max = risk_score / max_risk_score
    return percent_of_max


def get_risk_assessment(form: submit_schema.Form, timeframe) -> RiskAssessment:
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
