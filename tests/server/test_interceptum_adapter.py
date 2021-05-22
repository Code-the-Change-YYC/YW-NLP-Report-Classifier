from unittest import TestCase, main
from server.interceptum_adapter import InterceptumAdapter

with open('tests/server/interceptum-response.xml', 'r') as xml_file:
    xml = xml_file.read()


class TestXmlToFormValues(TestCase):

    def test_mapping(self):
        result = InterceptumAdapter.xml_to_form_values(xml)
        expected = {
            "description": "Example description from form field.",
            "client_primary": "AB",
            "client_secondary": "DL",
            "location": "yw croydon",
            "location_detail": "Around the corner.",
            "services_involved": ["ems", "police"],
            "services_involved_other": "police",
            "primary_staff_first_name": "John",
            "primary_staff_last_name": "Doe",
            "occurrence_time": "2008-09-15T15:53:00+05:00",
            "incident_type_primary": "Child abandonment",
            "incident_type_secondary": "injury",
            "child_involved": True,
            "non_client_involved": False,
            "program": "compass",
            "immediate_response": ["evacuation", "mental health assessment"],
            "staff_name": "John man",
            "program_supervisor_reviewer_name": "another john",
            "completion_date": "2008-09-15T15:53:00+05:00"
        }
        self.assertDictEqual(result, expected)


if __name__ == '__main__':
    main()
