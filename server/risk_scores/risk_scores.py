from datetime import datetime
from typing import List, Dict, Sequence
from math import floor

from server.credentials import credentials
from server.sanity_utils import risk_scores_query, headers, run_query

RiskScoreMapKey = str
RiskScoreMapValue = int
RiskScoreMap = Dict[RiskScoreMapKey, RiskScoreMapValue]

MAX_PREVIOUS_INCIDENTS = 3
MAX_RESPONSES_FOR_RISK_SCORE = 3


class RiskScoreData:
    def __init__(self):
        cirForm = run_query(credentials.sanity_gql_endpoint,
                            risk_scores_query, headers)['data']['CirForm']
        self.incident_type_to_risk = self.map_array_to_dict(
            cirForm['primaryIncTypes'], 'name')
        self.program_to_risk = self.map_array_to_dict(
            cirForm['programs'], 'name')
        self.response_to_risk = self.map_array_to_dict(
            cirForm['immediateResponses'], 'name')
        # hardcoded for now - adjusting these values seems lower value, might be an improvement
        # in the future
        self.time_of_day_to_risk = {
            "morning": 1,
            "afternoon": 2,
            "evening": 3,
            "night": 4,
        }

    def map_array_to_dict(self, arr, key_name) -> RiskScoreMap:
        return {entry[key_name].lower(): int(entry['risk_weighting']) for entry in arr}

    def get_maps(self):
        return [self.incident_type_to_risk, self.program_to_risk, self.response_to_risk, self.time_of_day_to_risk]


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


class RiskScoreCombiner:
    _mapping: List[List[int]]

    def __init__(self, filepath: str = 'server/risk_scores/mapping.txt'):
        """
        Reads a text file that contains the mappings for incoming risk scores.
        e.g., _mapping[20, 30] corresponds to the risk score for all scores where:
        0.20 <= score_from_current_incident < 0.21
        0.30 <= score_from_prev_incidents < 0.31
        """
        mapping_file = open(filepath, 'r')
        matrix = []
        for row in mapping_file:
            matrix.append([int(n) for n in list(row)[:-1]])
        self._mapping = matrix

    def combine_risk_scores(self, score_from_current_incident: float, score_from_prev_incidents: float) -> float:
        """
        Returns the value read from the mapping_file for the given scores.
        0 = LOW
        1 = MEDIUM
        2 = HIGH
        """
        if score_from_current_incident > 1:
            raise ValueError('Risk score from incident > 1')
        if score_from_prev_incidents > 1:
            raise ValueError('Risk score from previous incidents > 1')
        curr_score, prev_score = floor(
            score_from_current_incident * 100), floor(score_from_prev_incidents * 100)
        return self._mapping[curr_score][prev_score]


def calc_max_risk_score(incident_map, program_map, response_map, occurrence_time_map):
    single_val_maps = [incident_map, program_map, occurrence_time_map]
    # assumes that no more than 3 services will be involved on average
    return sum([risk_map.max_risk_score() for risk_map in single_val_maps] + [response_map.max_risk_score_with_value_count(MAX_RESPONSES_FOR_RISK_SCORE)])


risk_scores = RiskScoreData()
[incident_type_to_risk, program_to_risk, response_to_risk,
    time_of_day_to_risk] = risk_scores.get_maps()
risk_score_combiner = RiskScoreCombiner()


incident_type_to_risk_map = FieldRiskScoreMap(incident_type_to_risk)
program_to_risk_map = FieldRiskScoreMap(program_to_risk)
response_to_risk_map = MultiValFieldRiskScoreMap(response_to_risk)
occurrence_time_to_risk_map = DateFieldRiskScoreMap(time_of_day_to_risk)
max_risk_score = calc_max_risk_score(
    incident_type_to_risk_map, program_to_risk_map, response_to_risk_map, occurrence_time_to_risk_map)
