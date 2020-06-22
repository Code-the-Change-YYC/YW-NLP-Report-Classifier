from datetime import datetime
from enum import Enum

import pandas as pd
from dateutil.parser import parser

from preprocessor import Preprocessor
from report_data_d import _ColName


class TimeOfDay(Enum):
    MORNING = 'morning'
    AFTERNOON = 'afternoon'
    EVENING = 'evening'
    NIGHT = 'night'


class DatetimeMapper(Preprocessor):
    additional_columns = {_ColName.HOUR_OF_DAY, _ColName.TIME_OF_DAY, _ColName.WEEKDAY}

    def process(self, report_data: pd.DataFrame) -> pd.DataFrame:
        """Fill `self.additional_columns` using the value of the incident
        datetime column.

        - The hour column is given the hour of the day specified within the incident datetime column
        - The weekday column is given a boolean indicating whether the datetime is a weekday
        - The time of day column is given a value from `TimeOfDay` based on the time of day in the datetime
        """
        incident_datetimes: pd.Series = report_data[_ColName.DT_INC]
        for i, dt_str in enumerate(incident_datetimes):
            dt = self._parse_datetime(dt_str)
            report_data.at[i, _ColName.HOUR_OF_DAY] = dt.hour
            report_data.at[i, _ColName.WEEKDAY] = 0 <= dt.weekday() <= 4
            report_data.at[i, _ColName.TIME_OF_DAY] = self._time_of_day(dt).value

        return report_data

    def add_columns(self, report_data: pd.DataFrame) -> pd.DataFrame:
        """Adds `self.additional_columns` to the dataframe."""
        column_index: int = len(report_data.columns)
        for col in self.additional_columns:
            report_data.insert(column_index, col, None)
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
    def _time_of_day(dt: datetime) -> TimeOfDay:
        """
        :param dt:
        :return: Morning between 5am and noon, afternoon between noon and 5pm,
        evening between 5pm and 9pm, night otherwise.
        """
        hour = dt.hour
        if 5 <= hour <= 11:
            return TimeOfDay.MORNING
        elif 12 <= hour <= 16:
            return TimeOfDay.AFTERNOON
        elif 17 <= hour <= 20:
            return TimeOfDay.EVENING
        else:
            return TimeOfDay.NIGHT
