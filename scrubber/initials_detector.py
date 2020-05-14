import re

from scrubadub.detectors.base import RegexDetector
from scrubadub.filth import RegexFilth


class InitialsFilth(RegexFilth):
    regex = re.compile(r"[A-Z][A-Z]")
    type = "Initials"


class InitialsDetector(RegexDetector):
    filth_cls = InitialsFilth
