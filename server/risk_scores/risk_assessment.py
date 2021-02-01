from enum import Enum

from datetime import datetime
from dateutil.relativedelta import relativedelta
import server.schemas.submit as submit_schema
from typing import List, Tuple
import yagmail

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


def query_mongo(initials: str, timeframe: int = 12):
    """
    
    Parameters:
        timeframe: Months from the current date to look backward in time.
    """
    query = {
        'client_primary': initials,
        "occurence_time": {
            "$gte": datetime.utcnow() - relativedelta(months=timeframe)
        }
    }
    print("Queries matching incident initials from last year:",
          collection.count_documents(query))


def get_risk_assessment(form: submit_schema.Form, timeframe) -> RiskAssessment:
    prev_year_incidents = query_mongo(form.client_primary, timeframe)
    print(prev_year_incidents)
    risk_score = (risk_scores.program_to_risk_map.get_risk_score(form.program) +
                  risk_scores.incident_type_to_risk_map.get_risk_score(
                      form.incident_type_primary) +
                  risk_scores.response_to_risk_map.get_risk_score(
                      form.immediate_response))

    max_risk_score = (
        risk_scores.program_to_risk_map.max_risk_score() +
        risk_scores.incident_type_to_risk_map.max_risk_score() +
        risk_scores.response_to_risk_map.max_risk_score_with_value_count(
            len(form.immediate_response)))

    percent_of_max = risk_score / max_risk_score

    for max_percent, assessment in assessment_ranges:
        if percent_of_max <= max_percent:
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
