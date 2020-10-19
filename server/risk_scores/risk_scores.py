from typing import Dict, Sequence


RiskScoreMapKey = str
RiskScoreMapValue = int
RiskScoreMap = Dict[RiskScoreMapKey, RiskScoreMapValue]

incident_type_to_risk: RiskScoreMap = {
    "child abandonment": 1,
    "client aggression towards another person": 1,
    "client aggression towards property": 3,
    "client death (offsite)": 1,
    "client death (onsite)": 4,
    "client missing": 4,
    "concern for welfare of a child": 4,
    "covid-19 confirmed": 5,
    "exposure": 1,
    "homicide (Threat or attempt)": 3,
    "illegal activity on premises": 5,
    "injury": 2,
    "media/3rd party contact": 3,
    "medical emergency": 2,
    "mental health emergency": 2,
    "security concern": 1,
    "suicide attempt": 3,
    "suspected or actual breach of privacy": 3,
    "suspicion/allegation of abuse towards or against client": 3,
    "suspicion/allegation of child abuse - child is not a client": 4,
    "other": 1,
}

program_to_risk: RiskScoreMap = {
    "child care hub": 5,
    "child support": 5,
    "compass": 1,
    "counselling": 1,
    "croydon": 4,
    "DCRT": 3,
    "dropin child care": 3,
    "employment resource center": 1,
    "family access": 2,
    "family resource network": 3,
    "intensive case management": 5,
    "LINC": 2,
    "mindful moments": 4,
    "outreach counselling": 3,
    "providence (community housing)": 4,
    "sheriff king home": 1,
    "the maple (community housing)": 4,
    "transitional housing": 1,
}

response_to_risk: RiskScoreMap = {
    "called child welfare": 5,
    "evacuation": 4,
    "first-aid provided": 4,
    "infection prevention protocol": 2,
    "mental health assessment": 5,
    "naloxone administered": 5,
    "person barred/access restricted": 2,
    "safety assessment": 5,
    "safety planning": 5,
    "other": 2,
}


class FieldRiskScoreMap:
    _risk_score_map: RiskScoreMap

    def __init__(self, risk_score_map: RiskScoreMap):
        self._risk_score_map = risk_score_map

    def max_risk_score(self) -> int:
        """
        Returns the maximum possible risk score this field could receive.
        """
        risk_scores = self._risk_score_map.values()
        return max(risk_scores)

    def get_risk_score(self, field_value: RiskScoreMapKey) -> float:
        """
        Calculates the risk score for this field with the given `field_value` as
        its input.
        """
        return self._risk_score_map[field_value]


class MultiValFieldRiskScoreMap(FieldRiskScoreMap):
    def max_risk_score_with_value_count(self, value_count: int) -> int:
        """
        :value_count: The number of values entered into the field.
        """
        risk_scores = sorted(self._risk_score_map.values(), reverse=True)
        return sum(risk_scores[:value_count])

    def get_risk_score(self, field_value: Sequence[RiskScoreMapKey]) -> float:
        return sum(map(self._risk_score_map.__getitem__, field_value))


incident_type_to_risk_map = FieldRiskScoreMap(incident_type_to_risk)
program_to_risk_map = FieldRiskScoreMap(program_to_risk)
response_to_risk_map = MultiValFieldRiskScoreMap(response_to_risk)
