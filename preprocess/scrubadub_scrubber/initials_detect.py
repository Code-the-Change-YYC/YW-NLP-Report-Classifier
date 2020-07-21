import re

from scrubadub.detectors.base import RegexDetector
from scrubadub.filth import RegexFilth


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
