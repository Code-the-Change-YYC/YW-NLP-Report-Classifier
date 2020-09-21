from datetime import datetime

import pandas as pd
from dateutil.parser import parser

from preprocess.preprocessor import Preprocessor
from preprocess.report_data_d import _ColName


class DatetimeMapper(Preprocessor):
    additional_columns = {_ColName.HOUR_OF_DAY,
                          _ColName.MORNING,
                          _ColName.AFTERNOON,
                          _ColName.EVENING,
                          _ColName.NIGHT,
                          _ColName.WEEKDAY}

    def process(self, report_data: pd.DataFrame) -> pd.DataFrame:
        """Fill `self.additional_columns` using the value of the incident
        datetime column.

        - The hour column is given the hour of the day specified within the incident datetime column
        - The weekday column is given 1/0 indicating whether the datetime is a weekday
        - The time of day columns are given 1/0s
        """
        incident_datetimes: pd.Series = report_data[_ColName.DT_INC]
        for i, dt_str in enumerate(incident_datetimes):
            dt = self._parse_datetime(dt_str)
            report_data.at[i, _ColName.HOUR_OF_DAY] = dt.hour
            report_data.at[i, _ColName.WEEKDAY] = int(0 <= dt.weekday() <= 4)
            report_data.at[i, self._time_of_day(dt)] = 1

        return report_data

    def add_columns(self, report_data: pd.DataFrame) -> pd.DataFrame:
        """Adds `self.additional_columns` to the dataframe, initializing them to 0."""
        column_index: int = len(report_data.columns)
        for col in self.additional_columns:
            report_data.insert(column_index, col, 0)
            column_index += 1
        return report_data

    @staticmethod
    def _parse_datetime(dt_str: str) -> datetime:
        """
        :param dt_str: String representing a datetime.
        :return: Object representing the datetime contained in `dt_str`.
        """
        return parser().parse(dt_str)

    @staticmethod
    def _time_of_day(dt: datetime) -> _ColName:
        """
        :param dt:
        :return: Morning between 5am and noon, afternoon between noon and 5pm,
        evening between 5pm and 9pm, night otherwise.
        """
        hour = dt.hour
        if 5 <= hour <= 11:
            return _ColName.MORNING
        elif 12 <= hour <= 16:
            return _ColName.AFTERNOON
        elif 17 <= hour <= 20:
            return _ColName.EVENING
        else:
            return _ColName.NIGHT
