from modules.ui.base_page import BasePage
from modules.ui.ui_constants import const


class Register(BasePage):

    def __init__(self):
        super().__init__()

    def press_register_button(self) -> None:
        r = self.driver.find_element(
            *const.register_page_id['register_button_id']
        )
        r.click()

    def press_back_to_login_button(self):
        r = self.driver.find_element(
            *const.register_page_id['back_to_login_id']
        )
        r.click()

    def _fill_first_name_field(
            self,
            data: str,
    ) -> None:
        r = self.driver.find_element(
            *const.register_page_id['first_name_field_id']
        )
        r.send_keys(data)

    def _fill_last_name_field(
            self,
            data: str,
    ) -> None:
        r = self.driver.find_element(
            *const.register_page_id['last_name_field_id']
        )
        r.send_keys(data)

    def _fill_username_field(
            self,
            data: str,
    ) -> None:
        r = self.driver.find_element(
            *const.register_page_id['username_field_id']
        )
        r.send_keys(data)

    def _fill_password_field(
            self,
            data: str,
    ) -> None:
        r = self.driver.find_element(
            *const.register_page_id['password_field_id']
        )
        r.send_keys(data)

    def fill_register_form(
            self,
            first_name: str,
            last_name: str,
            username: str,
            password: str,
    ) -> None:
        self._fill_first_name_field(first_name)
        self._fill_last_name_field(last_name)
        self._fill_username_field(username)
        self._fill_password_field(password)

    def check_is_error_in_field_register(
            self,
            field_name: str,
    ) -> bool:
        field_name = field_name.lower().strip() + 'field_id'
        r = self.driver.find_element(
            *const.register_page_id[field_name]
        )

        return 'is-invalid' in r.get_attribute('class')
