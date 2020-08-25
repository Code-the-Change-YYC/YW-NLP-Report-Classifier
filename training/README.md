# Training

Model training is performed beforehand within IPython notebooks.

## Model Saving

The trained models are stored within `../model_output`.

When pickling models all dependencies should be imported from the root of the project. This is so that the models can be unpickled regardless of the location of the start script. For example, a ComplementNB pipeline might require the function `spacy_tokenizer`. If this is imported relative to the current notebook's directory with something like

```python
from utils import spacy_tokenizer
```

any module which wants to unpickle the pipeline must have a `utils` package (with a `spacy_tokenizer`) as a sibling due to the way that pickling works. So instead it should be imported as

```python
from training.description_classification.utils import spacy_tokenizer
```

and this way the pipeline can be unpickled from anywhere as long as a function called `spacy_tokenizer` with a `__module__` of `training.description_classification.utils` (which is easy to accomplish, just import it in the same way. Or even better an unpickler utility can be made within `utils`).

## Development

### Python Environment

Development of this package can occur within the root virtual environment. See the root README for instructions on Python environment setup.

> Note: There is a bug with Jupyter in Python 3.6.0 so a different Python version is recommended.

### Packages

To install the package's dependencies, ensure your virtual environment is activated and run
```shell script
pip install -r training/requirements.txt
```

Additionally, ensure the NLTK resources are installed using
```python
import nltk
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")
```

### Notebooks

#### Local Jupyter Lab

Ensure the dependencies have been installed and run `jupyter lab` to begin notebook development. This should open a tab in your browser with the [Jupyter Lab](https://jupyterlab.readthedocs.io/en/stable/) environment.

##### Cool Plugins

- [Shortcut UI](https://github.com/jupyterlab/jupyterlab-shortcutui/)
- [Table of Contents](https://github.com/jupyterlab/jupyterlab-toc)
- [Collapsible Headings](https://github.com/aquirdTurtle/Collapsible_Headings)
- Vim
    - [Keybindings](https://github.com/jwkvam/jupyterlab_vim)
    - [System clipboard support](https://github.com/ianhi/jupyterlab_vim-system-clipboard-support)
- [Language Server Protocol](https://github.com/krassowski/jupyterlab-lsp)
    - Note that some packages mentioned in the setup for this plugin are likely already installed from `requirements.txt`.
- Themes can also be installed

#### Google Colab

`.ipynb` can be uploaded to Colab for development. Notebooks should support development in Google Colab without modification to the existing code, refer to the instructions within the notebooks for more details.

> `training/description_classification/report_description_classification.ipynb` can be used as a sample for implementing conditional Colab support.

When finished development, download the notebook as `.ipynb` to a suitable folder within `training`. Also download any model outputs to the `model_output` folder. Before committing ensure the code is formatted.

#### PyCharm

PyCharm professional can also be used for notebook development. This can be useful as debugging is likely to be easier to setup in PyCharm.

#### Formatting

Python code within notebooks should be formatted regularly. Currently the only known way to do this is within a local Jupyter environment. To format:

> Note that some packages required in the following steps are likely already installed from `requirements.txt`

1. Make sure `black` is installed.
2. Follow [the steps here](https://jupyterlab-code-formatter.readthedocs.io/en/latest/installation.html) to setup the JupyterLab Code Formatter.
3. Update the JupyterLab Code Formatter preferences to set black as the default:
    ```json
    {
        "preferences": {
            "default_formatter": {
                "python": [
                    "black",
                    "isort"
                ]
            }
        }
    }
    ```
4. Click the button in the tool bar or run the command to format with black from the 'Commands' sidebar.

> If developing in Colab run the changed notebooks through the formatter on your local before committing.