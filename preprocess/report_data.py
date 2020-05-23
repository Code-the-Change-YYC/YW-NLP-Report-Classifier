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
    file_name_sensitive = "data/data-sensitive.csv"
    file_name_scrubbed = "data/data-scrubbed.csv"

    def get_raw_report_data(self) -> pd.DataFrame:
        """
        :return: Unprocessed report data.
        """
        # use pandas to get csv description column
        report_df = pd.read_csv(self.file_name_sensitive)
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

    def create_scrubbed_csv(self):
        """Create new .csv file with scrubbed data."""
        self.get_report_data().to_csv("data/data-scrubbed.csv", index=False)


if __name__ == '__main__':
    ReportData().create_scrubbed_csv()
