import pytest
from modules.faker_settings import faker
from modules.ui.ui_constants import const
import os


# Capcha is blocking registration
# @pytest.mark.ui
# @pytest.mark.ui_registration
# @pytest.mark.positive
# def test_success_registration(ui_register):
#     ui_register.fill_register_form(
#         faker.first_name(),
#         faker.last_name(),
#         ui_register.username,
#         ui_register.password,
#     )

#     ui_register.press_register_button_registration()

#     assert ui_register.check_alert_success_register_text()
#     ui_register.confirm_success_registered_alert()

#     assert ui_register.check_url(const.profile_url)


@pytest.mark.ui
@pytest.mark.ui_registration
@pytest.mark.positive
def test_go_to_login(ui_register):
    ui_register.press_back_to_login_button()

    assert ui_register.check_url(const.login_url)


@pytest.mark.ui
@pytest.mark.ui_registration
@pytest.mark.negative
def test_validation_error_on_register_fields(ui_register):
    ui_register.press_register_button_registration()

    assert ui_register.check_is_error_in_field_register('first_name')
    assert ui_register.check_is_error_in_field_register('last_name')
    assert ui_register.check_is_error_in_field_register('username')
    assert ui_register.check_is_error_in_field_register('password')

    ui_register._fill_first_name_field(faker.first_name())
    assert ui_register.check_is_error_in_field_register('first_name') is False
    assert ui_register.check_is_error_in_field_register('last_name')
    assert ui_register.check_is_error_in_field_register('username')
    assert ui_register.check_is_error_in_field_register('password')

    ui_register._fill_last_name_field(faker.last_name())
    assert ui_register.check_is_error_in_field_register('last_name') is False
    assert ui_register.check_is_error_in_field_register('username')
    assert ui_register.check_is_error_in_field_register('password')

    ui_register._fill_username_field(faker.user_name())
    assert ui_register.check_is_error_in_field_register('username') is False
    assert ui_register.check_is_error_in_field_register('password')

    ui_register._fill_password_field(faker.password())
    assert ui_register.check_is_error_in_field_register('password') is False

    assert ui_register.check_title(const.page_title)


@pytest.mark.ui
@pytest.mark.ui_registration
@pytest.mark.negative
@pytest.mark.parametrize(
    'password',
    [faker.password(special_chars=False),
     faker.password(digits=False),
     faker.password(upper_case=False),
     faker.password(lower_case=False)]
)
def test_unsuccess_register(ui_register, password):
    ui_register.fill_register_form(
        faker.first_name(),
        faker.last_name(),
        ui_register.username,
        password,
    )
    ui_register.press_register_button_registration()

    # assert ui_register.check_error_message('invalid_password')
    # ^ Message shows just for a second
    # Also, capcha exists, so right message won`t shown

    assert ui_register.check_title(const.page_title)
    assert ui_register.check_fields_in_register_form_are_not_empty() is False
    # From become empty after submitting.


@pytest.mark.ui
@pytest.mark.ui_registration
@pytest.mark.positive
def test_error_message_invisibility(ui_register):
    assert ui_register.check_is_element_is_invisible(
        const.register_page_id['error_message'])


# False in run is expected
@pytest.mark.ui
@pytest.mark.ui_registration
@pytest.mark.negative
def test_register_already_registered_user(ui_register):
    username = os.getenv('user_name')
    password = os.getenv('password')

    ui_register.fill_register_form(
        faker.first_name(),
        faker.last_name(),
        username,
        password,
    )

    ui_register.press_register_button_registration()

    assert ui_register.check_error_message('user_exists')
    assert ui_register.check_title(const.page_title)
    assert ui_register.check_fields_in_register_form_are_not_empty()
