from typing import Iterable

import pandas as pd

from incident_types.column_merge import merge_columns
from incident_types.incident_types_d import replacements
from preprocessor import Preprocessor
from report_data_d import ColName


def normalize_inc_type(col: pd.Series) -> pd.Series:
    return col.str.strip().str.capitalize()


class IncidentTypesProcessor(Preprocessor):
    """Normalize and apply corrections to the incident type columns."""

    col_names: Iterable[str] = {
        ColName.INC_T1,
        ColName.INC_T1_OLD,
        ColName.INC_T2,
        ColName.INC_T2_OLD,
    }

    def __init__(self, col_names: Iterable[str] = None):
        """
        :param col_names: The names of the incident type columns to process
        """
        if col_names is not None:
            self.col_names = col_names

    def process(self, report_data: pd.DataFrame) -> pd.DataFrame:
        for col_name in self.col_names:
            report_data[col_name] = normalize_inc_type(report_data[col_name])
            report_data[col_name].replace(replacements, inplace=True)

        return merge_columns(report_data)
