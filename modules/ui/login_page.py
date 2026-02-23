from modules.ui.base_page import BasePage
import logging
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import (TimeoutException,
                                        StaleElementReferenceException)
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
        """Fill the username field on the login page.

        Args:
            username (str): Username to enter.
        """
        r = WebDriverWait(self.driver, 5).until(
            ec.visibility_of_element_located(
                const.login_page_id['username_field'])
        )
        r.send_keys(username)

    def fill_password_field(
            self,
            password: str,
    ) -> None:
        """Fill the password field on the login page.

        Args:
            password (str): Password to enter.
        """
        r = WebDriverWait(self.driver, 5).until(
            ec.visibility_of_element_located(
                const.login_page_id['password_field'])
        )
        r.send_keys(password)

    def press_login_button(self) -> None:
        """Click the login button on the login page."""
        while True:
            try:
                r = WebDriverWait(self.driver, 5).until(
                    ec.element_to_be_clickable(
                        const.login_page_id['login_button']))
                logger.info('login button was found!')
                r.click()
                break
            except StaleElementReferenceException:
                logger.info('StaleElementReferenceException for login button')

    def press_register_button_login(self) -> None:
        """Click the 'New user' button on the login page."""
        r = WebDriverWait(self.driver, 5).until(
            ec.element_to_be_clickable(const.login_page_id['register_button']))
        r.click()

    def check_is_error_in_field_login(
            self,
            field_name: str,
    ) -> bool:
        """Check whether a validation error is shown for a field on the
        login page.

        Args:
            field_name (str): username / password

        Returns:
            bool: True if a validation error is shown.
        """
        field_name = field_name.lower().strip() + '_field'

        try:
            r = WebDriverWait(self.driver, 5).until(
                lambda d: 'is-invalid' in d.find_element(
                    *const.login_page_id[field_name]).get_attribute('class')
            )
            return r
        except TimeoutException:
            return False

    def check_error_text(self) -> bool:
        """Check whether the error text is shown after submitting the form
        and matches the expected message.

        Returns:
            bool: True if the error text is shown and matches expected text.
        """
        r = WebDriverWait(self.driver, 5).until(
            ec.visibility_of_element_located(
                const.login_page_id['error_message'])
        )
        text = r.text.strip()

        return text == const.login_error_message

    def confirm_success_registered_alert(self) -> None:
        """Accept the success registration alert."""
        r = WebDriverWait(self.driver, 5).until(
            ec.alert_is_present()
        )
        r.accept()

    def check_alert_success_register_text(self) -> bool:
        """Check is success registration alert text as expected.

        Returns:
            bool: True if the alert text matches the expected message.
        """
        r = WebDriverWait(self.driver, 5).until(
            ec.alert_is_present()
        )
        text = r.text.strip()

        return text == const.alert_success_register_text
