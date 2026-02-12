from modules.ui.BasePage import BasePage
from selenium.webdriver.support import wait
from selenium.webdriver.support import expected_conditions as ac
import logging

from modules.ui.ui_constants import const

logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    URL = const.login_url

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

    def check_element_absence(
            self,
            element: str,
    ) -> bool:
        """Returns True, if element is invisible"""
        pass

    def _get_element_id_by_element_name(
            self,
            element_name: str
    ) -> set | False:
        keys = const.login_page_id

        if element_name not in keys:
            logger.warning(
                'No such name element in login_page_id dict constant')
            return False

        r = wait.WebDriverWait(self.driver, 5).until(
            ac.invisibility_of_element_located(
                const.login_page_id[element_name])
        )

        return r
