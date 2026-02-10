import pytest
import logging
from http import HTTPStatus
from modules.faker_settings import faker, correct_password
from tests.api.api_constants import const

logger = logging.getLogger(__name__)


@pytest.mark.api
@pytest.mark.api_account
@pytest.mark.api_account_registration
@pytest.mark.positive
def test_success_registration(api):
    logger.debug('Username: %s, password: %s', *api.user_data)
    r = api.register(*api.user_data)
    body = r.json()
    logger.debug('test_success_registration, register response body: %s', body)
    user_id = body['userID']

    assert r.status_code == HTTPStatus.CREATED.value
    assert body['username'] == api['username']

    api.delete_user_after_test(api['username'], api['password'], user_id)


@pytest.mark.api
@pytest.mark.api_account
@pytest.mark.api_account_registration
@pytest.mark.negative
@pytest.mark.parametrize(
    'password',
    [
        faker.password(special_chars=False),
        faker.password(digits=False),
        faker.password(upper_case=False),
        faker.password(lower_case=False)
    ],
)
def test_registration_with_incorrect_password(api, password):
    r = api.register(api['username'], password)
    body = r.json()

    assert r.status_code == HTTPStatus.BAD_REQUEST.value
    assert body['code'] == '1300'
    assert body['message'] == const.password_error_validation_message


@pytest.mark.api
@pytest.mark.api_account
@pytest.mark.api_account_registration
@pytest.mark.negative
@pytest.mark.parametrize(
    'username, password',
    [(faker.name(), None), (None, correct_password()),
     (None, None)],
)
def test_registration_without_data(api, username, password):
    r = api.register(username, password)
    body = r.json()

    assert r.status_code == HTTPStatus.BAD_REQUEST.value
    assert body['code'] == '1200'
    assert body['message'] == const.fields_are_required


@pytest.mark.api
@pytest.mark.api_account
@pytest.mark.api_account_login
@pytest.mark.positive
def test_success_login(api):
    logger.debug('Success_login. Username: %s, password: %s',
                 *api.user_data)
    r = api.register(*api.user_data)
    logger.debug('Register response(success login test): %s', r.json())
    r = api.login(*api.user_data)
    body = r.json()
    token = body['token']
    user_id = body['userId']
    logger.debug('Login response(success login test): %s', body)

    assert r.status_code == HTTPStatus.OK.value
    assert token is not None

    api.delete_user(user_id, token)


@pytest.mark.api
@pytest.mark.api_account
@pytest.mark.api_account_login
@pytest.mark.negative
def test_login_with_unregistered_data(api):
    r = api.login(*api.user_data)
    body = r.json()

    assert r.status_code == HTTPStatus.OK.value
    assert body['token'] in None
    assert body['expires'] in None
    assert body['status'] == 'Failed'
    assert body['result'] == const.failed_auth


@pytest.mark.api
@pytest.mark.api_account
@pytest.mark.api_account_login
@pytest.mark.negative
def test_login_with_incorrect_password(api_user):
    incorrect_password = correct_password()

    r = api_user.login(api_user['username'], incorrect_password)
    body = r.json()

    assert r.status_code == HTTPStatus.OK.value
    assert body['token'] in None
    assert body['expires'] in None
    assert body['status'] == 'Failed'
    assert body['result'] == const.failed_auth


@pytest.mark.api
@pytest.mark.api_account
@pytest.mark.api_account_login
@pytest.mark.negative
@pytest.mark.parametrize(
    'username, password',
    [(faker.name(), None),
     (None, correct_password()),
     (None, None)],
)
def test_login_without_data(api, username, password):
    r = api.login(username, password)
    body = r.json()

    assert r.status_code == HTTPStatus.BAD_REQUEST.value
    assert body['code'] == '1200'
    assert body['message'] == const.fields_are_required


@pytest.mark.api
@pytest.mark.api_account
@pytest.mark.api_account_is_authorized
@pytest.mark.positive
def test_user_is_not_authorized(api_user):
    r = api_user.is_authorized(*api_user.user_data)
    body = r.json()

    assert r.status_code == HTTPStatus.OK.value
    assert body == 'false'


@pytest.mark.api
@pytest.mark.api_account
@pytest.mark.api_account_is_authorized
@pytest.mark.positive
def test_user_is_authorized(api_user):
    api_user.login(*api_user.user_data)

    r = api_user.is_authorized(*api_user.user_data)
    body = r.json()

    assert r.status_code == HTTPStatus.OK.value
    assert body == 'true'


@pytest.mark.api
@pytest.mark.api_account
@pytest.mark.api_account_is_authorized
@pytest.mark.negative
def test_user_is_authorized_not_found(api):
    r = api.is_authorized(*api.user_data)
    body = r.json()

    assert r.status_code == HTTPStatus.NOT_FOUND.value
    assert body['code'] == '1207'
    assert body['message'] == const.user_404


@pytest.mark.api
@pytest.mark.api_account
@pytest.mark.api_account_is_authorized
@pytest.mark.negative
@pytest.mark.parametrize(
    'username, password',
    [(None, faker.name()), (None, None),
     (correct_password(), None)],
)
def test_user_is_authorized_without_data(api, username, password):
    r = api.is_authorized(username, password)
    body = r.json()

    assert r.status_code == HTTPStatus.BAD_REQUEST.value
    assert body['code'] == '1200'
    assert body['message'] == const.fields_are_required


@pytest.mark.api
@pytest.mark.api_account
@pytest.mark.api_account_data
@pytest.mark.positive
def test_get_user_data_success(api_user):
    r = api_user.login(*api_user.user_data)
    body = r.json()
    user_id = body['userId']
    token = body['token']

    r = api_user.get_user(user_id, token)
    body = r.json()

    assert r.status_code == HTTPStatus.OK.value
    assert body['username'] == api_user['username']
    assert body['userID'] == user_id


@pytest.mark.api
@pytest.mark.api_account
@pytest.mark.api_account_data
@pytest.mark.negative
def test_get_user_not_authorized(api):
    r = api.register(*api.user_data)
    user_id = r.json()['userID']

    r = api.get_user(user_id, None)
    body = r.json()

    assert r.status_code == HTTPStatus.UNAUTHORIZED.value
    assert body['code'] == '1200'
    assert body['message'] == const.no_auth

    r = api.login(api['username'], api['password'])
    token = r.json()['token']
    api.delete_user(user_id, token)


@pytest.mark.api
@pytest.mark.api_account
@pytest.mark.api_account_data
@pytest.mark.negative
@pytest.mark.parametrize(
    'user_id_to_delete',
    ['81719c87-1617-41ba-ace9-aa7431', '81719c87-1617-41b-ace9-aa74311',
     '81719c87-1617-41ba-ace-aa74311', '81719c87-161-41ba-ace9-aa74311',
     '81719c8-1617-41ba-ace9-aa74311'],
)
def test_get_user_with_incorrect_user_id(api_user, user_id_to_delete):
    r = api_user.login(*api_user.user_data)
    body = r.json()
    token = body['token']

    r = api_user.get_user(user_id_to_delete, token)
    body = r.json()

    assert r.status_code == HTTPStatus.UNAUTHORIZED.value
    assert body['code'] == '1207'
    assert body['message'] == const.user_404


@pytest.mark.api
@pytest.mark.api_account
@pytest.mark.api_account_delete
@pytest.mark.positive
def test_success_delete(api_user):
    r = api_user.login(*api_user.user_data)
    body = r.json()
    user_id = body['userID']
    token = body['token']

    r = api_user.delete_user(user_id, token)

    assert r.status_code == HTTPStatus.NO_CONTENT.value
    assert r.json() is None


@pytest.mark.api
@pytest.mark.api_account
@pytest.mark.api_account_delete
@pytest.mark.negative
def test_delete_twice(api_user):
    username = faker.name()
    password = correct_password()

    # user to delete twice
    api_user.register(username, password)
    r = api_user.login(username, password)
    body = r.json()
    user_id = body['userId']

    # user who will deleting first one
    r = api_user.login(*api_user.user_data)
    body = r.json()
    token = body['token']

    api_user.delete_user(user_id, token)
    r = api_user.delete_user(user_id, token)
    body = r.json()

    assert r.status_code == HTTPStatus.OK.value
    assert body['code'] == '1207'
    assert body['message'] == const.incorrect_user_id


@pytest.mark.api
@pytest.mark.api_account
@pytest.mark.api_account_delete
@pytest.mark.negative
@pytest.mark.debug
@pytest.mark.parametrize(
    'user_id',
    ['81719c87-1617-41ba-ace9-aa7431', '81719c87-1617-41b-ace9-aa74311',
     '81719c87-1617-41ba-ace-aa74311', '81719c87-161-41ba-ace9-aa74311',
     '81719c8-1617-41ba-ace9-aa74311'],
)
def test_delete_with_incorrect_user_id(api_user, user_id):
    logger.debug('User data: %s, %s', *api_user.user_data)
    r = api_user.login(*api_user.user_data)
    body = r.json()
    token = body['token']

    r = api_user.delete_user(user_id, token)
    body = r.json()

    assert r.status_code == HTTPStatus.OK.value
    assert body['code'] == '1207'
    assert body['message'] == const.incorrect_user_id


@pytest.mark.api
@pytest.mark.api_account
@pytest.mark.api_account_delete
@pytest.mark.negative
def test_delete_without_token(api_user):
    r = api_user.login(*api_user.user_data)
    user_id = r.json()['userId']

    r = api_user.delete_user(user_id, None)
    body = r.json()
    logger.debug('''test_delete_without_token. delete body response:
                 %s
                 body type: %s''',
                 body, type(body))

    assert r.status_code == HTTPStatus.UNAUTHORIZED.value
    assert body['code'] == '1200'
    assert body['message'] == const.no_auth
