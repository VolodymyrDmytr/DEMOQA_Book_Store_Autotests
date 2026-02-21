from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import wait
from selenium.webdriver.support import expected_conditions as ec
import logging
from modules.ui.ui_constants import const
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()


class BasePage:
    URL = const.base_url

    def __init__(self):
        options = Options()
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--log-level=3")
        self.driver = webdriver.Chrome(options=options)
        # Block Ads
        self.driver.execute_cdp_cmd("Network.setBlockedURLs", {
            "urls": ["*google-analytics.com*", "*doubleclick.net*",
                     "*adsbygoogle*"]
        })
        self.driver.execute_cdp_cmd("Network.enable", {})

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
        r = wait.WebDriverWait(self.driver, 10).until(
            lambda d: d.current_url == exp_url
        )
        return r

    def press_log_out_button(
            self,
    ) -> None:
        self.driver.execute_script('window.scroll(0,0)')
        while True:
            try:
                r = WebDriverWait(self.driver, 5).until(
                    ec.element_to_be_clickable(
                        const.book_store_page_id['log_out_button'])
                )
                r.click()
                break
            except StaleElementReferenceException:
                logger.info(
                    'StaleElementReferenceException for log out button')

    def check_username(
            self,
            expected_username: str,
    ) -> bool:
        """Returns True, if username on page is the same with
        expected_username"""
        r = WebDriverWait(self.driver, 5).until(
            ec.visibility_of_element_located(
                const.same_elements_id['username_text'])
        )
        username = r.text

        return expected_username.lower().strip() == username.lower().strip()

    def check_is_element_is_invisible(
            self,
            element: str,
    ) -> bool | False:
        r = wait.WebDriverWait(self.driver, 5).until(
            ec.invisibility_of_element_located(
                element)
        )

        return r
