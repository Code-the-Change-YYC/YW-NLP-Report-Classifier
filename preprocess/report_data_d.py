from enum import Enum, unique


@unique
class ColName(Enum):
    """Column names of the processed data. To be used for indexing into the
    dataframe."""
    DT_INC = "DATETIME_INCIDENT"
    LOC = "LOCATION"
    LOC_DET = "LOCATION_DETAIL"
    CLI_PRI = "CLIENT_PRIMARY"
    CLI_SEC = "CLIENT_SECONDARY"
    CHI_INV = "CHILD_INVOLVED"
    N_CLI_INV = "NON_CLIENT_INVOLVED"
    PRO = "PROGRAM"
    CFS = "CFS"
    EMS = "EMS"
    FIRE = "FIRE"
    MISC_SERV_F = "MISC_SERVICE_FLAG"
    DOAP_PACT = "DOAP_PACT"
    POLICE = "POLICE"
    MISC_SERV = "MISC_SERVICE"
    INC_T1 = "INCIDENT_TYPE_1"
    INC_T2 = "INCIDENT_TYPE_2"
    """Inaccessible after pre-processing"""
    INC_T1_OLD = "INCIDENT_1_OLD"
    """Inaccessible after pre-processing"""
    INC_T2_OLD = "INCIDENT_TYPE_OTHER"
    DESC = "DESCRIPTION"
    RES_CHI_WF = "RESPONSE_CHILD_WELFARE"
    RES_EV = "RESPONSE_EVAC"
    RES_FA = "RESPONSE_FIRST_AID"
    RES_IPP = "RESPONSE_INFECTION_PREVENTION_PROTOCOL"
    RES_MA = "RESPONSE_MENTAL_ASSESSMENT"
    RES_N = "RESPONSE_NALOXONE"
    RES_PB = "RESPONSE_PERSON_BARRED"
    RES_SA = "RESPONSE_SAFETY_ASSESSMENT"
    RES_SP = "RESPONSE_SAFETY_PLANNING"
    RES_O = "RESPONSE_OTHER"
    RES_OD = "RESPONSE_OTHER_DESC"
    DT_WRIT = "DATETIME_WRITTEN"

    def __str__(self):
        """Overridden so that we can use this enum as the value of the
        dataframe's columns and the dataframe will use the enum's member's
        values as the column names when exporting to CSV."""
        return self._value_



