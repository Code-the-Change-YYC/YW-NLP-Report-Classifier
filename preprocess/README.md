# Critical Incident Report Data Pre-processing

This package provides pre-processing functionality for the initial data sent to us by the YW.

The `report_data.py` can be run as a script (see below).

**NOTE:** If the original data is needed, please reach out to the Code the Change YYC organization at [codethechangeyyc@gmail.com](mailto:codethechangeyyc@gmail.com)

USAGE: 
1. Save the downloaded YW data as `data-sensitive.csv` into the `data` folder.
2. Install the requirements using `pip install -r requirements.txt`.
3. Download the Spacy.io's pretrained model using `python -m spacy download en_core_web_lg`
4. Run the script using `python report_data.py`. The script expects 0-2
arguments. First argument specifies input file path, second specifies output
file path.

## Tests

- Using python's built-in
[unittest](https://docs.python.org/3/library/unittest.html) module
- Run tests with `python -m unittest` or through your IDE