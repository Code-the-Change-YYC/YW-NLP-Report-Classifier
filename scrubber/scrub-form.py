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
report_data = pd.read_csv("data-sensitive.csv",encoding = "ISO-8859-1")

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

#clean up the incident type column to restore the proper drop-down options 
# below is the record for replacement, e.g. x:y replace x with y
_t_replace_dict = {
    # "child abandonment"
    # "Client aggression towards another person"
    "Public Disturbance" :   "Client aggression towards another person",
    "Noise Disturbance"  :   "Client aggression towards another person",
    # "Client aggression towards property"
    "Damage to property within unit" :"Client aggression towards property",
    #  "Client death (offsite)"
    #  "Client death (onsite)"
    #  "Client death missing"
    # "Concern for welfare of a child"
    "Custodial parent did not pick up child after exchange" : "Concern for welfare of a child",
    # "COVID-19 Confirmed"
    # "Exposure"
    # "Homicde (Threat or attempt)"
    "Threatening with alleged weapon"   : "Homicde (Threat or attempt)",
    "Domestic violence"   : "Homicde (Threat or attempt)",
    # "Illegal activity on premises"
    # "Injury"
    # "Media/3rd party contact"
    # "Medical emergency"
    "Medical": "Medical emergency",
    "Client Health Risk"           : "Medical emergency",
    "drug overdose"                : "Medical emergency",
    "Health Concern"               : "Medical emergency",
    "health concern"               : "Medical emergency",
    "Health Corcern"               : "Medical emergency",
    "High Intoxication, EMS call." : "Medical emergency",
    "Hospital Trip"                : "Medical emergency",
    "Medical Emergency"            : "Medical emergency",
    "Medical Emergency (Overdose)" : "Medical emergency",
    "overdose"                     : "Medical emergency",
    "Medical Health Emergency"     : "Medical emergency",
    "Seizure/ anxiety attack"      : "Medical emergency",
    "Overdose"                     : "Medical emergency",
    "Medical Concern"              : "Medical emergency",
    "Medical Emergecny"            : "Medical emergency",
    "Medical concern"              : "Medical emergency", 
     
     # "Mental health emergency"
     "Potential overdose"          : "Mental health emergency",
     "Excessive use of medication" : "Mental health emergency",
    
    # "Other"
    "Positive incident involving CPS" : "Other",
    "Small Fire on stove top" : "Other",
    "fire" : "Other",
    "Fire" : "Other",
    "OD"   : "Other",

    # "Security concern"
    "Removal of Barred Guest" : "Security concern",
    "Unwanted man at door refused to leave property" : "Security concern",
    "property damage" : "Security concern",
    
    # "Suicide attempt" 
    "Client at-risk of suicide" : "Suicide attempt",

    # "Suspected or actual breach of privacy"
    # "Suspicion/allegation of abuse towards or against client"
    # "Suspicion/allegation of child abuse - child is a not a client"
    }


#clean each columns :  "INCIDENT_1_OLD","INCIDENT_TYPE_OTHER"

report_data["INCIDENT_1_OLD"].replace(_t_replace_dict, inplace = True)
report_data["INCIDENT_TYPE_OTHER"].replace(_t_replace_dict, inplace = True)




# create new .csv file with scrubbed data
report_data.to_csv("data_scrubbed.csv", index=False)
