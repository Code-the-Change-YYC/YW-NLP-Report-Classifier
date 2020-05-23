from enum import Enum


class IncidentType(Enum):
    """Contains the values of the incident type dropdown"""
    CLIENT_P = "Client aggression towards another person"
    CLIENT_PT = "Client aggression towards property"
    CONCERN_C = "Concern for welfare of a child"
    HOM_T = "Homicide (Threat or attempt)"
    MED_E = "Medical emergency"
    MEN_HE = "Mental health emergency"
    OTR = "Other"
    SECUR_C = "Security concern"
    SUICIDE_C = "Suicide attempt"


# below is the record for replacement, e.g. x:y replace x with y
replacements = {
    # "child abandonment"
    # "Client aggression towards another person"
    "Public disturbance": IncidentType.CLIENT_P,
    "Noise disturbance": IncidentType.CLIENT_P,
    # "Client aggression towards property"
    "Damage to property within unit": IncidentType.CLIENT_PT,
    #  "Client death (off-site)"
    #  "Client death (on-site)"
    #  "Client death missing"
    # "Concern for welfare of a child"
    "Custodial parent did not pick up child after exchange": IncidentType.CONCERN_C,
    # "COVID-19 Confirmed"
    # "Exposure"
    # "Homicide (Threat or attempt)"
    "Threatening with alleged weapon": IncidentType.HOM_T,
    "Domestic violence": IncidentType.HOM_T,
    # "Illegal activity on premises"
    # "Injury"
    # "Media/3rd party contact"
    # "Medical emergency"
    "Medical": IncidentType.MED_E,
    "Client health risk": IncidentType.MED_E,
    "Drug overdose": IncidentType.MED_E,
    "Health concern": IncidentType.MED_E,
    "Health corcern": IncidentType.MED_E,
    "High intoxication, ems call.": IncidentType.MED_E,
    "Hospital trip": IncidentType.MED_E,
    "Medical emergecny": IncidentType.MED_E,
    "Medical emergency (overdose)": IncidentType.MED_E,
    "Medical health emergency": IncidentType.MED_E,
    "Seizure/ anxiety attack": IncidentType.MED_E,
    "Overdose": IncidentType.MED_E,
    "Medical Concern": IncidentType.MED_E,
    "Medical Emergecny": IncidentType.MED_E,
    "Medical concern": IncidentType.MED_E,

    # "Mental health emergency"
    "Potential overdose": IncidentType.MEN_HE,
    "Excessive use of medication": IncidentType.MEN_HE,

    # "Other"
    "Positive incident involving cps": IncidentType.OTR,
    "Small fire on stove top": IncidentType.OTR,
    "Fire": IncidentType.OTR,
    "Od": IncidentType.OTR,

    # "Security concern"
    "Removal of barred guest": IncidentType.SECUR_C,
    "Unwanted man at door refused to leave property": IncidentType.SECUR_C,
    "Property damage": IncidentType.SECUR_C,

    # "Suicide attempt"
    "Client at-risk of suicide": IncidentType.SUICIDE_C,

    # "Suspected or actual breach of privacy"
    # "Suspicion/allegation of abuse towards or against client"
    # "Suspicion/allegation of child abuse - child is a not a client"
}
