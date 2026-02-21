from modules.ui.base_page import BasePage
from modules.ui.ui_constants import const
import logging
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException

logger = logging.getLogger(__name__)


class Register(BasePage):

    def __init__(self):
        super().__init__()

    def press_register_button_registration(self) -> None:
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
        field_name = field_name.lower().strip() + '_field_id'
        r = self.driver.find_element(
            *const.register_page_id[field_name]
        )

        return 'is-invalid' in r.get_attribute('class')

    def check_error_message(
            self,
            message_type: str,
    ) -> bool:
        """message_type = user_exists / invalid_password"""
        if message_type == 'user_exists':
            message = const.user_exists_error
        elif message_type == 'invalid_password':
            message = const.invalid_password
        else:
            logger.info(
                '''invalid message_type was provided to
                check_error_message method. Provided: %s''',
                message_type)
        try:
            r = WebDriverWait(self.driver, 5).until(
                ec.text_to_be_present_in_element(
                    const.register_page_id['error_message'], message)
            )
        except TimeoutException:
            return False

        return r

    def check_fields_in_register_form_are_not_empty(self) -> bool:
        result_list = []
        result = True

        r = self.driver.find_element(
            *const.register_page_id['first_name_field_id'])
        result_list.append(r.text.strip() != "")

        r = self.driver.find_element(
            *const.register_page_id['last_name_field_id'])
        result_list.append(r.text.strip() != "")

        r = self.driver.find_element(
            *const.register_page_id['username_field_id'])
        result_list.append(r.text.strip() != "")

        r = self.driver.find_element(
            *const.register_page_id['password_field_id'])
        result_list.append(r.text.strip() != "")

        for element in result_list:
            if element is False:
                result = False
                break

        return result
