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
        """Open tab with provided URL

        Args:
            url (str): Target URL to open.
        """
        self.driver.get(url)

    def close(self) -> None:
        """Close the current browser tab."""
        self.driver.close()

    def teardown(self) -> None:
        """Quit the browser and close all windows."""
        self.driver.quit()

    def check_title(self, expected_title) -> bool:
        """Check whether the current page title matches the expected title.

        Args:
            expected_title (str): Expected page title.

        Returns:
            bool: True if the titles match, otherwise False.
        """
        return self.driver.title == expected_title

    def check_url(
            self,
            exp_url: str,
    ) -> bool:
        """Check whether the current page URL matches the expected URL.

        Args:
            exp_url (str): Expected URL.

        Returns:
            bool: True if the URLs match, otherwise False.
        """
        r = wait.WebDriverWait(self.driver, 10).until(
            lambda d: d.current_url == exp_url
        )
        return r

    def press_log_out_button(
            self,
    ) -> None:
        """Click the Log Out button (available on most pages)."""
        self.scroll_to(0)
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
        """Check whether the displayed username matches the expected one.

        Args:
            expected_username (str): Expected username shown on the page.

        Returns:
            bool: True if the displayed username matches `expected_username`.
        """

        r = WebDriverWait(self.driver, 5).until(
            ec.visibility_of_element_located(
                const.same_elements_id['username_text'])
        )
        username = r.text

        return expected_username.lower().strip() == username.lower().strip()

    def check_is_element_is_invisible(
            self,
            element: str,
    ) -> bool:
        """Check whether an element exists but is invisible.

        Args:
            element (str): Element locator.

        Returns:
            bool: True if the element exists but is invisible.
        """
        r = wait.WebDriverWait(self.driver, 5).until(
            ec.invisibility_of_element_located(
                element)
        )

        return r

    def scroll_to(self, on: int) -> None:
        """Scroll the page to an absolute vertical position.

        Args:
            on (int): Vertical pixel position to scroll to.
        """
        self.driver.execute_script(f"window.scroll(0,{on})")

    def scroll_lower(self, by: int) -> None:
        """Scroll the page by a relative vertical offset downward.

        Args:
            by (int): Number of pixels to scroll down by.
        """
        self.driver.execute_script(f"window.scrollBy(0,{by})")
