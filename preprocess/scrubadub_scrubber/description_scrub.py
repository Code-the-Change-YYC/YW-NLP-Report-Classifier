# NOTE: The scrubadub library is broken as of Python 3.7, so please downgrade
# to Python 3.6 before using this script. This is noted in the .python-version
# file if you are using pyenv.

import pandas as pd
import scrubadub

from preprocess.preprocessor import Preprocessor
from preprocess.report_data_d import _ColName
from preprocess.scrubadub_scrubber.initials_detect import InitialsDetector
from preprocess.scrubadub_scrubber.name_detect import CustomNameDetector


class DescriptionScrubber(Preprocessor):
    """Scrubs out sensitive data from the report's descriptions."""

    _uids_for_initials: bool

    scrubber: scrubadub.Scrubber

    def __init__(self, uids_for_initials=True, initials_placeholder='someone'):
        """
        :param uids_for_initials: Whether or not unique identifiers should be
        used to replace initials. If `False`, `initials_placeholder` will be
        used instead.
        """
        super().__init__()
        self._uids_for_initials = uids_for_initials
        self.scrubber = scrubadub.Scrubber()
        # replace default name detector with new name detector that doesn't delete keywords
        self.scrubber.remove_detector("name")

        custom_detectors = (CustomNameDetector, InitialsDetector)

        # Use placeholders instead of uids if specified
        if not uids_for_initials:
            # noinspection PyProtectedMember
            for detector in [*custom_detectors, *self.scrubber._detectors.values()]:
                detector.filth_cls.placeholder = initials_placeholder
                # Don't add '{{'/'}}' prefix/suffix
                detector.filth_cls.prefix = detector.filth_cls.suffix = ''
                # Prevent merging because it doesn't respect the placeholder
                detector.filth_cls.merge = lambda _self, other: _self

        for detector in custom_detectors:
            self.scrubber.add_detector(detector)

    def process(self, report_data: pd.DataFrame) -> pd.DataFrame:
        descriptions = report_data[_ColName.DESC]

        scrubbed_descriptions = []
        # loop to clean
        for description in descriptions:
            scrubbed_descriptions.append(self.scrubber.clean(
                description, replace_with='identifier' if self._uids_for_initials else 'placeholder'))

        # update pandas column
        report_data[_ColName.DESC] = scrubbed_descriptions

        return report_data
