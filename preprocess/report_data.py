import sys
from typing import List, Type

import pandas as pd

from incident_types.processor import IncidentTypesProcessor
from preprocessor import Preprocessor
from report_data_d import ColName
from scrub.description_scrub import DescriptionScrubber


class ReportData:
    pipeline: List[Type[Preprocessor]] = [
        DescriptionScrubber,
        IncidentTypesProcessor
    ]
    in_file_path: str
    out_file_path: str

    def __init__(self, in_file_path: str = "data/data-sensitive.csv",
                 out_file_path: str = "data/data-processed.csv"):
        """
        :param in_file_path:
        :param out_file_path:
        """
        self.in_file_path = in_file_path
        self.out_file_path = out_file_path

    def get_raw_report_data(self) -> pd.DataFrame:
        """
        :return: Unprocessed report data.
        """
        # use pandas to get csv description column
        report_df = pd.read_csv(self.in_file_path)
        # Use enum for column access. This works because enum's are iterable and
        # ordered.
        report_df.columns = ColName
        return report_df

    def get_report_data(self) -> pd.DataFrame:
        """
        :return: Processed report data.
        """
        report_df = self.get_raw_report_data()
        for processor in self.pipeline:
            report_df = processor().process(report_df)
        return report_df

    def create_preprocessed_csv(self):
        """Create new .csv file with scrubbed data."""
        self.get_report_data().to_csv(self.out_file_path, index=False)


# Expects 0-2 arguments. First argument specifies input file path, second
# specifies output file path
if __name__ == '__main__':
    file_names = sys.argv[1:]
    ReportData(*file_names).create_preprocessed_csv()
