from datetime import datetime
from typing import Dict, Sequence


RiskScoreMapKey = str
RiskScoreMapValue = int
RiskScoreMap = Dict[RiskScoreMapKey, RiskScoreMapValue]

incident_type_to_risk: RiskScoreMap = {
    "child abandonment": 3,
    "client aggression towards another person": 3,
    "client aggression towards property": 3,
    "client death (offsite)": 0,
    "client death (onsite)": 0,
    "client missing": 3,
    "concern for welfare of a child": 4,
    "covid-19 confirmed": 5,
    "exposure": 1,
    "homicide (threat or attempt)": 6,
    "illegal activity on premises": 6,
    "injury": 1,
    "media/3rd party contact": 1,
    "medical emergency": 2,
    "mental health emergency": 2,
    "security concern": 1,
    "suicide attempt": 6,
    "suspected or actual breach of privacy": 3,
    "suspicion/allegation of abuse towards or against client": 5,
    "suspicion/allegation of child abuse - child is not a client": 5,
    "other": 1,
}

program_to_risk: RiskScoreMap = {
    "child care (hub)": 5,
    "child support": 5,
    "compass": 1,
    "counselling and personal development": 1,
    "croydon (community housing)": 4,
    "dcrt": 3,
    "drop-in child care": 3,
    "employment resource center": 1,
    "family access": 2,
    "family resource network": 3,
    "intensive case management": 5,
    "linc": 2,
    "mindful moments": 4,
    "outreach counselling": 3,
    "providence (community housing)": 4,
    "sheriff king home": 1,
    "the maple (community housing)": 4,
    "transitional housing": 1,
}

response_to_risk: RiskScoreMap = {
    "called child welfare": 5,
    "evacution": 4,
    "first-aid provided": 3,
    "infection prevention protocol": 2,
    "mental health assessment": 5,
    "naloxone administered": 6,
    "person barred/access restricted": 2,
    "safety assessment": 4,
    "safety planning": 3,
    "other": 2,
}

# TODO: Use meaningful risk values
time_of_day_to_risk: RiskScoreMap = {
    "morning": 1,
    "afternoon": 2,
    "evening": 3,
    "night": 4,
}


class FieldRiskScoreMap:
    _risk_score_map: RiskScoreMap

    def __init__(self, risk_score_map: RiskScoreMap):
        self._risk_score_map = risk_score_map

    def max_risk_score(self) -> int:
        """
        Returns:
            The maximum possible risk score this field could receive.
        """
        risk_scores = self._risk_score_map.values()
        return max(risk_scores)

    def get_risk_score(self, field_value: RiskScoreMapKey) -> float:
        """
        Calculates the risk score for this field with the given `field_value` as
        its input.
        """
        return self._risk_score_map[field_value.lower()]


class MultiValFieldRiskScoreMap(FieldRiskScoreMap):
    def max_risk_score_with_value_count(self, value_count: int) -> int:
        """
        Params:
            value_count: The number of values entered into the field.
        """
        risk_scores = sorted(self._risk_score_map.values(), reverse=True)
        return sum(risk_scores[:value_count])

    def get_risk_score(self, field_value: Sequence[RiskScoreMapKey]) -> float:
        s = sum(map(self._risk_score_map.__getitem__,
                    [f.lower() for f in field_value]))
        return s


class DateFieldRiskScoreMap(FieldRiskScoreMap):
    def get_risk_score(self, field_value: datetime) -> float:
        hour = field_value.hour
        time_of_day: RiskScoreMapKey
        if 5 <= hour <= 11:
            time_of_day = 'morning'
        elif 12 <= hour <= 16:
            time_of_day = 'afternoon'
        elif 17 <= hour <= 20:
            time_of_day = 'evening'
        else:
            time_of_day = 'night'

        return self._risk_score_map[time_of_day]


incident_type_to_risk_map = FieldRiskScoreMap(incident_type_to_risk)
program_to_risk_map = FieldRiskScoreMap(program_to_risk)
response_to_risk_map = MultiValFieldRiskScoreMap(response_to_risk)
occurrence_time_to_risk_map = DateFieldRiskScoreMap(time_of_day_to_risk)
