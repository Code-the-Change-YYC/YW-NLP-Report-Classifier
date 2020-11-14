import json
from typing import Dict, Any


class CredentialsError(Exception):
    def __init__(self, message='Error processing credentials'):
        self.message = message


class Credentials:
    """Handles reading and supplying application credentials.
    
    Example:
        ```
        interceptum_pw = Credentials().password
        ```
    """
    _credentials: Dict[str, Any]

    def __init__(self, cred_file_path: str = 'credentials.json'):
        """Creates a `Credentials` instance, reading the credential data.
        
        Params:
            cred_file_path: Path to the credential file. Default reads from a
            `credentials.json` file in the folder the app was started from.
        """
        with open(cred_file_path, 'r') as cred_file:
            self._credentials = json.load(cred_file)

    @property
    def account_name(self) -> str:
        """The Interceptum account name."""
        return self['accountName']

    @property
    def username(self) -> str:
        """The Interceptum username."""
        return self['username']

    @property
    def password(self) -> str:
        """The Interceptum password."""
        return self['password']

    def __getitem__(self, cred_name: str) -> Any:
        """Gets the credential value with name `cred_name`.
        
        Raises:
            CredentialsError: if credential with name `cred_name` could not be
            retrieved.
        """
        if cred_name not in self._credentials:
            raise CredentialsError(
                f'Could not retrieve credential with key {cred_name}.')
        return self._credentials[cred_name]
