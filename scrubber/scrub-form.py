# NOTE: The scrubadub library is broken as of Python 3.7, so please downgrade
# to Python 3.6 before using this script. This is noted in the .python-version
# file if you are using pyenv.

import scrubadub
import pandas as pd
import re
import math
from scrubadub.detectors.base import RegexDetector
from scrubadub.filth import RegexFilth


# Custom scrubadub logic
# List of words that should remain unscrubbed
# Note: These are converted to lower case anyways

whitelisted_words = [
    "Staff",
    "EMS",
    "Fire",
    "CPS",
    "Rockyview",
    "Rocky",
    "View",
    "Health",
    "Link",
    "Sheldon",
    "Gabapentin",
    "Chumir",
    "Hospital",
    "Fentanyl",
    "Writer",
    "Crystal",
    "Meth",
    "Overdose",
    "Police",
    "Client",
    "First",
    "Aid",
    "Providence",
]


class CustomNameDetector(scrubadub.detectors.NameDetector):
    """Detector that will run through descriptions and detect sensitive data such as names. 


    Upon initialization loops through whitelisted words to append to disallowed nouns, so non-sensitive data 
    isn't unnecesarily scrubbed.
    """

    def __init__(self):
        for word in whitelisted_words:
            self.disallowed_nouns.add(word)


class InitialsFilth(RegexFilth):
    """Classifies filth for InitialsDetector using regex.

    Will classify sequence of 2 capital letters as filth, excluding AM and PM.
    """

    regex = re.compile(
        r"\b(?!AM|PM|EMS|CPS)[A-Z]\.?[A-Z]'?[A-Z]?\.?( ?\d+?[a-z]?)?\b"
    )  # Excluding AM or PM, sequence that starts with 2 capital letters.
    type = "Initials"


class InitialsDetector(RegexDetector):
    """Utilizes InitialsFilth to detect filth.

    Additional detector added to scrubber to scrub initials.
    """

    filth_cls = InitialsFilth


# replace default name detector with new name detector that doesn't delete keywords
scrubber = scrubadub.Scrubber()
scrubber.remove_detector("name")
scrubber.add_detector(CustomNameDetector)
scrubber.add_detector(InitialsDetector)


# use pandas to get csv description column
report_data = pd.read_csv("data-sensitive.csv")

# rename columns by index
report_data.columns = [
    "DATETIME_INCIDENT",
    "LOCATION",
    "LOCATION_DETAIL",
    "CLIENT_PRIMARY",
    "CLIENT_SECONDARY",
    "CHILD_INVOLVED",
    "NON_CLIENT_INVOLVED",
    "PROGRAM",
    "CFS",
    "EMS",
    "FIRE",
    "MISC_SERVICE_FLAG",
    "DOAP_PACT",
    "POLICE",
    "MISC_SERVICE",
    "INCIDENT_TYPE_1",
    "INCIDENT_TYPE_2",
    "INCIDENT_1_OLD",
    "INCIDENT_TYPE_OTHER",
    "DESCRIPTION",
    "RESPONSE_CHILD_WELFARE",
    "RESPONSE_EVAC",
    "RESPONSE_FIRST_AID",
    "RESPONSE_INFECTION_PREVENTION_PROTOCOL",
    "RESPONSE_MENTAL_ASSESSMENT",
    "RESPONSE_NALOXONE",
    "RESPONSE_PERSON_BARRED",
    "RESPONSE_SAFETY_ASSESSMENT",
    "RESPONSE_SAFETY_PLANNING",
    "RESPONSE_OTHER",
    "RESPONSE_OTHER_DESC",
    "DATETIME_WRITTEN",
]

descriptions = report_data["DESCRIPTION"]
client_1 = report_data["CLIENT_PRIMARY"]
client_2 = report_data["CLIENT_SECONDARY"]

scrubbed_descriptions = []
scrubbed_client_1 = []
scrubbed_client_2 = []
# loop to clean
for description in descriptions:
    scrubbed_descriptions.append(scrubber.clean(
        description, replace_with="identifier"))

# some names still remain in the client columns, so we still run both name and initial detectors

for client in client_1:
    updated_text = scrubber.clean(
        client, replace_with="identifier") if client and isinstance(client, str) else ""
    scrubbed_client_1.append(updated_text)

for client in client_2:
    updated_text = scrubber.clean(
        client, replace_with="identifier") if client and isinstance(client, str) else ""
    scrubbed_client_2.append(updated_text)

# update pandas column
report_data["DESCRIPTION"] = scrubbed_descriptions
report_data["CLIENT_PRIMARY"] = scrubbed_client_1
report_data["CLIENT_SECONDARY"] = scrubbed_client_2

# create new .csv file with scrubbed data
report_data.to_csv("data_scrubbed.csv", index=False)
