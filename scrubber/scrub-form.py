# NOTE: The scrubadub library is broken as of Python 3.7, so please downgrade
# to Python 3.6 before using this script. This is noted in the .python-version
# file if you are using pyenv.

import scrubadub
import pandas as pd

# Custom scrubadub logic
# List of words that should remain unscrubbed
# Note: These are converted to lower case anyways
whitelisted_words = ["Staff", "EMS", "Fire", "CPS", "Rockyview", "Rocky",
                     "View", "Health", "Link", "Sheldon", "Gabapentin", "Chumir", "Hospital", "Fentanyl", "Writer"]


class CustomNameDetector(scrubadub.detectors.NameDetector):
    def __init__(self):
        for word in whitelisted_words:
            self.disallowed_nouns.add(word)


# replace default name detector with new name detector that doesn't delete keywords
scrubber = scrubadub.Scrubber()
scrubber.remove_detector("name")
scrubber.add_detector(CustomNameDetector)


# use pandas to get csv description column
report_data = pd.read_csv("data-sensitive.csv")
descriptions = report_data["DESCRIPTION"]

scrubbed_descriptions = []
# loop to clean
for description in descriptions:
    scrubbed_descriptions.append(scrubber.clean(
        description, replace_with="identifier"))

# update pandas column
report_data["DESCRIPTION"] = scrubbed_descriptions

# create new .csv file with scrubbed data
# report_data.to_csv("data_scrubbed.csv")
