from typing import Iterable

import pandas as pd

# clean up the incident type column to restore the proper drop-down options
# set variables for each drop down options
from preprocessor import Preprocessor
from report_data_d import ColNames

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


def normalize_inc_type(col: pd.Series) -> pd.Series:
    return col.str.strip().str.capitalize()


def merge_columns(report_data: pd.DataFrame) -> pd.DataFrame:
    pd.set_option('display.max_columns', None)
    # create new column and add to end of DataFrame
    report_data[ColNames.INC_T1] = report_data[ColNames.INC_T1_OLD].fillna(
        '') + report_data[ColNames.INC_T1].fillna('')
    # preprocess, replace nan with empty string
    report_data[ColNames.INC_T2] = report_data[ColNames.INC_T2].fillna('')
    # for "Other" 2nd types, set to description instead of "Other"
    report_data[ColNames.INC_T2] = report_data.apply(
        lambda r: (r[ColNames.INC_OTHER] if r[ColNames.INC_T2].lower() == 'other'
                   else r[ColNames.INC_T2]),
        axis=1)

    # make blank if matching first incident type
    report_data[ColNames.INC_T2] = report_data.apply(
        lambda r: (r[ColNames.INC_T2] if r[ColNames.INC_T1] != r[ColNames.INC_T2] else ''),
        axis=1)

    # remove old columns
    return report_data[[col for col in report_data if col not in [ColNames.INC_T1_OLD, ColNames.INC_OTHER]]]


class IncidentTypesProcessor(Preprocessor):
    """Normalize and apply corrections to the incident type columns."""

    col_names: Iterable[str] = {
        ColNames.INC_T1,
        ColNames.INC_T1_OLD,
        ColNames.INC_T2,
        ColNames.INC_OTHER,
    }

    def __init__(self, col_names: Iterable[str] = None):
        """
        :param col_names: The names of the incident type columns to process
        """
        if col_names is not None:
            self.col_names = col_names

    def process(self, report_data: pd.DataFrame) -> pd.DataFrame:
        for col_name in self.col_names:
            report_data[col_name] = normalize_inc_type(report_data[col_name])
            report_data[col_name].replace(_t_replace_dict, inplace=True)

        return merge_columns(report_data)
