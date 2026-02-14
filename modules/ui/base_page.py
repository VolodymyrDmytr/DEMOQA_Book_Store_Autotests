from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import wait
from selenium.webdriver.support import expected_conditions as ac
import logging
from modules.ui.ui_constants import const

logger = logging.getLogger(__name__)


class BasePage:
    URL = const.base_url
    page_id_dict = {}

    def __init__(self):
        options = Options()
        options.add_argument("--window-size=1920,1080")
        options.add_experimental_option('prefs', BasePage.prefs)
        self.driver = webdriver.Chrome(options=options)

    def go_to(self):
        self.driver.get(self.URL)
    
    def go_to_url(
            self,
            url: str,
    ) -> None:
        self.driver.get(url)

    def close(self):
        self.driver.close()

    def teardown(self):
        self.driver.quit()

    def check_title(self, expected_title) -> bool:
        return self.driver.title == expected_title

    def check_url(
            self,
            exp_url: str,
    ) -> bool:
        r = wait.WebDriverWait(self.driver, 5).until(
            lambda d: d.current_url == exp_url
        )
        return r

    def press_log_out_button(
            self,
    ) -> None:
        r = self.driver.find_element(*self.page_id_dict['log_out_button'])
        r.click()

    def check_username(
            self,
            expected_username: str,
    ) -> bool:
        """Returns True, if username on page is the same with
        expected_username"""
        r = self.driver.find_element(*const.same_elements_id['username_text'])
        username = r.text

        return expected_username.lower().strip() == username.lower().strip()

    def check_is_element_is_invisible(
            self,
            element_name: str,
    ) -> bool | False:
        keys = self.page_id_dict

        if element_name not in keys:
            logger.warning(
                'No such name element in login_page_id dict constant')
            return False

        r = wait.WebDriverWait(self.driver, 5).until(
            ac.invisibility_of_element_located(
                self.page_id_dict[element_name])
        )

        return r
