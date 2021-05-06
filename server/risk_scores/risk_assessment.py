from enum import Enum

from datetime import timezone, datetime
from dateutil.relativedelta import relativedelta
import server.schemas.submit as submit_schema
from typing import List, Tuple
import yagmail

from server.schemas.submit import Form

import server.risk_scores.risk_scores as risk_scores
from server.risk_scores.risk_scores import MAX_PREVIOUS_INCIDENTS, risk_score_combiner
from server.connection import collection
from server.credentials import credentials
from server.sanity_utils import run_query, headers, minimum_email_score_query

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


assessment_ranges: List[RiskAssessment] = [RiskAssessment.LOW,
                                           RiskAssessment.MEDIUM,
                                           RiskAssessment.HIGH]


minimum_email_score = run_query(
    credentials.sanity_gql_endpoint,
    minimum_email_score_query,
    headers)['data']['CirForm']['minimumEmailRiskScore'].upper()

minimum_email_score_index = 0

for i, assessment in enumerate(assessment_ranges):
    if assessment == RiskAssessment[minimum_email_score]:
        minimum_email_score_index = i


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
    min_value = 0.4
    prev_incident.occurrence_time = prev_incident.occurrence_time.replace(
        tzinfo=timezone.utc)
    delta = (current_incident.occurrence_time -
             prev_incident.occurrence_time).days/30
    # Calculate recency scaled by min_value. If delta == timeframe, incident_recency = min_value.
    # If delta ~= 0 (the previous incident occurred recently), incident_recency ~= 1.
    scale = 1 - min_value
    incident_recency = 1 - scale * (delta/timeframe)
    # Avoid potential off-by-one month errors by dividing by 30
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
    Normalizes the total_prev_risk_score by the maximum potential risk score of an incident, returning a value between 0 and 1.
    Params:
        total_prev_risk_score: Risk score based on a past Critical Incident Report.
    """
    # Submitting the same form twice guarantees maximum similarity and recency
    same_form = submit_schema.Form(description='', client_primary='', client_secondary='', location='', services_involved=[], occurrence_time=datetime.utcfromtimestamp(
        0), incident_type_primary='incident-type', incident_type_secondary='incident-type', child_involved=False, non_client_involved=False, program='program', immediate_response=[], staff_name='staff', program_supervisor_reviewer_name='reviewer', completion_date=datetime.utcfromtimestamp(0))
    incident_similarity = get_incident_similarity(same_form, same_form)
    incident_recency = get_incident_recency(
        same_form, same_form, timeframe=1)
    max_prev_risk_score = previous_risk_score_func(
        risk_scores.max_risk_score, incident_recency, incident_similarity)

    max_total_prev_risk_score = max_prev_risk_score
    return total_prev_risk_score / max_total_prev_risk_score


def normalize_current_risk_score(risk_score: float):
    """
    Normalizes the risk_score by the maximum potential incident risk score, returning a value between 0 and 1.
    Params:
        risk_score: Risk score based on the Critical Incident Report.
    """
    return risk_score / risk_scores.max_risk_score


def calculate_previous_risk_score_weightings() -> List[float]:
    """
    Creates a risk score weighting distribution of size MAX_PREVIOUS_INCIDENTS such that the distribution
    is a decreasing linear series that sums to 1. For example, with MAX_PREVIOUS_INCIDENTS == 3,
    this function returns [0.5, 0.333..., 0.166...], or [3/6, 2/6. 1/6].

    This is designed to put more weighting on the first most recent incident types, as well
    as lessen the difference between the number of incident types a client has.
    """
    mpi = MAX_PREVIOUS_INCIDENTS
    # arithmetic sum formula
    denominator = mpi * (mpi+1) / 2

    return [(mpi-i)/denominator for i in range(mpi)]


def get_previous_incidents_risk_score(form: submit_schema.Form, timeframe: int):
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
    sort_order = [("occurrence_time", 1)]
    prev_incidents = list(collection.find(query).sort(
        sort_order))[-MAX_PREVIOUS_INCIDENTS:]

    previous_risk_score_weightings = calculate_previous_risk_score_weightings()

    total_prev_risk_score = 0
    for i, incident_dict in enumerate(prev_incidents):
        incident_dict = {key: (val.lower() if type(val) == str else val)
                         for key, val in incident_dict.items()}
        incident = Form(**incident_dict)
        total_prev_risk_score += normalize_previous_risk_score(get_previous_incident_risk_score(
            form, incident, 1)) * previous_risk_score_weightings[i]

    return total_prev_risk_score


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
    score_from_current_incident = get_current_risk_score(form)
    score_from_prev_incidents = get_previous_incidents_risk_score(
        form, timeframe)
    risk_assessment = risk_score_combiner.combine_risk_scores(
        score_from_current_incident, score_from_prev_incidents)

    if risk_assessment >= minimum_email_score_index and credentials.PYTHON_ENV != "development":
        email_high_risk_alert(form.dict())  # TODO: make async
    return assessment_ranges[risk_assessment]


def email_high_risk_alert(form_values: dict):
    form_values = (
        f"<b>{field}</b>: {value}" for field, value in form_values.items())
    yag.send(credentials.gmail_username,
             subject="Recent high risk assessment",
             contents=email_format.format(form_values="\n".join(form_values)))
