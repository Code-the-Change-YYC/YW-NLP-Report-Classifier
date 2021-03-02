from preprocess.preprocessor import Preprocessor

import pandas as pd
import re
from preprocess.report_data_d import _ColName


class Lowercaser(Preprocessor):

    def process(self, report_data: pd.DataFrame) -> pd.DataFrame:
        """Apply a pre-processing step to report_data.

        Params:
            report_data: Data to be processed. NOTE: This method can modify this value.

        Returns:
            The data with lowercased descriptions.

        """
        descriptions = report_data[_ColName.DESC]
        lowercased_descriptions = []
        # loop to lemmatize
        for description in descriptions:
            # tokenize to check if each word is already a transformed item
            tokens = description.split()

            for i, token in enumerate(tokens):
                # special token defined by anything between "{{" and "}}"
                match_special_token = re.match(r"{{.*}}", token)
                # check if transformed item
                if not match_special_token:
                    # lowercase token
                    tokens[i] = token.lower()
                else:
                    # strip special token
                    first, last = match_special_token.start(), match_special_token.end()
                    tokens[i] = token[first:last]

            lowercased_descriptions.append(" ".join(tokens))

        report_data[_ColName.DESC] = lowercased_descriptions
        return report_data
