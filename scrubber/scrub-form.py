# NOTE: The scrubadub library is broken as of Python 3.7, so please downgrade
# to Python 3.6 before using this script. This is noted in the .python-version
# file if you are using pyenv.

import pandas as pd
import scrubadub

from scrubber import incident_types

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
report_data = pd.read_csv("data-sensitive.csv", encoding="ISO-8859-1")

# rename columns by index
report_data.columns = ["DATETIME_INCIDENT", "LOCATION", "LOCATION_DETAIL",
                       "CLIENT_PRIMARY", "CLIENT_SECONDARY", "CHILD_INVOLVED",
                       "NON_CLIENT_INVOLVED", "PROGRAM", "CFS", "EMS", "FIRE",
                       "MISC_SERVICE_FLAG", "DOAP_PACT", "POLICE", "MISC_SERVICE",
                       "INCIDENT_TYPE_1", "INCIDENT_TYPE_2", "INCIDENT_1_OLD",
                       "INCIDENT_TYPE_OTHER", "DESCRIPTION", "RESPONSE_CHILD_WELFARE",
                       "RESPONSE_EVAC", "RESPONSE_FIRST_AID", "RESPONSE_INFECTION_PREVENTION_PROTOCOL",
                       "RESPONSE_MENTAL_ASSESSMENT", "RESPONSE_NALOXONE",
                       "RESPONSE_PERSON_BARRED", "RESPONSE_SAFETY_ASSESSMENT",
                       "RESPONSE_SAFETY_PLANNING", "RESPONSE_OTHER", "RESPONSE_OTHER_DESC",
                       "DATETIME_WRITTEN"]

descriptions = report_data["DESCRIPTION"]

scrubbed_descriptions = []
# loop to clean
for description in descriptions:
    scrubbed_descriptions.append(scrubber.clean(
        description, replace_with="identifier"))

# update pandas column
report_data["DESCRIPTION"] = scrubbed_descriptions

incident_types.preprocess(report_data)

# create new .csv file with scrubbed data
report_data.to_csv("data_scrubbed.csv", index=False)
