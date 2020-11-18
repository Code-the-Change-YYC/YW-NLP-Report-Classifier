from enum import Enum
import server.schemas.submit as submit_schema
from typing import List, Tuple
import yagmail

import server.risk_scores.risk_scores as risk_scores
from server.risk_scores.yagmail_secrets import gmail_username, gmail_password


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
assessment_ranges: List[AssessmentRange] = [
    (1/3, RiskAssessment.LOW),
    (1/3*2, RiskAssessment.MEDIUM),
    (1, RiskAssessment.HIGH)
]
assessment_ranges.sort(key=lambda range: range[0])


def get_risk_assessment(form: submit_schema.Form) -> RiskAssessment:
    risk_score = (
        risk_scores.program_to_risk_map.get_risk_score(form.program) +
        risk_scores.incident_type_to_risk_map.get_risk_score(form.incident_type_primary) +
        risk_scores.response_to_risk_map.get_risk_score(
            form.immediate_response)
    )
    max_risk_score = (
        risk_scores.program_to_risk_map.max_risk_score() +
        risk_scores.incident_type_to_risk_map.max_risk_score() +
        risk_scores.response_to_risk_map.max_risk_score_with_value_count(
            len(form.immediate_response))
    )
    percent_of_max = risk_score / max_risk_score

    for max_percent, assessment in assessment_ranges:
        if percent_of_max <= max_percent:
            if assessment == RiskAssessment.HIGH:
                email_high_risk_alert()
            return assessment

    return RiskAssessment.UNDEFINED

yag = yagmail.SMTP(gmail_username, gmail_password)

def email_high_risk_alert():
    yag.send(
        gmail_username, 
        subject="High risk assessment determined", 
        contents="A high risk assessment was determined in a recently filled out form"
        )