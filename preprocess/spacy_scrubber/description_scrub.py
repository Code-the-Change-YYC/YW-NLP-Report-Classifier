import re
from typing import Optional

import pandas as pd

from preprocessor import Preprocessor
from report_data_d import _ColName
from spacy_scrubber.scrubber import Scrubber


class DescriptionScrubber(Preprocessor):
    """Scrubs out sensitive data from the report's descriptions."""
    ent_replacement: Optional[str]

    def __init__(self, ent_replacement: str = None, **kwargs):
        """
        :param ent_replacement: Optional string to replace entities with. Will
        be replaced with an entity placeholder if not specified.
        """
        super().__init__()
        self.ent_replacement = ent_replacement
        self.client_tokens = set()

    def get_client_tokens(self, client_primary, client_secondary):
        # iterate over client columns and add the names to be scrubbed
        for series in (client_primary, client_secondary):
            for name in series:
                # if typeof name is float, then ignore (empty cells in excel are converted to NaN)
                if isinstance(name, float):
                    continue
                # remove spaces
                no_spaces_name = name.replace(" ", "")
                self.client_tokens.add(no_spaces_name)
                # remove brackets
                no_brackets_name = re.compile("(.*)").sub("", no_spaces_name)
                # remove numbers and spaces
                no_nums_name = re.compile("[ 0-9]").sub("", no_brackets_name)
                self.client_tokens.add(no_nums_name)
                # remove periods
                no_periods_name = no_nums_name.replace(".", "")
                self.client_tokens.add(no_periods_name)

    def process(self, report_data: pd.DataFrame) -> pd.DataFrame:
        self.get_client_tokens(
            report_data[_ColName.CLI_PRI], report_data[_ColName.CLI_SEC])
        scrubber = Scrubber(self.client_tokens,
                            ent_replacement=self.ent_replacement)
        descriptions = report_data[_ColName.DESC]

        # loop to clean
        scrubbed_descriptions = [scrubber.scrub(d) for d in descriptions]

        # update pandas column
        report_data[_ColName.DESC] = scrubbed_descriptions

        return report_data
