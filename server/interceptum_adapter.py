import xml.etree.ElementTree as ET

import requests

from server.schemas.submit import Form

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
    account_name: str
    username: str
    password: str

    def __init__(self, account_name: str, username: str, password: str):
        """Inits `InterceptumAdapter` with the given `account_name`, `username`,
        and `password` to use in requests."""
        self.account_name = account_name
        self.username = username
        self.password = password

    def call_api(self, request_body: Form) -> str:
        """Calls the Interceptum API with the given request body.

        :param request_body: Python dict converted from the JSON body of the /api/submit endpoint
        :return: The redirect URL to the autocompleted Interceptum form
        """
        credentials = self.get_credentials()
        form_values_xml = self.form_values_xml()
        invite_req_body = invite_req_body_base.format(
            credentials=credentials, form_values_xml=form_values_xml)
        res = requests.post(INTERCEPTUM_ENDPOINT,
                            data=invite_req_body,
                            headers=XML_REQ_HEADERS)
        if res.ok and res.content:
            print(res.content)
        else:
            raise InterceptumException(
                'Error obtaining invite request from Interceptum.')

        return ''

    def get_credentials(self) -> str:
        """Gets Interceptum credentials via a login request.
        
        Raises:
            InterceptumException: Unable to retrieve credentials.
        """
        login_request_body = login_request_body_base.format(
            account_name=self.account_name,
            username=self.username,
            password=self.password)
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

    def form_values_xml(self):
        return '<value fId="447821">TS</value>'
