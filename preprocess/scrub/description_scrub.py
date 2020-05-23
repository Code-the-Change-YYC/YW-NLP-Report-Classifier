# NOTE: The scrubadub library is broken as of Python 3.7, so please downgrade
# to Python 3.6 before using this script. This is noted in the .python-version
# file if you are using pyenv.

import pandas as pd
import scrubadub

from preprocessor import Preprocessor
from report_data_d import ColNames
from scrub.initials_detect import InitialsDetector
from scrub.name_detect import CustomNameDetector


class DescriptionScrubber(Preprocessor):
    """Scrubs out sensitive data from the report's descriptions."""

    scrubber: scrubadub.Scrubber

    def __init__(self):
        self.scrubber = scrubadub.Scrubber()
        # replace default name detector with new name detector that doesn't delete keywords
        self.scrubber.remove_detector("name")
        self.scrubber.add_detector(CustomNameDetector)
        self.scrubber.add_detector(InitialsDetector)

    def process(self, report_data: pd.DataFrame) -> pd.DataFrame:
        descriptions = report_data[ColNames.DESC]

        scrubbed_descriptions = []
        # loop to clean
        for description in descriptions:
            scrubbed_descriptions.append(self.scrubber.clean(description, replace_with="identifier"))

        # update pandas column
        report_data[ColNames.DESC] = scrubbed_descriptions

        return report_data
