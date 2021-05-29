from enum import Enum

from datetime import timezone, datetime
from dateutil.relativedelta import relativedelta
from os.path import dirname
import server.schemas.submit as submit_schema
from typing import List, Tuple
import yagmail
import htmlmin

from server.schemas.submit import Form

import server.risk_scores.risk_scores as risk_scores
from server.risk_scores.risk_scores import MAX_PREVIOUS_INCIDENTS, risk_score_combiner
from server.connection import collection
from server.credentials import credentials
from server.sanity_utils import run_query, headers, minimum_email_score_query
yag = yagmail.SMTP(credentials.gmail_username, credentials.gmail_password)


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
    scale = 1 - min_value

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
            similarity += score / total_field_sum * scale

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
    NOTE: in the case where more than risk_scores.MAX_RESPONSES_FOR_RISK_SCORE responses are included in the CIR, then there's
    a case where the normalized score may be >1. We accept this case and check for it when classifying the final risk level of
    the CIR.
    Params:
        total_prev_risk_score: Risk score based on a past Critical Incident Report.
    """
    # Submitting the same form twice guarantees maximum similarity and recency
    same_form = submit_schema.Form(description='', client_primary='', client_secondary='', location='', services_involved=[], occurrence_time=datetime.utcfromtimestamp(
        0), incident_type_primary='incident-type', incident_type_secondary='incident-type', child_involved=False, non_client_involved=False, program='program', immediate_response=[], staff_name='staff', program_supervisor_reviewer_name='reviewer', completion_date=datetime.utcfromtimestamp(0))
    incident_similarity = get_incident_similarity(same_form, same_form)
    incident_recency = get_incident_recency(
        same_form, same_form, timeframe=1)
    max_total_prev_risk_score = previous_risk_score_func(
        risk_scores.max_risk_score, incident_recency, incident_similarity)

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
            "$gte": form.occurrence_time - relativedelta(months=timeframe)
        }
    }
    sort_order = [("occurrence_time", -1)]
    prev_incidents = list(collection.find(query).sort(
        sort_order))[:MAX_PREVIOUS_INCIDENTS]

    previous_risk_score_weightings = calculate_previous_risk_score_weightings()

    total_prev_risk_score = 0
    for i, incident_dict in enumerate(prev_incidents):
        incident_dict = {key: (val.lower() if type(val) == str else val)
                         for key, val in incident_dict.items()}
        incident = Form(**incident_dict)
        total_prev_risk_score += normalize_previous_risk_score(get_previous_incident_risk_score(
            form, incident, timeframe)) * previous_risk_score_weightings[i]

    return total_prev_risk_score


def get_current_risk_score(form: submit_schema.Form):
    risk_score = (risk_scores.program_to_risk_map.get_risk_score(form.program) +
                  risk_scores.incident_type_to_risk_map.get_risk_score(
                      form.incident_type_primary) +
                  risk_scores.response_to_risk_map.get_risk_score(
                      form.immediate_response) +
                  risk_scores.services_to_risk_map.get_risk_score(
                      form.services_involved) +
                  risk_scores.occurrence_time_to_risk_map.get_risk_score(
                      form.occurrence_time))

    return normalize_current_risk_score(risk_score)


def get_risk_assessment(form: submit_schema.Form, timeframe: int) -> RiskAssessment:
    score_from_current_incident = get_current_risk_score(form)
    score_from_prev_incidents = get_previous_incidents_risk_score(
        form, timeframe)
    risk_assessment = risk_score_combiner.combine_risk_scores(
        score_from_current_incident, score_from_prev_incidents)
    print(
        f"Risk score from current incident: {score_from_current_incident:.3f}")
    print(
        f"Risk score from previous incidents: {score_from_prev_incidents:.3f}")

    form_dict = form.dict()

    if risk_assessment >= minimum_email_score_index and credentials.PYTHON_ENV != "development":
        risk_assessment_str = assessment_ranges[risk_assessment.value]
        print(
            f"Form assessed to be {risk_assessment_str} risk. Sending email.")
        email_dict = {
            "staff_name": form_dict["staff_name"],
            "client_primary": form_dict["client_primary"],
            "risk_assessment": risk_assessment_str,
            "score_from_prev_incidents": score_from_prev_incidents,
            "score_from_current_incident": score_from_current_incident,
            "time_of_incident": form_dict["occurrence_time"].ctime(),
            "time_of_report_completion": form_dict["completion_date"].ctime()
        }
        email_high_risk_alert(email_dict)

    return assessment_ranges[risk_assessment]


html_template_filename = "/template.html"

with open(dirname(__file__) + html_template_filename) as f:
    html_template = f.read()

email_recipients = tuple(credentials.email_recipients)


def email_high_risk_alert(email_values: dict):
    email_contents = htmlmin.minify(html_template.format(**email_values))
    yag.send(to=email_recipients,
             subject="CIR Risk Assessment",
             contents=email_contents)
