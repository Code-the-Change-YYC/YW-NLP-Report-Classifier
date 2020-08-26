from enum import Enum
from typing import Dict


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
    ABU_CHI = "Suspicion/allegation of child abuse - child is not a client"
    ABU_CLI = "Suspicion/allegation of abuse towards or against client"
    PRI_BRE = "Suspected or actual breach of privacy"
    MEDIA = "Media/3rd party contact"
    INJURY = "Injury"
    ILLEGAL = "Illegal activity on premises"
    EXPOSURE = "Exposure"
    COVID = "COVID-19 Confirmed"
    REF_ISO_COVID = "Refusal to isolate for covid-19"
    MISSING = "Client missing"
    DEATH_ONSITE = "Client death (onsite)"
    DEATH_OFFSITE = "Client death (offsite)"
    CHI_ABD = "Child abandonment"


# below is the record for replacement, e.g. x:y replace x with y
replacements: Dict[str, str] = {
    # "child abandonment"
    # "Client aggression towards another person"
    "Public disturbance": IncidentType.CLIENT_P.value,
    "Noise disturbance": IncidentType.CLIENT_P.value,
    # "Client aggression towards property"
    "Damage to property within unit": IncidentType.CLIENT_PT.value,
    #  "Client death (off-site)"
    #  "Client death (on-site)"
    #  "Client death missing"
    # "Concern for welfare of a child"
    "Custodial parent did not pick up child after exchange": IncidentType.CONCERN_C.value,
    # "COVID-19 Confirmed"
    # "Exposure"
    # "Homicide (Threat or attempt)"
    "Threatening with alleged weapon": IncidentType.HOM_T.value,
    "Domestic violence": IncidentType.HOM_T.value,
    # "Illegal activity on premises"
    # "Injury"
    # "Media/3rd party contact"
    # "Medical emergency"
    "Medical": IncidentType.MED_E.value,
    "Client health risk": IncidentType.MED_E.value,
    "Drug overdose": IncidentType.MED_E.value,
    "Health concern": IncidentType.MED_E.value,
    "Health corcern": IncidentType.MED_E.value,
    "High intoxication, ems call.": IncidentType.MED_E.value,
    "Hospital trip": IncidentType.MED_E.value,
    "Medical emergecny": IncidentType.MED_E.value,
    "Medical emergency (overdose)": IncidentType.MED_E.value,
    "Medical health emergency": IncidentType.MED_E.value,
    "Seizure/ anxiety attack": IncidentType.MED_E.value,
    "Overdose": IncidentType.MED_E.value,
    "Medical Concern": IncidentType.MED_E.value,
    "Medical Emergecny": IncidentType.MED_E.value,
    "Medical concern": IncidentType.MED_E.value,

    # "Mental health emergency"
    "Potential overdose": IncidentType.MEN_HE.value,
    "Excessive use of medication": IncidentType.MEN_HE.value,

    # "Other"
    "Positive incident involving cps": IncidentType.OTR.value,
    "Small fire on stove top": IncidentType.OTR.value,
    "Fire": IncidentType.OTR.value,
    "Od": IncidentType.OTR.value,

    # "Security concern"
    "Removal of barred guest": IncidentType.SECUR_C.value,
    "Unwanted man at door refused to leave property": IncidentType.SECUR_C.value,
    "Property damage": IncidentType.SECUR_C.value,

    # "Suicide attempt"
    "Client at-risk of suicide": IncidentType.SUICIDE_C.value,

    # "Suspected or actual breach of privacy"
    # "Suspicion/allegation of abuse towards or against client"
    # "Suspicion/allegation of child abuse - child is a not a client"
}
