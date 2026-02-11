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

    assert r.status_code == HTTPStatus.CREATED.value
    assert body['username'] == api.username

    r = api.login(*api.user_data)
    body = r.json()
    api.delete_user(body['userId'], body['token'])


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
    r = api.register(api.username, password)
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
@pytest.mark.api_account_generate_token
@pytest.mark.positive
def test_success_login(api):
    logger.debug('Success_login. Username: %s, password: %s',
                 *api.user_data)
    r = api.register(*api.user_data)
    logger.debug('Register response(success login test): %s', r.json())
    api.generate_token(*api.user_data)
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
@pytest.mark.api_account_generate_token
@pytest.mark.negative
def test_generate_token_with_unregistered_data(api):
    r = api.generate_token(*api.user_data)
    body = r.json()

    assert r.status_code == HTTPStatus.OK.value
    assert body['token'] is None
    assert body['expires'] is None
    assert body['status'] == 'Failed'
    assert body['result'] == const.failed_auth


@pytest.mark.api
@pytest.mark.api_account
@pytest.mark.api_account_generate_token
@pytest.mark.negative
def test_generate_token_with_incorrect_password(my_user):
    incorrect_password = correct_password()

    r = my_user.generate_token(my_user.username, incorrect_password)
    body = r.json()

    assert r.status_code == HTTPStatus.OK.value
    assert body['token'] is None
    assert body['expires'] is None
    assert body['status'] == 'Failed'
    assert body['result'] == const.failed_auth


@pytest.mark.api
@pytest.mark.api_account
@pytest.mark.api_account_generate_token
@pytest.mark.negative
@pytest.mark.parametrize(
    'username, password',
    [(faker.name(), None),
     (None, correct_password()),
     (None, None)],
)
def test_generate_token_without_data(api, username, password):
    r = api.generate_token(username, password)
    body = r.json()

    assert r.status_code == HTTPStatus.BAD_REQUEST.value
    assert body['code'] == '1200'
    assert body['message'] == const.fields_are_required


@pytest.mark.api
@pytest.mark.api_account
@pytest.mark.api_account_login
@pytest.mark.positive
def test_successfull_login(my_user):
    r = my_user.login(*my_user.user_data)
    body = r.json()

    assert r.status_code == HTTPStatus.OK.value
    assert body['userId'] == my_user.user_id
    assert body['username'] == my_user.username
    assert body['token'] == my_user.token


@pytest.mark.api
@pytest.mark.api_account
@pytest.mark.api_account_login
@pytest.mark.negative
@pytest.mark.parametrize(
    'username, password',
    [(faker.name(), correct_password()), (faker.name(), None),
     (None, correct_password()), (None, None)],
)
def test_unsuccessfull_login(api, username, password):
    r = api.login(username, password)

    assert r.status_code == HTTPStatus.OK.value
    assert r.text == ""


@pytest.mark.api
@pytest.mark.api_account
@pytest.mark.api_account_is_authorized
@pytest.mark.positive
def test_user_is_not_authorized(api):
    api.register(*api.user_data)
    r = api.is_authorized(*api.user_data)
    body = r.json()

    assert r.status_code == HTTPStatus.OK.value
    assert body is False


@pytest.mark.api
@pytest.mark.api_account
@pytest.mark.api_account_is_authorized
@pytest.mark.positive
def test_user_is_authorized(api_user):
    r = api_user.is_authorized(*api_user.user_data)
    body = r.json()

    assert r.status_code == HTTPStatus.OK.value
    assert body is True


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
    assert body['username'] == api_user.username
    assert body['userId'] == user_id


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

    r = api.login(*api.user_data)
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
def test_get_user_with_incorrect_user_id(my_user, user_id_to_delete):
    r = my_user.get_user(user_id_to_delete, my_user.token)
    body = r.json()

    assert r.status_code == HTTPStatus.UNAUTHORIZED.value
    assert body['code'] == '1207'
    assert body['message'] == const.user_404


@pytest.mark.api
@pytest.mark.api_account
@pytest.mark.api_account_delete
@pytest.mark.positive
def test_success_delete(api):
    api.register(*api.user_data)
    api.generate_token(*api.user_data)
    r = api.login(*api.user_data)
    body = r.json()
    user_id = body['userId']
    token = body['token']

    r = api.delete_user(user_id, token)

    assert r.status_code == HTTPStatus.NO_CONTENT.value
    assert r.text == ""


@pytest.mark.api
@pytest.mark.api_account
@pytest.mark.api_account_delete
@pytest.mark.negative
def test_delete_twice(my_user):
    username = faker.name()
    password = correct_password()

    # user to delete twice
    my_user.register(username, password)
    r = my_user.login(username, password)
    body = r.json()
    user_id = body['userId']

    my_user.delete_user(user_id, my_user.token)
    r = my_user.delete_user(user_id, my_user.token)
    body = r.json()

    assert r.status_code == HTTPStatus.UNAUTHORIZED.value
    assert body['code'] == '1200'
    assert body['message'] == const.no_auth


@pytest.mark.api
@pytest.mark.api_account
@pytest.mark.api_account_delete
@pytest.mark.negative
@pytest.mark.parametrize(
    'user_id',
    ['81719c87-1617-41ba-ace9-aa7431', '81719c87-1617-41b-ace9-aa74311',
     '81719c87-1617-41ba-ace-aa74311', '81719c87-161-41ba-ace9-aa74311',
     '81719c8-1617-41ba-ace9-aa74311'],
)
def test_delete_with_incorrect_user_id(my_user, user_id):
    r = my_user.delete_user(user_id, my_user.token)
    body = r.json()

    assert r.status_code == HTTPStatus.OK.value
    assert body['code'] == '1207'
    assert body['message'] == const.incorrect_user_id


@pytest.mark.api
@pytest.mark.api_account
@pytest.mark.api_account_delete
@pytest.mark.negative
def test_delete_without_token(my_user):
    r = my_user.delete_user(my_user.user_id, None)
    body = r.json()
    logger.debug('''test_delete_without_token. delete body response:
                 %s
                 body type: %s''',
                 body, type(body))

    assert r.status_code == HTTPStatus.UNAUTHORIZED.value
    assert body['code'] == '1200'
    assert body['message'] == const.no_auth
