from abc import ABC, abstractmethod

import pandas as pd


class Preprocessor(ABC):
    @abstractmethod
    def process(self, report_data: pd.DataFrame) -> pd.DataFrame:
        """Apply a pre-processing step to report_data.

        :param report_data: Data to be processed. NOTE: This method can modify
        this value.
        :return: The updated data.
        """
        ...

    def add_columns(self, report_data: pd.DataFrame) -> pd.DataFrame:
        """Override this to add any additional columns created by this
        preprocessor step to the dataframe.

        :param report_data: Data to which the columns are added. NOTE: This method can modify
        this value.
        :return: The updated data.
        """
        return report_data
