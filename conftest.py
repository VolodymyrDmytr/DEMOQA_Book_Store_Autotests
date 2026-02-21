from modules.api.book_store import BookStore
from modules.ui.demo_qa import DemoQA

from selenium.common import exceptions
from modules.logger_settings import setup_logging
import logging
from tests.test_data import data
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
    user.driver.execute_script('window.scroll(0,90)')

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
    book_id = data.random_book_id()
    books = [data.get_book_by_book_id(book_id)]

    user = DemoQA(books)
    logger.debug('%s', user)

    user.go_to()

    user.driver.execute_script('window.scroll(0, 90)')
    user.click_book_link(user.books[0]['title'])
    assert user.check_url(const.book_url_format.format(user.books[0]['isbn']))
    user.driver.execute_script('window.scroll(0,0)')

    yield user

    user.teardown()


@pytest.fixture
def ui_book_login():
    book_id = data.random_book_id()
    books = [data.get_book_by_book_id(book_id)]

    user = DemoQA(books)

    user.go_to()
    user.driver.execute_script('window.scroll(0,0)')
    user.press_login_button()

    user.username = os.getenv('user_name')
    user.password = os.getenv('password')

    user.fill_username_field(user.username)
    user.fill_password_field(user.password)
    user.press_login_button()

    user.press_go_to_book_store_button_profile()
    logger.debug('%s', user)
    logger.debug('Books list: %s', user.books)
    user.driver.execute_script('window.scroll(0, 90)')
    user.click_book_link(user.books[0]['title'])
    user.driver.execute_script('window.scroll(0,0)')

    yield user

    user.press_log_out_button()

    user.fill_username_field(user.username)
    user.fill_password_field(user.password)
    user.press_login_button()

    user.press_delete_all_books_button()
    user.actions_with_modal('OK')

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
def ui_profile_with_books():
    user = DemoQA()

    user.go_to()

    user.press_login_button()

    user.username = os.getenv('user_name')
    user.password = os.getenv('password')

    user.fill_username_field(user.username)
    user.fill_password_field(user.password)
    user.press_login_button()

    user.wait_till_books_loaded()
    user.press_delete_all_books_button()
    user.actions_with_modal('ok')
    try:
        user.accept_alert()
        user.actions_with_modal('x')
    except exceptions.TimeoutException:
        pass

    user.press_go_to_book_store_button_profile()

    user.books = []

    for _ in range(2):
        while True:
            book_id = data.random_book_id()
            book = data.get_book_by_book_id(book_id)

            if any(book['isbn'] == b['isbn'] for b in user.books):
                continue

            user.books.append(book)
            user.click_book_link(book['title'])
            user.press_add_to_collection_button()
            user.accept_alert()
            user.press_back_to_store_button()

            break
    logger.debug('%s', user)

    user.press_log_out_button()

    user.fill_username_field(user.username)
    user.fill_password_field(user.password)
    user.press_login_button()

    yield user

    user.press_log_out_button()

    user.fill_username_field(user.username)
    user.fill_password_field(user.password)
    user.press_login_button()

    user.wait_till_books_loaded()
    user.press_delete_all_books_button()
    user.actions_with_modal('ok')
    try:
        user.accept_alert()
    except exceptions.TimeoutException:
        pass
    user.actions_with_modal('x')

    user.teardown()
