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
        """
        Docstring for is_authorized

        Returns True in response, if user is authorized

        :param self:
        :param name:
        :type name: str
        :param password: Min - 1 capital letter, 1 small letter,
                        1 special char, 1 digit
        :type password: str
        :return:
        :rtype: Request
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
        """
        Docstring for delete_user

        :param self:
        :param user_id: ID of existing user
        :type user_id: str
        :param token: Bearer token
        :type token: str
        :return:
        :rtype: Response
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
        """
        Docstring for get_user

        :param self:
        :param user_id: ID of existing user
        :type user_id: str
        :param token: Bearer token
        :type token: str
        :return:
        :rtype: Response
        """
        header = {
            'Authorization': f'Bearer {token}',
        }

        r = requests.get(f'{self.URL_account}/User/{user_id}', headers=header)
        return r
