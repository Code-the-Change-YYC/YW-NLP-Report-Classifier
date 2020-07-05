from os import path
import sys
from typing import List, Type

import pandas as pd

from datetime_map.mapper import DatetimeMapper
from incident_types.processor import IncidentTypesProcessor
from clean.word_character_filter import WordCharacterFilter
from clean.lowercaser import Lowercaser
from preprocessor import Preprocessor
from report_data_d import _ColName, ColName
from scrub.description_scrub import DescriptionScrubber


class ReportData:
    pipeline: List[Type[Preprocessor]] = [
        DescriptionScrubber,
        IncidentTypesProcessor,
        DatetimeMapper,
        WordCharacterFilter,
        Lowercaser
    ]
    dir_path = path.dirname(path.realpath(__file__))
    in_file_path: str = path.join(dir_path, "data/data-sensitive.csv")
    out_file_path: str = path.join(dir_path, "data/data-processed.csv")

    def __init__(self, in_file_path: str = in_file_path,
                 out_file_path: str = out_file_path):
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
        # Add all additional columns not included in the original csv
        for processor in self.pipeline:
            report_df = processor().add_columns(report_df)
        # Use enum for column access. This works because enum's are iterable and
        # ordered.
        report_df.columns = _ColName
        return report_df

    def process_report_data(self) -> pd.DataFrame:
        """
        :return: Processed report data.
        """
        report_df = self.get_raw_report_data()
        for processor in self.pipeline:
            report_df = processor().process(report_df)
        return report_df

    def create_preprocessed_csv(self):
        """Create new .csv file with scrubbed data."""
        self.process_report_data().to_csv(self.out_file_path, index=False)

    def get_processed_data(self) -> pd.DataFrame:
        """Reads processed data directly from out_file_path into a DataFrame.

        :return: Processed data, indexed by the updated ColName enum.
        """
        report_df = pd.read_csv(self.out_file_path, header=0, names=ColName)
        return report_df


# Expects 0-2 arguments. First argument specifies input file path, second
# specifies output file path
if __name__ == '__main__':
    file_names = sys.argv[1:]
    ReportData(*file_names).create_preprocessed_csv()
