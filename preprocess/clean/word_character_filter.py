from preprocess.preprocessor import Preprocessor

import pandas as pd
import re
from preprocess.report_data_d import _ColName


class WordCharacterFilter(Preprocessor):

    def process(self, report_data: pd.DataFrame) -> pd.DataFrame:
        """Apply a pre-processing step to report_data.

        :param report_data: Data to be processed. NOTE: This method can modify
        this value.
        :return: The filtered data devoid of non-word characters, including punctuation. There is a special
        exception with the "*" character for spacy.io scrubbing purposes, and "{", "}" for scrubadub and token purposes.
        """
        descriptions = report_data[_ColName.DESC]
        filtered_descriptions = []
        # loop to lemmatize
        for description in descriptions:
            # tokenize to check if each word is already a transformed item
            tokens = description.split()

            for i, token in enumerate(tokens):
                # special token defined by anything between "{{" and "}}"
                match_special_token = re.match(r"{{.*}}", token)
                # check if transformed item
                if not match_special_token:
                    # filter out all non-word characters and underscores, excluding "*", "{", "}"
                    tokens[i] = re.sub(r"([^\w *]|_)", "", token)
                else:
                    # strip special token
                    first, last = match_special_token.start(), match_special_token.end()
                    tokens[i] = token[first:last]

            filtered_descriptions.append(" ".join(tokens))

        report_data[_ColName.DESC] = filtered_descriptions
        return report_data
