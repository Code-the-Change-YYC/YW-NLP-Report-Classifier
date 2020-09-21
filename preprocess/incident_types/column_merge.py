import pandas as pd

from preprocess.incident_types.incident_types_d import IncidentType
from preprocess.preprocessor import Preprocessor
from preprocess.report_data_d import _ColName


class ColumnMerger(Preprocessor):
    def process(self, report_data: pd.DataFrame) -> pd.DataFrame:
        """Merges the old incident type columns into the new, removes the old.

        :param report_data:
        :return: The updated data.
        """
        report_data[_ColName.INC_T1] = self.merge(report_data[_ColName.INC_T1], report_data[_ColName.INC_T1_OLD])
        report_data[_ColName.INC_T2] = self.merge(report_data[_ColName.INC_T2], report_data[_ColName.INC_T2_OLD])

        # remove old columns
        return report_data[[col for col in report_data if col not in [_ColName.INC_T1_OLD, _ColName.INC_T2_OLD]]]

    @staticmethod
    def merge(primary_col: pd.Series, secondary_col: pd.Series,
              exception: str = IncidentType.OTR.value, default: str = IncidentType.OTR.value) -> pd.Series:
        """Merge the two columns, prioritizing values from `primary_col` except
        where the `primary_col` value equals `exception`.

        `exception` values are still prioritized over NA/NaN values.

        If neither column contains a value, `default` is inserted.

        :param primary_col:
        :param secondary_col:
        :param exception:
        :param default:
        """
        na_val = ''
        primary_col: pd.Series = primary_col.fillna(na_val)
        secondary_col: pd.Series = secondary_col.fillna(na_val)

        for i, (primary, secondary) in enumerate(zip(primary_col, secondary_col)):
            if (primary == exception or primary == na_val) and secondary != na_val:
                primary_col[i] = secondary
            elif primary == secondary == na_val:
                primary_col[i] = default

        return primary_col
