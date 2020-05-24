import sys

python_version = sys.version_info
if not (python_version.major == 3 and python_version.minor <= 6):
    raise ImportError('This package requires Python version 3.6 or earlier.')
