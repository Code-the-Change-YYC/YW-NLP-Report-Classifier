# NOTE: The scrubadub library is broken as of Python 3.7, so please downgrade
# to Python 3.6 before using this script. This is noted in the .python-version
# file if you are using pyenv.

import re

import pandas as pd
import scrubadub
from scrubadub.detectors.base import RegexDetector
from scrubadub.filth import RegexFilth

from preprocessor import Preprocessor

# Custom scrubadub logic
# List of words that should remain unscrubbed
# Note: These are converted to lower case anyways
whitelisted_words = [
    "Staff",
    "EMS",
    "Fire",
    "CPS",
    "Rockyview",
    "Rocky",
    "View",
    "Health",
    "Link",
    "Sheldon",
    "Gabapentin",
    "Chumir",
    "Hospital",
    "Fentanyl",
    "Writer",
    "Crystal",
    "Meth",
    "Overdose",
    "Police",
    "Client",
    "First",
    "Aid",
    "Providence",
]


class CustomNameDetector(scrubadub.detectors.NameDetector):
    """Detector that will run through descriptions and detect sensitive data such as names.


    Upon initialization loops through whitelisted words to append to disallowed nouns, so non-sensitive data
    isn't unnecesarily scrubbed.
    """

    def __init__(self):
        for word in whitelisted_words:
            self.disallowed_nouns.add(word)


class InitialsFilth(RegexFilth):
    """Classifies filth for InitialsDetector using regex.

    Will classify sequence of 2 capital letters as filth, excluding AM and PM.
    """

    regex = re.compile(
        r"\b(?!AM|PM)([A-Z]{2})"
    )  # Excluding AM or PM, sequence that starts with 2 capital letters.
    type = "Initials"


class InitialsDetector(RegexDetector):
    """Utilizes InitialsFilth to detect filth.

    Additional detector added to scrubber to scrub initials.
    """

    filth_cls = InitialsFilth


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
        descriptions = report_data["DESCRIPTION"]

        scrubbed_descriptions = []
        # loop to clean
        for description in descriptions:
            scrubbed_descriptions.append(self.scrubber.clean(description, replace_with="identifier"))

        # update pandas column
        report_data["DESCRIPTION"] = scrubbed_descriptions

        return report_data
