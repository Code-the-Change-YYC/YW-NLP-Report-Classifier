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

# options here for clean some white space and set all first letter of each sentence to be capped to reduce duplicate efforts in _t_replace_dict
report_data["INCIDENT_1_OLD"] = report_data["INCIDENT_1_OLD"].str.strip()
report_data["INCIDENT_TYPE_OTHER"] = report_data["INCIDENT_TYPE_OTHER"].str.strip()
report_data["INCIDENT_1_OLD"] = report_data["INCIDENT_1_OLD"].str.capitalize()
report_data["INCIDENT_TYPE_OTHER"] = report_data["INCIDENT_TYPE_OTHER"].str.capitalize()



#clean up the incident type column to restore the proper drop-down options 
# set varaibles for each drop down options 

client_p = "Client aggression towards another person"
client_pt = "Client aggression towards property"
concern_c = "Concern for welfare of a child"
hom_t = "Homicide (Threat or attempt)"
med_e = "Medical emergency"
men_he = "Mental health emergency"
otr = "Other"
secur_c = "Security concern"
suicide_c = "Suicide attempt"



# below is the record for replacement, e.g. x:y replace x with y

_t_replace_dict = {
    # "child abandonment"
    # "Client aggression towards another person"
    "Public disturbance" :   client_p,
    "Noise disturbance"  :   client_p,
    # "Client aggression towards property"
    "Damage to property within unit" : client_pt,
    #  "Client death (offsite)"
    #  "Client death (onsite)"
    #  "Client death missing"
    # "Concern for welfare of a child"
    "Custodial parent did not pick up child after exchange" : concern_c,
    # "COVID-19 Confirmed"
    # "Exposure"
    # "Homicide (Threat or attempt)"
    "Threatening with alleged weapon"   : hom_t,
    "Domestic violence"   : hom_t,
    # "Illegal activity on premises"
    # "Injury"
    # "Media/3rd party contact"
    # "Medical emergency"
    "Medical": med_e,
    "Client health risk"           : med_e,
    "Drug overdose"                : med_e,
    "Health concern"               : med_e,
    "Health corcern"               : med_e,
    "High intoxication, ems call." : med_e,
    "Hospital trip"                : med_e,
    "Medical emergecny"            : med_e,
    "Medical emergency (overdose)" : med_e,
    "Medical health emergency"     : med_e,
    "Seizure/ anxiety attack"      : med_e,
    "Overdose"                     : med_e,
    "Medical Concern"              : med_e,
    "Medical Emergecny"            : med_e,
    "Medical concern"              : med_e, 
     
     # "Mental health emergency"
     "Potential overdose"          : men_he,
     "Excessive use of medication" : men_he,
    
    # "Other"
    "Positive incident involving cps" : otr,
    "Small fire on stove top" : otr,
    "Fire" : otr,
    "Od"   : otr,

    # "Security concern"
    "Removal of barred guest" : secur_c,
    "Unwanted man at door refused to leave property" : secur_c,
    "Property damage" : secur_c,
    
    # "Suicide attempt" 
    "Client at-risk of suicide" : suicide_c,

    # "Suspected or actual breach of privacy"
    # "Suspicion/allegation of abuse towards or against client"
    # "Suspicion/allegation of child abuse - child is a not a client"
    }


 #clean each columns :  "INCIDENT_1_OLD","INCIDENT_TYPE_OTHER"

report_data["INCIDENT_1_OLD"].replace(_t_replace_dict, inplace = True)
report_data["INCIDENT_TYPE_OTHER"].replace(_t_replace_dict, inplace = True)




# create new .csv file with scrubbed data
report_data.to_csv("data_scrubbed.csv", index=False)
