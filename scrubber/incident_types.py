from typing import Iterable

import pandas as pd

# clean up the incident type column to restore the proper drop-down options
# set variables for each drop down options

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
    "Public disturbance": client_p,
    "Noise disturbance": client_p,
    # "Client aggression towards property"
    "Damage to property within unit": client_pt,
    #  "Client death (off-site)"
    #  "Client death (on-site)"
    #  "Client death missing"
    # "Concern for welfare of a child"
    "Custodial parent did not pick up child after exchange": concern_c,
    # "COVID-19 Confirmed"
    # "Exposure"
    # "Homicide (Threat or attempt)"
    "Threatening with alleged weapon": hom_t,
    "Domestic violence": hom_t,
    # "Illegal activity on premises"
    # "Injury"
    # "Media/3rd party contact"
    # "Medical emergency"
    "Medical": med_e,
    "Client health risk": med_e,
    "Drug overdose": med_e,
    "Health concern": med_e,
    "Health corcern": med_e,
    "High intoxication, ems call.": med_e,
    "Hospital trip": med_e,
    "Medical emergecny": med_e,
    "Medical emergency (overdose)": med_e,
    "Medical health emergency": med_e,
    "Seizure/ anxiety attack": med_e,
    "Overdose": med_e,
    "Medical Concern": med_e,
    "Medical Emergecny": med_e,
    "Medical concern": med_e,

    # "Mental health emergency"
    "Potential overdose": men_he,
    "Excessive use of medication": men_he,

    # "Other"
    "Positive incident involving cps": otr,
    "Small fire on stove top": otr,
    "Fire": otr,
    "Od": otr,

    # "Security concern"
    "Removal of barred guest": secur_c,
    "Unwanted man at door refused to leave property": secur_c,
    "Property damage": secur_c,

    # "Suicide attempt"
    "Client at-risk of suicide": suicide_c,

    # "Suspected or actual breach of privacy"
    # "Suspicion/allegation of abuse towards or against client"
    # "Suspicion/allegation of child abuse - child is a not a client"
}

inc_type_col_names = ("INCIDENT_1_OLD", "INCIDENT_TYPE_OTHER", "INCIDENT_TYPE_1", "INCIDENT_TYPE_2")


def normalize_inc_type(col: pd.Series) -> pd.Series:
    return col.str.strip().str.capitalize()


def preprocess(report_data: pd.DataFrame, col_names: Iterable = inc_type_col_names):
    """Normalize and apply corrections to the incident type columns.

    :param report_data: Report data read from CSV. Modifies this value.
    :param col_names: The names of the incident type columns to preprocess
    """
    for col_name in col_names:
        report_data[col_name] = normalize_inc_type(report_data[col_name])
        report_data[col_name].replace(_t_replace_dict, inplace=True)
