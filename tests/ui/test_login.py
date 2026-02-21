import pytest
import os
from modules.ui.ui_constants import const
from modules.faker_settings import faker


@pytest.mark.ui
@pytest.mark.ui_login
@pytest.mark.positive
def test_success_login(ui_login):
    username = os.getenv('user_name')
    password = os.getenv('password')

    ui_login.fill_username_field(username)
    ui_login.fill_password_field(password)
    ui_login.press_login_button()

    assert ui_login.check_url(const.profile_url)
    assert ui_login.check_title(const.page_title)


@pytest.mark.ui
@pytest.mark.ui_login
@pytest.mark.positive
def test_new_user_button(ui_login):
    ui_login.press_register_button_login()
    assert ui_login.check_url(const.register_url)
    assert ui_login.check_title(const.page_title)


@pytest.mark.ui
@pytest.mark.ui_login
@pytest.mark.negative
def test_unsuccess_login(ui_login):
    username = faker.user_name()
    password = faker.password()

    assert ui_login.check_is_element_is_invisible(
        const.login_page_id['error_message'])

    ui_login.fill_username_field(username)
    ui_login.fill_password_field(password)
    ui_login.press_login_button()

    assert ui_login.check_error_text()
    assert ui_login.check_url(const.login_url)
    assert ui_login.check_title(const.page_title)


@pytest.mark.ui
@pytest.mark.ui_login
@pytest.mark.negative
def test_errors_in_logins_fields(ui_login):
    username = os.getenv('user_name')
    password = os.getenv('password')

    ui_login.press_login_button()
    assert ui_login.check_is_error_in_field_login('username')
    assert ui_login.check_is_error_in_field_login('password')

    ui_login.fill_username_field(username)
    assert ui_login.check_is_error_in_field_login('username') is False

    ui_login.fill_password_field(password)
    assert ui_login.check_is_error_in_field_login('password') is False
    assert ui_login.check_title(const.page_title)
