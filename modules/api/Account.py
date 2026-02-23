import requests
import logging
from modules.faker_settings import faker, correct_password

logger = logging.getLogger(__name__)


class Account:
    URL_account = 'https://demoqa.com/Account/v1'

    def __init__(self):
        self.username = faker.name()
        self.password = correct_password()
        self.user_data = (self.username, self.password)

    def is_authorized(
            self,
            name: str,
            password: str,
    ) -> requests.Response:
        """Sending request to check is user authorized.
        Returns True in response, if user is authorized

        Args:
            name (str): Username.
            password (str): Password (min: 1 uppercase, 1 lowercase,
                1 special character, 1 digit).

        Returns:
            requests.Response: Response indicating whether the user is
                authorized.
        """
        data = {
            'userName': name,
            'password': password,
        }
        r = requests.post(f'{self.URL_account}/Authorized', json=data)
        return r

    def login(
            self,
            name: str,
            password: str,
    ) -> requests.Response:
        """Send a request to log in a user.

        Note:
            The token in the login response will be None unless
            `generate_token` was called first.

        Args:
            name (str): username
            password (str): password

        Returns:
            requests.Response: userId(str), username(str), password(str),
             token(str | None), expires(str | None), created_date(str),
             isActive(bool)
        """
        data = {
            'userName': name,
            'password': password,
        }
        r = requests.post(f'{self.URL_account}/Login', json=data)
        return r

    def generate_token(
            self,
            name: str,
            password: str,
    ) -> requests.Response:
        """Send a request to generate a user's token.

        This request should be sent before `login` if a token is required.

        Args:
            name (str): username
            password (str): password

        Returns:
            requests.Response: token(str), expires(str), status(str),
             result(str)
        """
        data = {
            'userName': name,
            'password': password,
        }
        r = requests.post(f'{self.URL_account}/GenerateToken', json=data)
        return r

    def register(
            self,
            name: str,
            password: str,
    ) -> requests.Response:
        """Send a request to register a new user.

        Args:
            name (str): username
            password (str): password

        Returns:
            requests.Response: userID(str), username(str), books(list)
        """
        data = {
            'userName': name,
            'password': password,
        }
        r = requests.post(f'{self.URL_account}/User', json=data)
        return r

    def delete_user(
            self,
            user_id: str,
            token: str,
    ) -> requests.Response:
        """Send a request to delete a user.

        Args:
            user_id (str): ID of existing user
            token (str): Bearer token

        Returns:
            requests.Response: None in body
        """
        header = {
            'Authorization': f'Bearer {token}',
        }
        r = requests.delete(f'{self.URL_account}/User/{user_id}',
                            headers=header)
        logger.debug('Delete response header: %s', r.headers)
        return r

    def get_user(
            self,
            user_id: str,
            token: str,
    ) -> requests.Response:
        """Send a request to retrieve information about a specific user.

        Args:
            user_id (str): ID of existing user
            token (str): Bearer token

        Returns:
            requests.Response: userId(str), username(str), books(list)
        """
        header = {
            'Authorization': f'Bearer {token}',
        }

        r = requests.get(f'{self.URL_account}/User/{user_id}', headers=header)
        return r
