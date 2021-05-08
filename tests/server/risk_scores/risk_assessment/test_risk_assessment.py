from server.risk_scores.risk_assessment import get_current_risk_score
from unittest import TestCase, main
from unittest.mock import patch
from server.schemas.submit import Form

mock_program_to_risk_map = {
    'child care (hub)': 5,
    'child support': 5,
    'compass': 1,
    'counselling and personal development': 1,
    'croydon (community housing)': 4,
    'dcrt': 3,
    'drop-in child care': 3,
    'employment resource center': 1,
    'family access': 2,
    'family resource network': 3,
    'intensive case management': 5,
    'linc': 2,
    'mindful moments': 4,
    'outreach counselling': 3,
    'providence (community housing)': 4,
    'sheriff king home': 1,
    'the maple (community housing)': 4,
    'transitional housing': 1
}
mock_incident_type_to_risk_map = {
    'client aggression towards another person': 3,
    'client aggression towards property': 3,
    'concern for welfare of a child': 4,
    'homicide (threat or attempt)': 6,
    'medical emergency': 2,
    'mental health emergency': 2,
    'other': 1,
    'security concern': 1,
    'suicide attempt': 6,
    'suspicion/allegation of child abuse - child is not a client': 5,
    'suspicion/allegation of abuse towards or against client': 5,
    'suspected or actual breach of privacy': 3,
    'media/3rd party contact': 1,
    'injury': 1,
    'illegal activity on premises': 6,
    'exposure': 1,
    'covid-19 confirmed': 5,
    'refusal to isolate for covid-19': 3,
    'client missing': 3,
    'client death (onsite)': 1,
    'client death (offsite)': 1,
    'child abandonment': 3
}
mock_response_to_risk_map = {
    'called child welfare': 5,
    'evacuation': 4,
    'first-aid provided': 3,
    'infection prevention protocol': 2,
    'mental health assessment': 5,
    'naloxone administered': 6,
    'person barred/access restricted': 2,
    'safety assessment': 4,
    'safety planning': 3,
    'other': 2
}
mock_occurrence_time_to_risk_map = {
    'morning': 1,
    'afternoon': 2,
    'evening': 3,
    'night': 4
}


@patch.dict('server.risk_scores.risk_scores.program_to_risk_map._risk_score_map', mock_program_to_risk_map)
@patch.dict('server.risk_scores.risk_scores.incident_type_to_risk_map._risk_score_map', mock_incident_type_to_risk_map)
@patch.dict('server.risk_scores.risk_scores.response_to_risk_map._risk_score_map', mock_response_to_risk_map)
@patch.dict('server.risk_scores.risk_scores.occurrence_time_to_risk_map._risk_score_map', mock_occurrence_time_to_risk_map)
class TestRiskAssessment(TestCase):
    def test_risk_assessment_sample(self):
        mock_form = Form(**{
            "description": "Example description from form field.",
            "client_primary": "AB",
            "client_secondary": "DL",
            "location": "yw croydon",
            "location_detail": "Around the corner.",
            "services_involved": ["police", "hospital"],
            "services_involved_other": "police",
            "primary_staff_first_name": "John",
            "primary_staff_last_name": "Doe",
            "occurrence_time": "2008-09-15T15:53:00+05:00",
            "incident_type_primary": "child abandonment",
            "incident_type_secondary": "injury",
            "child_involved": True,
            "non_client_involved": False,
            "program": "compass",
            "immediate_response": ["evacuation", "mental health assessment"],
            "staff_name": "John man",
            "program_supervisor_reviewer_name": "another john",
            "completion_date": "2008-09-15T15:53:00+05:00"
        })
        risk_score = get_current_risk_score(mock_form)
        self.assertAlmostEqual(risk_score, 0.48, places=2)

    def test_risk_assessment_drug_related_three_services(self):
        mock_form = Form(**{
            "description": "At 4:08am staff did a safety check on TL. No answer, so staff entered the unit. Found TL hunched over and breathing laboured and erratically about once every 30-45 seconds. Staff called for assistance. Upon arrival of team member staff was informed to call 911. EMS arrived 4:15am, Nar can was administered, secondary EMS called in by EMS for guest who was convulsing. Fire/Police arrived. Fire carried TL to EMS vehicle. TL and guest taken to unknown hospital in separate vehicle.",
            "client_primary": "TL",
            "client_secondary": "",
            "location": "yw providence",
            "location_detail": "Unit 201",
            "services_involved": ["hospital", "fire", "ems"],
            "services_involved_other": "police",
            "primary_staff_first_name": "",
            "primary_staff_last_name": "",
            "occurrence_time": "2019-02-24T04:08:01",
            "incident_type_primary": "medical emergency",
            "incident_type_secondary": "",
            "child_involved": False,
            "non_client_involved": True,
            "program": "compass",
            "immediate_response": ["first-aid provided", "naloxone administered"],
            "staff_name": "",
            "program_supervisor_reviewer_name": "",
            "completion_date": "2019-02-24T06:08:01",
        })
        risk_score = get_current_risk_score(mock_form)
        self.assertAlmostEqual(risk_score, 0.52, places=2)

    def test_risk_assessment_client_can_communicate(self):
        mock_form = Form(**{
            "description": "Client was brought to Rubina's office by a classroom volunteer. MB reported pain in his left arm and left side of the chest and trouble breathing. He reported this is a perviously existing condition. Supervisor called EMS. They arrived in approximately in 10 minutes. ER staff evaluated and his ECG was normal but was taken to the Foothills hospital for follow up. Client was able to communicate.",
            "client_primary": " MB",
            "client_secondary": "",
            "location": " yw downtown",
            "location_detail": " 3rd floor.",
            "services_involved": ["ems"],
            "services_involved_other": "police",
            "primary_staff_first_name": "John",
            "primary_staff_last_name": "Doe",
            "occurrence_time": "2019-04-01T10:15:00",
            "incident_type_primary": "medical emergency",
            "incident_type_secondary": "",
            "child_involved": False,
            "non_client_involved": False,
            "program": "linc",
            "immediate_response": ["first-aid provided"],
            "staff_name": "John man",
            "program_supervisor_reviewer_name": "another john",
            "completion_date": "2019-03-28T13:12:00",
        })
        risk_score = get_current_risk_score(mock_form)
        self.assertAlmostEqual(risk_score, 0.26, places=2)

    def test_risk_assessment_violence_involved_under_control(self):
        mock_form = Form(**{
            "description": "CC's male guest came to the office with blood dripping down his face. He told staff that CC hit him with a piece of wood, and he needed staff to get his bags from her. CC came downstairs with the bags, and the guest hid in the office. CC was angry and yelled, but she gave the bags to staff. The guest left with his stuff, and CC went to her room. CPS came and spoke to CC. They asked that CC stay in the building for the night, as they did not consider a risk for violence.",
            "client_primary": "CC",
            "client_secondary": "",
            "location": "yw providence",
            "location_detail": " Main floor office ",
            "services_involved": ["ems"],
            "services_involved_other": "police",
            "primary_staff_first_name": "John",
            "primary_staff_last_name": "Doe",
            "occurrence_time": "2019-04-08T18:15:00",
            "incident_type_primary": " client aggression towards another person",
            "incident_type_secondary": "",
            "child_involved": True,
            "non_client_involved": False,
            "program": "Providence (Community Housing)",
            "safety planning": ["first-aid provided"],
            "staff_name": "John man",
            "program_supervisor_reviewer_name": "another john",
            "completion_date": "2019-04-09T19:25:00",
        })
        risk_score = get_current_risk_score(mock_form)
        self.assertAlmostEqual(risk_score, 0.4, places=2)

    def test_risk_assessment_violence_involved_under_control(self):
        mock_form = Form(**{
            "description": "Community Paramedics (CP) came to assess DA. After assessing her and taking her vitals staff found empty pill packages. It was suspected that she had taken up to 90 Aspirin and 15 Gravol. CP called DA's doctor who concluded that the amount of pills she has taken could lead to liver failure. DA did not want to go to hospital so CP called EMS and police for assistance. DA continued to be resistant in the EMS as they were examining her. Police helped EMS and they took her to Peter Lougheed Hospital.",
            "client_primary": "DA",
            "client_secondary": "",
            "location": "yw downtown",
            "location_detail": "515",
            "services_involved": ["ems"],
            "services_involved_other": "",
            "primary_staff_first_name": "John",
            "primary_staff_last_name": "Doe",
            "occurrence_time": "2019-04-15T17:15:00",
            "incident_type_primary": "medical emergency",
            "incident_type_secondary": "",
            "child_involved": False,
            "non_client_involved": False,
            "program": "transitional housing",
            "immediate_response": ["other"],
            "staff_name": "John man",
            "program_supervisor_reviewer_name": "another john",
            "completion_date": "2019-04-15T19:30:00",
        })
        risk_score = get_current_risk_score(mock_form)
        # TODO: reexamine this risk score
        self.assertAlmostEqual(risk_score, 0.26, places=2)

    def test_risk_assessment_not_responsive(self):
        mock_form = Form(**{
            "description": "Staff heard a loud noise, looked at the cameras and saw SSC laying on the ground blocking the elevator door. Staff went to check on SSC and moved her into the hallway & called 911. Staff sat with SSC while waiting for EMS to arrive however SSC was not responsive to staff. EMS arrived and assessed SSC and because of her low vital signs and recent trip to the hospital they decided to take her back to the Foothills hospital.",
            "client_primary": " SSC ",
            "client_secondary": "",
            "location": "yw maple",
            "location_detail": "4th floor near elevator",
            "services_involved": ["ems"],
            "services_involved_other": "",
            "primary_staff_first_name": "",
            "primary_staff_last_name": "",
            "occurrence_time": "2019-04-27T15:00:00",
            "incident_type_primary": "medical emergency",
            "incident_type_secondary": "",
            "child_involved": False,
            "non_client_involved": False,
            "program": "the maple (community housing)",
            "immediate_response": ["other"],
            "staff_name": "",
            "program_supervisor_reviewer_name": "",
            "completion_date": "2019-04-27T15:20:00",
        })
        risk_score = get_current_risk_score(mock_form)
        # TODO: reexamine this risk score
        self.assertAlmostEqual(risk_score, 0.32, places=2)

    def test_risk_assessment_police_no_actions(self):
        mock_form = Form(**{
            "description": "BH asked staff to call 911; she felt unsafe at shelter (staff letting men in building, women getting someone to beat her up, someone putting meth in her clothes). Staff told her that there was no emergency; she took it upon herself to call 911. police were sent. Police arrived around 1:30 am; stated that they would not take BH anywhere because they considered SK to be a very safe place. BH was not happy with this and called 911 again. BH was on her way out to take her own taxi.",
            "client_primary": "BH",
            "client_secondary": "",
            "location": "yw sheriff king",
            "location_detail": "front office",
            "services_involved": ["ems"],
            "services_involved_other": "police",
            "primary_staff_first_name": "",
            "primary_staff_last_name": "",
            "occurrence_time": "2019-04-27T01:30:00",
            "incident_type_primary": "mental health emergency",
            "incident_type_secondary": "",
            "child_involved": False,
            "non_client_involved": False,
            "program": "transitional housing",
            "immediate_response": ["safety planning"],
            "staff_name": "",
            "program_supervisor_reviewer_name": "",
            "completion_date": "2019-04-28T02:00:00",
        })
        risk_score = get_current_risk_score(mock_form)
        # TODO: reexamine this risk score
        self.assertAlmostEqual(risk_score, 0.32, places=2)

    def test_risk_assessment_police_no_extreme_actions(self):
        mock_form = Form(**{
            "description": "MM came to staff and expressed that she wished to call police to make a statement about the mistreatment of the Stoney People. Writer encouraged MM to call the non-emergency line but MM insisted on calling 911. She made the call and police arrived a short time later to take her statement.  MM thanked them for their time and went back to her room.",
            "client_primary": "MM",
            "client_secondary": "",
            "location": "yw downtown",
            "location_detail": " 4th floor offices ",
            "services_involved": ["police"],
            "services_involved_other": "",
            "primary_staff_first_name": "",
            "primary_staff_last_name": "",
            "occurrence_time": "2019-04-29T21:30:00",
            "incident_type_primary": "other",
            "incident_type_secondary": "",
            "child_involved": False,
            "non_client_involved": False,
            "program": "transitional housing",
            "immediate_response": ["other"],
            "staff_name": "",
            "program_supervisor_reviewer_name": "",
            "completion_date": "2019-04-30T21:17:00",
        })
        risk_score = get_current_risk_score(mock_form)
        # TODO: reexamine this risk score
        self.assertAlmostEqual(risk_score, 0.26, places=2)

    def test_risk_assessment_guest_threatening(self):
        mock_form = Form(**{
            "description": "At approximately 4:30pm WE came up to office crying and told staff the SSC's guest was threatening her - Writer went down and asked SSC if it was time for her guest to and she nodded her head. This writer asked guest to leave and he refused - Writer let guest know that CPS will be called if he does not leave - Guest replied \"Go ahead I will be taken away anyway because I have warrants!\" Writer returned to office and called CPS - At 4:45pm CPS came to building and escorted guest out of building.",
            "client_primary": "WE",
            "client_secondary": "SSC",
            "location": "yw maple",
            "location_detail": "basement common area",
            "services_involved": ["police"],
            "services_involved_other": "",
            "primary_staff_first_name": "",
            "primary_staff_last_name": "",
            "occurrence_time": "2019-05-20T16:30:00",
            "incident_type_primary": "security concern",
            "incident_type_secondary": "suspicion/allegation of abuse towards or against client",
            "child_involved": False,
            "non_client_involved": True,
            "program": "The Maple (community housing)",
            "immediate_response": ["safety assessment"],
            "staff_name": "",
            "program_supervisor_reviewer_name": "",
            "completion_date": "2019-05-20T16:50:00",
        })
        risk_score = get_current_risk_score(mock_form)
        # TODO: reexamine this risk score
        self.assertAlmostEqual(risk_score, 0.35, places=2)

    def test_risk_assessment_child_aggression(self):
        mock_form = Form(**{
            "description": "Writer had an update with HL in regards to how CL was doing at home. HL reported that CL was hitting him and he spanked her. He reported that his emotion was under control and he used the same amount of force as CL used on him.  Writer and HL discussed alternative forms of discipline.Writer consulted Katharine Chapman, clinical supervisor .Writer telephoned SSRT to report concern.",
            "client_primary": "CL",
            "client_secondary": "HL",
            "location": "yw sheriff king",
            "location_detail": "Room 56",
            "services_involved": ["police"],
            "services_involved_other": "",
            "primary_staff_first_name": "",
            "primary_staff_last_name": "",
            "occurrence_time": "2019-06-20T12:00:00",
            "incident_type_primary": "concern for welfare of a child",
            "incident_type_secondary": "",
            "child_involved": "Yes",
            "non_client_involved": True,
            "program": "counselling and personal development",
            "immediate_response": ["called child welfare"],
            "staff_name": "",
            "program_supervisor_reviewer_name": "",
            "completion_date": "2019-06-20T13:00:00",
        })
        risk_score = get_current_risk_score(mock_form)
        # TODO: reexamine this risk score
        self.assertAlmostEqual(risk_score, 0.39, places=2)

    def test_risk_assessment_client_aggression(self):
        mock_form = Form(**{
            "description": "Staff heard the yelling sound coming from unit 405 around 11:20am, staff went to check and found LBP locking her guest with her feet and chocking him, staff told her to let go, another resident TR was also with staff. LBP continued chocking him so staff called 911. When staff was calling she let go of him and her guest just took his bag and left the building. staff heard LBP yelling and throwing things in her unit. CPS arrived at 11:35am talked with her and left.",
            "client_primary": "LBP",
            "client_secondary": "",
            "location": "yw providence",
            "location_detail": "426 2nd Ave NE",
            "services_involved": ["police"],
            "services_involved_other": "",
            "primary_staff_first_name": "",
            "primary_staff_last_name": "",
            "occurrence_time": "2019-09-05T11:20:00",
            "incident_type_primary": "client aggression towards another person",
            "incident_type_secondary": "",
            "child_involved": False,
            "non_client_involved": True,
            "program": "providence (community housing)",
            "immediate_response": ["safety assessment"],
            "staff_name": "",
            "program_supervisor_reviewer_name": "",
            "completion_date": "2019-09-05T11:47:00",
        })
        risk_score = get_current_risk_score(mock_form)
        # TODO: reexamine this risk score
        self.assertAlmostEqual(risk_score, 0.39, places=2)


if __name__ == '__main__':
    main()
