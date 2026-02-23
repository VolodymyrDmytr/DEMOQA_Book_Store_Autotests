from modules.ui.book_store import BookStore
from modules.ui.login_page import LoginPage
from modules.ui.profile import Profile
from modules.ui.register_page import Register
from modules.ui.table import Table
from modules.ui.ui_constants import const
from modules.faker_settings import faker, correct_password
import logging
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (StaleElementReferenceException,
                                        ElementClickInterceptedException)
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
logger = logging.getLogger(__name__)


class DemoQA(BookStore, LoginPage, Profile, Register, Table):
    URL = const.base_url

    def __init__(self, books=[]):
        super().__init__(),
        self.username = faker.user_name()
        self.password = correct_password()
        self.books = books

    def go_to(self):
        """Open the Book Store page."""
        self.go_to_url(const.base_url)

        max_i = 5
        i = 0

        while i <= max_i:
            try:
                self.scroll_lower(90)
                r = WebDriverWait(self.driver, 5).until(
                    ec.visibility_of_all_elements_located(
                        const.base_page_element))
                logger.debug('Count of elements: %s', len(r))
                r = r[-1]
                ActionChains(self.driver).scroll_to_element(r).perform()
                r.click()
                break
            except StaleElementReferenceException:
                i += 1
                logger.error('Element not found')
            except ElementClickInterceptedException:
                i += 1
                logger.error('Can not click on element!')

        if i == 4:
            raise Exception("Failed to click element after retries")

        self.scroll_to(0)

    def __str__(self):
        msg = 'Username: {}. Password: {}. Users book list: {}'
        msg = msg.format(self.username, self.password, self.books)
        return msg
