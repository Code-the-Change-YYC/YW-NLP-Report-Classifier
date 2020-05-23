from typing import List, Type

import pandas as pd

from incident_types import IncidentTypesProcessor
from preprocessor import Preprocessor
from scrub import DescriptionScrubber

# rename columns by index
columns = [
    "DATETIME_INCIDENT",
    "LOCATION",
    "LOCATION_DETAIL",
    "CLIENT_PRIMARY",
    "CLIENT_SECONDARY",
    "CHILD_INVOLVED",
    "NON_CLIENT_INVOLVED",
    "PROGRAM",
    "CFS",
    "EMS",
    "FIRE",
    "MISC_SERVICE_FLAG",
    "DOAP_PACT",
    "POLICE",
    "MISC_SERVICE",
    "INCIDENT_TYPE_1",
    "INCIDENT_TYPE_2",
    "INCIDENT_1_OLD",
    "INCIDENT_TYPE_OTHER",
    "DESCRIPTION",
    "RESPONSE_CHILD_WELFARE",
    "RESPONSE_EVAC",
    "RESPONSE_FIRST_AID",
    "RESPONSE_INFECTION_PREVENTION_PROTOCOL",
    "RESPONSE_MENTAL_ASSESSMENT",
    "RESPONSE_NALOXONE",
    "RESPONSE_PERSON_BARRED",
    "RESPONSE_SAFETY_ASSESSMENT",
    "RESPONSE_SAFETY_PLANNING",
    "RESPONSE_OTHER",
    "RESPONSE_OTHER_DESC",
    "DATETIME_WRITTEN",
]


def get_raw_report_data() -> pd.DataFrame:
    # use pandas to get csv description column
    report_df = pd.read_csv("data/data-sensitive.csv")
    report_df.columns = columns
    return report_df


pipeline: List[Type[Preprocessor]] = [DescriptionScrubber, IncidentTypesProcessor]

if __name__ == '__main__':
    report_data = get_raw_report_data()

    for processor in pipeline:
        report_data = processor().process(report_data)

    # create new .csv file with scrubbed data
    report_data.to_csv("data/data_scrubbed.csv", index=False)
