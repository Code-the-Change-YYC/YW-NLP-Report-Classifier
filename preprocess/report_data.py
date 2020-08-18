import sys
from os import path
from typing import List, Type

import pandas as pd

from clean.lowercaser import Lowercaser
from clean.word_character_filter import WordCharacterFilter
from datetime_map.mapper import DatetimeMapper
from incident_types.processor import IncidentTypesProcessor
from lemmatize.ntlk_lemmatize import NLTKLemmatizer
from preprocessor import Preprocessor
from report_data_d import _ColName, ColName
from spacy_scrubber.description_scrub import DescriptionScrubber

# use for filepath relative from this file
dir_path = path.dirname(path.realpath(__file__))


class ReportData:
    pipeline: List[Type[Preprocessor]] = [
        DescriptionScrubber,
        IncidentTypesProcessor,
        DatetimeMapper,
        WordCharacterFilter,
        Lowercaser,
        NLTKLemmatizer
    ]
    in_file_path: str = path.join(dir_path, 'data', 'data-sensitive.csv')
    out_file_path: str = path.join(dir_path, 'data', 'data-processed.csv')

    def __init__(self, in_file_path: str = in_file_path,
                 out_file_path: str = out_file_path, **processor_args):
        """
        :param in_file_path:
        :param out_file_path:
        :param processor_args: Arguments to be passed to the constructors of each preprocessor.
        """
        self.in_file_path = in_file_path
        self.out_file_path = out_file_path
        self._processor_args = processor_args

    def get_raw_report_data(self) -> pd.DataFrame:
        """
        :return: Unprocessed report data.
        """
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
            report_df = processor(**self._processor_args).process(report_df)
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
    ReportData(*file_names, ent_replacement='someone', uids_for_initials=True,
               initials_placeholder='someone').create_preprocessed_csv()
