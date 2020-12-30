interceptum_boolean_dict = {
    True: "1",
    False: "2",
}

interceptum_services_involved_dict = {
    'child welfare (cfs)': "1",
    'ems': "2",
    'police': "6",
    'fire': "3",
    'outreach (doap/pact)': "5",
    'other': "4",
}

interceptum_location_dict = {
    "yw croydon": "1",
    "yw providence": "2",
    "yw downtown": "3",
    "yw hub": "4",
    "yw sheriff king": "5",
    "in community": "7",
    "yw maple": "8",
}

interceptum_program_dict = {
    'child care (hub)': "1",
    'child support': "10",
    'compass': "2",
    'counselling and personal development': "3",
    'croydon (community housing)': "4",
    'dcrt': "5",
    'drop-in child care': "6",
    'employment resource center': "7",
    'family access': "8",
    'family resource network': "14",
    'intensive case management': "9",
    'linc': "11",
    'mindful moments': "20",
    'outreach counselling': "13",
    'providence (community housing)': "15",
    'sheriff king home': "16",
    'the maple (community housing)': "19",
    'transitional housing': "12",
}

interceptum_incident_type_primary_dict = {
    "child abandonment": "1",
    "client aggression towards another person": "2",
    "client aggression towards property": "3",
    "client death (offsite)": "4",
    "client death (onsite)": "5",
    "client missing": "6",
    "concern for welfare of a child": "7",
    "exposure": "8",
    "homicide (threat or attempt)": "9",
    "illegal activity on premises": "11",
    "injury": "12",
    "media/3rd party contact": "13",
    "medical emergency": "14",
    "mental health emergency": "15",
    "security concern": "16",
    "suicide attempt": "17",
    "suspected or actual breach of privacy": "18",
    "suspicion/allegation of abuse towards or against client": "19",
    "suspicion/allegation of child abuse - child is not a client": "20",
    "other": "21",
    "covid-19 confirmed": "22",
}

interceptum_incident_type_secondary_dict = {
    "child abandonment": "1",
    "client aggression towards another person": "2",
    "client aggression towards property": "3",
    "client death (offsite)": "4",
    "client death (onsite)": "5",
    "client missing": "6",
    "concern for welfare of a child": "7",
    "exposure": "8",
    "homicide (threat or attempt)": "9",
    "other": "10",
    "illegal activity on premises": "11",
    "injury": "12",
    "media/3rd party contact": "13",
    "medical emergency": "14",
    "mental health emergency": "15",
    "security concern": "16",
    "suicide attempt": "17",
    "suspected or actual breach of privacy": "18",
    "suspicion/allegation of abuse towards or against client": "19",
    "suspicion/allegation of child abuse - child is not a client": "20",
}

interceptum_immediate_response_dict = {
    "called child welfare": "1",
    "evacution": "2",
    "first-aid provided": "3",
    "infection prevention protocol": "4",
    "mental health assessment": "5",
    "naloxone administered": "10",
    "person barred/access restricted": "6",
    "safety assessment": "7",
    "safety planning": "8",
    "other": "9",
}

field_values_dict = {
    "description": "447832",
    "client_primary": "447821",
    "client_secondary": "447822",
    "location": "447817",
    "location_detail": "447818",
    "services_involved": "447826",
    "services_involved_other": "447827",
    "primary_staff_first_name": "447819",
    "primary_staff_last_name": "447820",
    "occurence_time": "447816",
    "incident_type_primary": "447828",
    "incident_type_secondary": "447829",
    "child_involved": "447823",
    "non_client_involved": "447824",
    "program": "447825",
    "immediate_response": "447833",
    "staff_name": "447836",
    "program_supervisor_reviewer_name": "447838",
    "completion_date": "447835",
}

multi_options = {
    "services_involved": interceptum_services_involved_dict,
    "immediate_response": interceptum_immediate_response_dict,
}

single_option = {
    "location": interceptum_location_dict,
    "incident_type_primary": interceptum_incident_type_primary_dict,
    "incident_type_secondary": interceptum_incident_type_secondary_dict,
    "program": interceptum_program_dict,
}
