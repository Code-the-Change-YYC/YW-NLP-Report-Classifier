class InterceptumAdapter():
    def call_api(self, request_body: dict) -> string:
        """Calls the Interceptum API with the given request body.

        :param request_body: Python dict converted from the JSON body of the /api/submit endpoint
        :return: The redirect URL to the autocompleted Interceptum form
        """
        ...