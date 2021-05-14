from typing import Iterable, Union

import pandas as pd

from preprocess.incident_types.incident_types_d import replacements, IncidentType
from preprocess.preprocessor import Preprocessor
from preprocess.report_data_d import _ColName


class IncTypeMapper(Preprocessor):
    """Maps old incident types to their current dropdown counterparts."""
    col_names: Iterable[str] = {
        _ColName.INC_T1,
        _ColName.INC_T1_OLD,
        _ColName.INC_T2,
        _ColName.INC_T2_OLD,
    }

    def __init__(self, col_names: Iterable[str] = col_names, **kwargs):
        """
        Params:
            col_names: The names of the incident type columns to process
        """
        super().__init__(**kwargs)
        self.col_names = col_names
        # Add normalized incident types to replacements
        self.replacements = {**replacements,
                             **{self.normalize_inc_type(inc_type.value): inc_type.value for inc_type in IncidentType}}

    def process(self, report_data: pd.DataFrame) -> pd.DataFrame:
        for col_name in self.col_names:
            try:
                report_data[col_name] = report_data[col_name].apply(
                    self.normalize_inc_type)
                report_data[col_name].replace(self.replacements, inplace=True)
            except KeyError as ke:
                print(f"key error: {ke} in preprocess.incident_types.mapper in IncTypeMapper.process")

        return report_data

    IncTypeVal = Union[str, float]

    @staticmethod
    def normalize_inc_type(inc_type: IncTypeVal) -> IncTypeVal:
        if type(inc_type) is float:
            return inc_type
        return inc_type.strip().capitalize()
