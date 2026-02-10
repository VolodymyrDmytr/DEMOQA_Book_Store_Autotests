from modules.api.BookStore import BookStore
from http import HTTPStatus

import pytest

from modules.logger_settings import setup_logging

logger = setup_logging()


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

    yield user

    r = user.login(*user.user_data)

    if r.status_code == HTTPStatus.OK.value and (
     'json' in r.headers.get('Content-Type')):
        body = r.json()
        user_id = body['userId']
        token = body['token']

        user.delete_user(user_id, token)
    else:
        logger.warning('Login failed. Status code: %s, Body: %s',
                       r.status_code, r.text)
