import logging
from sys import version_info as python_version

if not (python_version.major == 3 and python_version.minor <= 6):
    logging.warning("This package requires Python version 3.6 or earlier.")
