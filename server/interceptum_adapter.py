from server.credentials import Credentials
import xml.etree.ElementTree as ET

import requests
from datetime import datetime

import pytz
from server.schemas.submit import Form
import server.interceptum_adapter_d as d

INTERCEPTUM_ENDPOINT = 'https://interceptum.com/service/survey.do'

invite_req_body_base = """
<REQUEST>  <!--The Service operation-->
  <action>invite</action>
  <!--The credential token obtained from the login operation-->
<credentials>{credentials}</credentials>
  <!--The Survey's unique identifier-->
  <sId>5333180</sId>
  <!--The language in which to sent the invitation [en; fr]-->
  <langCode>en</langCode>
	<!--The first name of the participant (optional)-->
	<firstname>fname</firstname>
	<!--The last name of the participant (optional)-->
	<lastname>lname</lastname>
	<!--The email of the participant (optional)-->
	<email>email@email.com</email>
	<!--The subject of the invitation message (optional)-->

	<subject>filler</subject>
  <!--The contents of the invitation message (optional)-->
	<message>filler</message>
	<!-- 1 to prevent email sending-->
	<addOnly>1</addOnly>
  <!--Additional values to pre-populate data (optional)-->
  <values>
		{form_values_xml}
    </values>
</REQUEST>
"""

login_request_body_base = """
<REQUEST>  <!--The Service operation-->
  <action>login</action>
  <!--The name of the account-->
  <accountName>{account_name}</accountName>
  <!--The username of the user to use in the API calls-->
  <username>{username}</username>
  <!--The password of the user to use in the API calls-->
  <password>{password}</password>
</REQUEST>
"""

XML_REQ_HEADERS = {'Content-Type': 'text/xml'}


class InterceptumException(Exception):
    def __init__(self, message='Exception occurred while using Interceptum.'):
        self.message = message


class InterceptumAdapter():
    account_credentials: Credentials
    api_credentials: str

    def __init__(self, account_credentials: Credentials):
        """Inits `InterceptumAdapter` with the given `account_name`, `username`,
        and `password` to use in requests."""
        self.account_credentials = account_credentials
        self.api_credentials = self.get_api_credentials()

    def call_api(self, request_body: dict) -> str:
        """Calls the Interceptum API with the given request body.

        Params:
            request_body: Python dict converted from the JSON body of the /api/submit endpoint

        Returns:
            The redirect URL to the autocompleted Interceptum form
        """
        invite_res_root = self.send_invite_request(request_body)
        final_url = "https://interceptum.com/si/en/5333180?code="

        invalid_invite_code_exception = InterceptumException(
            'Unable to obtain invite code from Interceptum.')

        try:
            invite_code = invite_res_root.find("data").find("inviteCode").text
            if invite_code is None:
                raise invalid_invite_code_exception
        except AttributeError:
            raise invalid_invite_code_exception

        if invite_res_root:
            final_url = final_url + invite_code
        else:
            raise InterceptumException(
                'Error obtaining invite request from Interceptum.')

        return final_url

    def send_invite_request(self, request_body: dict) -> ET.Element:
        """Sends an invite request to Interceptum and returns the root XML
        element.

        Retries the request with freshly retrieved credentials if an error
        occurs in the first attempt.

        Raises:
            All exceptions from `get_credentials`.
        """
        credentials = self.get_api_credentials()
        form_values_xml = self.form_values_to_xml(request_body)
        invite_req_body = invite_req_body_base.format(
            credentials=credentials, form_values_xml=form_values_xml)
        res = requests.post(INTERCEPTUM_ENDPOINT,
                            data=invite_req_body,
                            headers=XML_REQ_HEADERS)

        post_res_root = ET.fromstring(res.content)
        error = post_res_root.find('ERRORS') is not None \
            or post_res_root.find('ERRORCODE') is not None
        # Retry the request with fresh credentials on error
        if error:
            credentials = self.get_api_credentials(force_refresh=True)
            invite_req_body = invite_req_body_base.format(
                credentials=credentials, form_values_xml=form_values_xml)
            res = requests.post(INTERCEPTUM_ENDPOINT,
                                data=invite_req_body,
                                headers=XML_REQ_HEADERS)
            return ET.fromstring(res.content)
        else:
            return post_res_root

    def get_api_credentials(self, force_refresh: bool = False) -> str:
        """Gets Interceptum credentials via a login request.

        Does not request fresh credentials if `self.credentials` has been
        created already, unless `force_refresh` is `True`.

        Raises:
            InterceptumException: Unable to retrieve credentials.
        """
        credentials_exists = getattr(self, 'credentials', None) is not None
        if not force_refresh and credentials_exists:
            return self.api_credentials

        login_request_body = login_request_body_base.format(
            account_name=self.account_credentials.account_name,
            username=self.account_credentials.username,
            password=self.account_credentials.password)
        res = requests.post(INTERCEPTUM_ENDPOINT,
                            data=login_request_body,
                            headers=XML_REQ_HEADERS)
        login_res_root = ET.fromstring(res.content)

        login_exception = InterceptumException(
            'Error logging in to Interceptum.')
        try:
            cred = login_res_root.find('data').find('credentials').text
            if cred is None:
                raise login_exception
            return cred
        except AttributeError:
            raise login_exception

    def form_values_to_xml(self, form_values: dict) -> str:
        xml_values = []
        for field, value in form_values.items():
            if value is None:
                continue
            if isinstance(value, list):
                value_map = d.multi_options[field]
                mapped_text = (str(value_map[val]) for val in value
                               if val in value_map)
                text = "|".join(mapped_text)

            elif isinstance(value, datetime):
                localtime = value.astimezone(pytz.timezone("Canada/Mountain"))
                text = localtime.strftime("%Y-%m-%d %H:%M")

            elif isinstance(value, bool):
                text = d.interceptum_boolean_dict[value]

            elif field in d.single_option:
                value_map = d.single_option[field]
                text = value_map[value]
            else:
                text = value

            fId = d.field_values_dict[field]
            xml_values.append(f"<value fId=\"{fId}\">{text}</value>")
        return "".join(xml_values)

    @staticmethod
    def xml_to_form_values(xml) -> dict:
        # TODO: Implement
        pass
