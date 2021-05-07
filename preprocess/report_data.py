from server.schemas.submit import Form
import sys
from os import path
from typing import IO, List, Optional, Any, cast

import pandas as pd

from preprocess.clean.lowercaser import Lowercaser
from preprocess.clean.word_character_filter import WordCharacterFilter
from preprocess.datetime_map.mapper import DatetimeMapper
from preprocess.incident_types.processor import IncidentTypesProcessor
from preprocess.lemmatize.ntlk_lemmatize import NLTKLemmatizer
from preprocess.preprocessor import Preprocessor
from preprocess.report_data_d import _ColName, ColName
from preprocess.spacy_scrubber.description_scrub import DescriptionScrubber
# from scrubadub_scrubber.description_scrub import DescriptionScrubber

# use for filepath relative from this file
dir_path = path.dirname(path.realpath(__file__))


class DescriptionProcessor(Preprocessor):

    def __init__(self, **processor_args):
        self.processor_args = processor_args
        self.processors = (DescriptionScrubber(**processor_args),
                           WordCharacterFilter(**processor_args),
                           Lowercaser(**processor_args),
                           NLTKLemmatizer(**processor_args))

    def process(self, report_data: pd.DataFrame) -> pd.DataFrame:
        for processor in self.processors:
            report_data = processor.process(report_data)
        return report_data


class ReportData:
    pipeline: Optional[List[Preprocessor]] = None
    in_file_path: str = path.join(dir_path, 'data', 'data-sensitive.csv')
    out_file_path: str = path.join(dir_path, 'data', 'data-processed.csv')

    def __init__(self,
                 in_file_path: str = in_file_path,
                 out_file_path: str = out_file_path,
                 **processor_args):
        """
        Params:
            in_file_path: Input report data file path 
            out_file_path: Output report file path
            processor_args: Arguments to be passed to the constructors of each preprocessor.
        """
        self.in_file_path = in_file_path
        self.out_file_path = out_file_path
        self.desc_processor = DescriptionProcessor(**processor_args)
        if ReportData.pipeline is None:
            ReportData.pipeline = [
                DatetimeMapper(**processor_args),
                IncidentTypesProcessor(**processor_args),
                self.desc_processor
            ]
            

    def get_raw_report_data(self, file_spec: Any = None) -> pd.DataFrame:
        """
        Params:
            file_spec: Type as passed to pd.read_csv
        Returns:
            Unprocessed report data.
        """
        if file_spec is None:
            file_spec = self.in_file_path
        report_df = cast(pd.DataFrame, pd.read_csv(file_spec))
        # Add all additional columns not included in the original csv
        for processor in self.pipeline:
            report_df = processor.add_columns(report_df)
        # Use enum for column access. This works because enum's are iterable and
        # ordered.
        report_df.columns = _ColName
        return report_df

    def process_report_data(self, file_spec = None) -> pd.DataFrame:
        """
        Params:
            file_spec: see `get_raw_report_data`
        Returns:
            Processed report data.
        """
        report_df = self.get_raw_report_data(file_spec)
        for processor in self.pipeline:
            print(f'Starting {processor.__class__.__name__}')
            report_df = processor.process(report_df)
            print(f'Finished {processor.__class__.__name__}')
        return report_df

    def process_form_submission(self, form_submission: Form) -> Form:
        """
        Returns:
            Processed report data.
        """
        report_df = pd.DataFrame({
            _ColName.DESC: [form_submission.description],
            _ColName.CLI_PRI: [form_submission.client_primary],
            _ColName.CLI_SEC: [form_submission.client_secondary],
        })
        report_df = self.desc_processor.process(report_df)
        new_form_submission = form_submission.copy()
        new_form_submission.description = report_df.at[0, _ColName.DESC]
        return new_form_submission

    def create_preprocessed_csv(self):
        """Create new .csv file with scrubbed data."""
        self.process_report_data().to_csv(self.out_file_path, index=False)

    def get_processed_data(self) -> pd.DataFrame:
        """Reads processed data directly from out_file_path into a DataFrame.

        Returns:
            Processed data, indexed by the updated ColName enum.
        """
        report_df = pd.read_csv(self.out_file_path, header=0, names=ColName)
        return report_df


# Expects 0-2 arguments. First argument specifies input file path, second
# specifies output file path
if __name__ == '__main__':
    file_names = sys.argv[1:]
    ReportData(
        *file_names,    # Spacy scrubber
        ent_replacement='someone',    # Scrubadub scrubber
        uids_for_initials=False,
        initials_placeholder='someone').create_preprocessed_csv()
