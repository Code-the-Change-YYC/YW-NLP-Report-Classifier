import re

from scrubadub.detectors.base import RegexDetector
from scrubadub.filth import RegexFilth


class InitialsFilth(RegexFilth):
    regex = re.compile(r"\s+[A-Z][A-Z]\s+")
    type = "Initials"


class InitialsDetector(RegexDetector):
    filth_cls = InitialsFilth
