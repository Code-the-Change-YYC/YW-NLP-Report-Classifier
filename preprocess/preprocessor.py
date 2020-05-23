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
