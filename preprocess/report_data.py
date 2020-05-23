from typing import List, Type

import pandas as pd

from incident_types.processor import IncidentTypesProcessor
from preprocessor import Preprocessor
from report_data_d import ColName
from scrub.description_scrub import DescriptionScrubber


def get_raw_report_data() -> pd.DataFrame:
    # use pandas to get csv description column
    report_df = pd.read_csv("data/data-sensitive.csv")
    # Use enum for column access. This works because enum's are iterable and
    # ordered.
    report_df.columns = ColName
    return report_df


pipeline: List[Type[Preprocessor]] = [
    DescriptionScrubber,
    IncidentTypesProcessor
]

if __name__ == '__main__':
    report_data = get_raw_report_data()

    for processor in pipeline:
        report_data = processor().process(report_data)

    # create new .csv file with scrubbed data
    report_data.to_csv("data/data-scrubbed.csv", index=False)
