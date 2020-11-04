from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class Form(BaseModel):
    description: str
    client_primary: str
    client_secondary: Optional[str] = None
    location: str
    location_detail: Optional[str] = None
    services_involved: List[str]
    primary_staff_first_name: str
    primary_staff_last_name: str
    occurence_time: datetime
    incident_type_primary: str
    incident_type_secondary: Optional[str] = None
    child_involved: bool
    non_client_involved: bool
    program: str
    immediate_response: List[str]
    staff_name = str
    program_supervisor_reviewer_name = str
    completion_date = datetime

    class Config:
        schema_extra = {
            "example": {
                "description": "Example description from form field.",
                "client_primary": "AB",
                "client_secondary": "DL",
                "location": "yw croydon",
                "location_detail": "Around the corner.",
                "services_involved": ["police", "hospital"],
                "primary_staff_first_name": "John",
                "primary_staff_last_name": "Doe",
                "occurence_time": "2008-09-15T15:53:00+05:00",
                "incident_type_primary": "child abandonment",
                "incident_type_secondary": "injury",
                "child_involved": True,
                "non_client_involved": False,
                "program": "compass",
                "immediate_response": ["evacuation", "mental health assessment"],
                "staff_name": "John man",
                "program_supervisor_reviewer_name": "another john",
                "completion_date": "2008-09-15T15:53:00+05:00",
            }
        }


# NOTE: it's `form_fields` and not `fields` because that's an internal BaseModel variable.
class SubmitIn(BaseModel):
    form_fields: Form


class SubmitOut(BaseModel):
    form_fields: Form
    risk_assessment: str
    redirect_url: str
