# Critical Incident Report Data Pre-processing

This package provides pre-processing functionality for the initial data sent to us by the YW.

The `report_data.py` can be run as a script (see below).

**NOTE:** If the original data is needed, please reach out to the Code the Change YYC organization at [codethechangeyyc@gmail.com](mailto:codethechangeyyc@gmail.com)

## Usage

1. Save the downloaded YW data as `data-sensitive.csv` into the `data` folder.
2. Install the requirements using `pip install -r requirements.txt`.
3. Run the script using `python report_data.py`. The script expects 0-2
arguments. First argument specifies input file path, second specifies output
file path.

**Note:** If you are using the scrubadub preprocessor you would need to run the files using an older version of Python than 3.7, see `.python-version` for the recommended version.

## Development

### Python Environment

This package requires Python 3.6 due to it's dependency on `scrubadub`. It is recommended to create a virtual environment specific to this package for use during development. See the root README for instructions on Python environment setup. Ensure this virtual environment is activated during development.

### Packages

To install the package's dependencies, ensure your Python 3.6 virtual environment is activated and run
```shell script
pip install -r preprocess/requirements.txt
```
