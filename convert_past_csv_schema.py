import pandas as pd
from server.connection import collection
import json

past_data = pd.read_csv("data-past.csv", encoding="iso-8859-1")

rename_columns = {
    "Form - Date and time of Occurrence": "occurrence_time",
    "Form - Location of Incident": "location",
    "Form - Location Detail": "location_detail",
    "Form - Did this incident involve a child?": "child_involved",
    "Form - Did this incident involve a non-client guest?": "non_client_involved",
    "Form - Program": "program",
    "Form - Incident Type (Primary)": "incident_type_primary",
    "Form - Incident Type (Secondary)": "incident_type_secondary",
    "Form - DESCRIPTION OF INCIDENT Provide a brief, precise description of the actual incident, including timelines. (500 character max.)": "description",
    "Form - Other Services Involved (if other)": "services_involved_other",
    "Form - Completed On": "completion_date",
    "Form - Client Involved - Primary (initials)": "client_primary",
    "Form - Client Involved - Secondary (initials)": "client_secondary",
    "Form - Other Services Involved (select all that apply) - Child Walfare (CFS)": "child welfare (cfs)",
    "Form - Other Services Involved (select all that apply) - EMS": "ems",
    "Form - Other Services Involved (select all that apply) - Fire": "fire",
    "Form - Other Services Involved (select all that apply) - Other": "other",
    "Form - Other Services Involved (select all that apply) - Outreach (DOAP/PACT)": "outreach (doap/pact)",
    "Form - Other Services Involved (select all that apply) - Police": "police",
    "Form - What was the immediate response to the incident? Select all that apply - Called Child Welfare": "called child welfare",
    "Form - What was the immediate response to the incident? Select all that apply - Evacution": "evacuation",
    "Form - What was the immediate response to the incident? Select all that apply - First-aid provided": "first-aid provided",
    "Form - What was the immediate response to the incident? Select all that apply - Infection prevention protocol": "infection prevention protocol",
    "Form - What was the immediate response to the incident? Select all that apply - Mental health assessment": "mental health assessment",
    "Form - What was the immediate response to the incident? Select all that apply - Naloxone administered": "naloxone administered",
    "Form - What was the immediate response to the incident? Select all that apply - Person barred/access restricted": "person barred/access restricted",
    "Form - What was the immediate response to the incident? Select all that apply - Safety assessment": "safety assessment",
    "Form - What was the immediate response to the incident? Select all that apply - Safety Planning": "safety Planning",
    "Form - What was the immediate response to the incident? Select all that apply - Other": "other"


}

#   "Form - Client Involved - Primary (initials)"
#     "Form - Client Involved - Secondary (initials)" both need to combine to incident_type_primary and secondary

# add columns not in old schema
past_data["staff_name"] = ""
past_data["primary_staff_first_name"] = ""
past_data["primary_staff_last_name"] = ""
past_data["program_supervisor_reviewer_name"] = ""


past_data["services_involved"] = [list() for x in range(len(past_data.index))]
past_data["immediate_response"] = [list() for x in range(len(past_data.index))]

past_data.rename(columns=rename_columns, inplace=True)

past_data.drop(columns="Form - Specify Other Response", inplace=True)

old_otherServices_st_index = 8
new_otherSverices_ed_index = 14
for i in range(old_otherServices_st_index, new_otherSverices_ed_index+1):
    for j, entry in enumerate(past_data[past_data.columns[i]]):
        if(entry == 1):
            past_data["services_involved"][j].append(past_data.columns[i])

old_response_st_index = 20
old_response_ed_index = 29
for i in range(old_response_st_index, old_response_ed_index+1):
    for j, entry in enumerate(past_data[past_data.columns[i]]):
        if(entry == 1):
            past_data["immediate_response"][j].append(past_data.columns[i])

colums_to_drop_1 = past_data.iloc[:,
                                  old_otherServices_st_index:new_otherSverices_ed_index].columns
colums_to_drop_2 = past_data.iloc[:,
                                  old_response_st_index:old_response_ed_index].columns

past_data.drop(columns=colums_to_drop_1, inplace=True)
past_data.drop(columns=colums_to_drop_2, inplace=True)


# deal with Form - Primary Incident Type and Form - Secondary Incident Type


for i, entry in enumerate(past_data["incident_type_primary"].isnull()):
    if(entry):
        past_data["incident_type_primary"][i] = past_data["Form - Primary Incident Type"][i]

for i, entry in enumerate(past_data["incident_type_secondary"].isnull()):
    if(entry):
        past_data["incident_type_secondary"][i] = past_data["Form - Secondary Incident Type"][i]


past_data.drop(columns=["Form - Primary Incident Type",
                        "Form - Secondary Incident Type"], inplace=True)

past_data[["child_involved", "non_client_involved"]] = past_data[[
    "child_involved", "non_client_involved"]].replace({"Yes": True, "No": False})

past_data = past_data[["description",
                       "client_primary",
                       "client_secondary",
                       "location",
                       "location_detail",
                       "services_involved",
                       "services_involved_other",
                       "primary_staff_first_name",
                       "primary_staff_last_name",
                       "occurrence_time",
                       "incident_type_primary",
                       "incident_type_secondary",
                       "child_involved",
                       "non_client_involved",
                       "program",
                       "immediate_response",
                       "staff_name",
                       "program_supervisor_reviewer_name",
                       "completion_date"]]

past_data.reset_index(drop=True, inplace=True)
records = json.loads(past_data.T.to_json()).values()
collection.insert_many(records)
