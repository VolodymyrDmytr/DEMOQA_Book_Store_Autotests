from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from modules.ui.ui_constants import const


class BasePage:
    URL = const.base_url

    def __init__(self):
        options = Options()
        options.add_argument("--window-size=1920,1080")
        options.add_experimental_option('prefs', BasePage.prefs)
        self.driver = webdriver.Chrome(options=options)

    def go_to(self):
        self.driver.get(self.URL)

    def close(self):
        self.driver.close()

    def teardown(self):
        self.driver.quit()

    def check_title(self, expected_title) -> bool:
        return self.driver.title == expected_title

    def press_log_out_button(self) -> None:
        r = self.driver.find_element(*const.same_elements_id['log_out_button'])
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
