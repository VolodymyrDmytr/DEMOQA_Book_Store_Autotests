from modules.ui.base_page import BasePage
import logging

from modules.ui.ui_constants import const

logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    page_id_dict = const.login_page_id

    def __init__(self):
        super().__init__()

    def fill_username_field(
            self,
            username: str,
    ) -> None:
        r = self.driver.find_element(*const.login_page_id['username_field'])
        r.send_keys(username)

    def fill_password_field(
            self,
            password: str,
    ) -> None:
        r = self.driver.find_element(*const.login_page_id['password_field'])
        r.send_keys(password)

    def press_login_button(self) -> None:
        r = self.driver.find_element(*const.login_page_id['login_button'])
        r.click()

    def press_register_button(self) -> None:
        r = self.driver.find_element(*const.login_page_id['register_button'])
        r.click()

    def press_profile_link(self) -> None:
        r = self.driver.find_element(*const.login_page_id['profile_href'])
        r.click()

    def check_is_error_in_field_login(
            self,
            field_name: str,
    ) -> bool:
        field_name = field_name.lower().strip() + 'field_id'
        r = self.driver.find_element(
            *const.register_page_id[field_name]
        )

        return 'is-invalid' in r.get_attribute('class')

    def check_error_text(self) -> bool:
        r = self.driver.find_element(*const.login_page_id['error_message'])
        text = r.text.strip()

        return text == const.login_error_message
