import re

import pandas as pd


def clean_scrubadub_entities(series: pd.Series, replace_word: str = "someone"):
    """Replace one or more characters excluding curly braces that is/are contained
    within 2 pairs of curly braces, followed by zero or one alpha-numeric
    character.

    Exclusion of inner curly braces is required so that on lines with
    more than one entity, the entire space between the first and the last entity
    is not matched.
    Optional alpha numeric is a temporary fix for strings like CPS which should
    have been ignored in preprocessing but instead have their first two letters
    replaced with a scrubadub entity.
    """
    return [re.sub(r"\{\{[^{}]+\}\}\w?", replace_word, s) for s in series]
