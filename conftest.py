from modules.api.book_store import BookStore
from modules.ui.demo_qa import DemoQA

from selenium.common import exceptions
from modules.logger_settings import setup_logging
import logging
from modules.ui.ui_constants import const
import os
from http import HTTPStatus

import pytest


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


@pytest.fixture
def ui():
    user = DemoQA()

    user.go_to()
    user.scroll_to(90)

    yield user

    user.teardown()


@pytest.fixture
def ui_login():
    user = DemoQA()

    user.username = os.getenv('user_name')
    user.password = os.getenv('password')

    user.go_to()
    user.press_login_button()

    yield user

    user.teardown()


@pytest.fixture
def ui_register():
    user = DemoQA()

    user.go_to()
    user.press_login_button()
    user.press_register_button_login()

    yield user

    try:
        user.press_delete_account_button()
    except exceptions.TimeoutException:
        logger.info('Account wasn`t created. So didn`t deleted')

    user.teardown()


@pytest.fixture
def ui_book_no_login():
    api = BookStore()
    books = [api.get_random_book_dict()]

    user = DemoQA(books)
    logger.debug('%s', user)

    user.go_to()

    user.scroll_to(90)
    user.click_book_link(user.books[0]['title'])
    assert user.check_url(const.book_url_format.format(user.books[0]['isbn']))
    user.scroll_to(0)

    yield user

    user.teardown()


@pytest.fixture
def ui_book_login():
    api = BookStore()
    books = [api.get_random_book_dict()]

    user = DemoQA(books)

    user.go_to()
    user.scroll_to(0)
    user.press_login_button()

    user.username = os.getenv('user_name')
    user.password = os.getenv('password')

    user.fill_username_field(user.username)
    user.fill_password_field(user.password)
    user.press_login_button()

    user.press_go_to_book_store_button_profile()
    logger.debug('%s', user)
    logger.debug('Books list: %s', user.books)
    user.scroll_to(90)
    user.click_book_link(user.books[0]['title'])
    user.scroll_to(0)

    yield user

    api.generate_token(user.username, user.password)
    r = api.login(user.username, user.password)
    body = r.json()
    user_id = body['userId']
    token = body['token']
    api.delete_all_users_books(user_id, token)

    user.teardown()


@pytest.fixture
def ui_profile():
    user = DemoQA()

    user.go_to()

    user.press_login_button()

    user.username = os.getenv('user_name')
    user.password = os.getenv('password')

    user.fill_username_field(user.username)
    user.fill_password_field(user.password)
    user.press_login_button()

    yield user

    user.teardown()


@pytest.fixture
def ui_profile_for_delete():
    user = DemoQA()
    api = BookStore()

    api.register(user.username, user.password)

    user.go_to()

    user.press_login_button()

    user.fill_username_field(user.username)
    user.fill_password_field(user.password)
    user.press_login_button()

    yield user

    user.teardown()


@pytest.fixture
def ui_profile_with_books():
    user = DemoQA()
    api = BookStore()

    # API register here
    r = api.register(user.username, user.password)
    body = r.json()
    user_id = body['userID']

    r = api.generate_token(user.username, user.password)
    body = r.json()
    token = body['token']

    # adding books to registered account
    books_id_list, books_number_list = api.get_random_books_list(2)
    api.post_users_books_list(user_id, books_id_list, token)

    # Adding books to user.books
    books_list = []
    for element in books_id_list:
        r = api.get_book(element)
        body = r.json()
        books_list.append(body)
    user.books = books_list

    # Moving to profile page
    user.go_to()
    user.press_login_button()

    user.fill_username_field(user.username)
    user.fill_password_field(user.password)
    user.press_login_button()

    yield user

    user.teardown()

    # Delete created account
    r = api.generate_token(user.username, user.password)
    body = r.json()
    token = body['token']
    api.delete_user(user_id, token)
