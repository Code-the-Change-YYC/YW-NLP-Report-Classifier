import re

from scrubadub.detectors.base import RegexDetector
from scrubadub.filth import RegexFilth


class InitialsFilth(RegexFilth):
    regex = re.compile(r"\b[A-Z]{2}\d*\b")
    type = "Initials"


class InitialsDetector(RegexDetector):
    filth_cls = InitialsFilth
