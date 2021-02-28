# YW NLP Classifier Project

This repository contains a model for classifying critical incident reports for the YW.

This project was completed by the YW-NLP team for Code the Change YYC 2020.

## Python Development

### Python Environment

It is recommended to use a tool for Python installation management such as [pyenv](https://github.com/pyenv/pyenv) on Mac/Unix or [pyenv-win](https://github.com/pyenv-win/pyenv-win) on Windows. The primary project Python version is listed in `.python-version`.

Once a suitable Python is installed it is recommended to create a virtual environment for the root project.

> Note: Some packages may recommend a different setup for their development and the below steps may not be necessary.

The built-in `venv` will be used for the instructions:

1. Create the virtual environment with `python -m venv .env`. Ensure the Python executable is the desired version.
2. Activate the virtual environment in your shell. This will differ based on your system. In PowerShell the command is `.\.env\Scripts\activate`. On Mac/Linux, the command is `source ./.env/bin/activate`. See [here](https://docs.python.org/3/library/venv.html#creating-virtual-environments) for details.
3. Use this environment for `python` and `pip` calls during development.
4. Run `pre-commit` install to install all pre-commit hooks.

### Packages

Dependencies are split up by development environment using multiple `requirements.txt` files. The root `requirements.txt` contains shared dependencies and generally should not be used directly for installation. Instead it is recommended to follow the README instructions in the individual packages depending on the section you are developing. Development environments include:

- `training`: This includes training of the project's models in IPython notebooks.
- `preprocess`: This includes the general preprocessing of the raw report data.

### Credentials

In order to use third-party libraries on the backend such as Sanity, Interceptum, and `yagmail` integration, put a `credentials.json` file in a `keys` folder. The format of the JSON file should follow [this template](https://gist.github.com/JCayabyab/93d6a2a010096d4ae6738d492d4624d8). Send an email to [jofred.cayabyab1@ucalgary.ca](mailto:jofred.cayabyab1@ucalgary.ca) for help setting up these credentials.

## AWS Deployment

For updated deployment to our AWS server, run `server/deploy.sh` from the root folder. This script assumes that the necessary access permissions are granted before the script runs.

Note: The docker-compose files in the root folder are currently not being used for deployment.
