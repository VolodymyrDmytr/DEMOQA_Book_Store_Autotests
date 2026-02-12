from modules.api.BookStore import BookStore
from http import HTTPStatus

import pytest

from modules.logger_settings import setup_logging
import logging

logger = setup_logging()
logger = logging.getLogger(__name__)


@pytest.fixture
def api():
    user = BookStore()

    yield user


@pytest.fixture
def api_user():
    user = BookStore()

    r = user.register(*user.user_data)

    if r.status_code not in (201, 406):
        pytest.fail(
            f"User registration failed: {r.status_code} {r.text}")
        logger.debug('Used data: Username = %s, Password = %s',
                     *user.user_data)

    user.generate_token(*user.user_data)

    yield user

    r = user.login(*user.user_data)

    if r.status_code == HTTPStatus.OK.value:
        body = r.json()
        user_id = body['userId']
        token = body['token']

        user.delete_user(user_id, token)
    else:
        logger.warning('Login failed. Status code: %s, Body: %s',
                       r.status_code, r.text)


@pytest.fixture(scope='session')
def my_user():
    user = BookStore()

    user.register(*user.user_data)

    user.generate_token(*user.user_data)

    r = user.login(*user.user_data)
    body = r.json()
    user.token = body['token']
    user.user_id = body['userId']

    yield user

    user.delete_user(user.user_id, user.token)
