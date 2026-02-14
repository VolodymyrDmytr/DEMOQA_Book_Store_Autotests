from modules.ui.base_page import BasePage
from modules.ui.ui_constants import const
from selenium.webdriver.support.wait import WebDriverWait
import logging

logger = logging.getLogger(__name__)


class Table(BasePage):

    def __init__(self):
        super().__init__()

    def fill_search_field(
            self,
            search: str,
    ) -> None:
        r = self.driver.find_element(*const.book_store_page_id['search_field'])
        r.send_keys(search)

    def click_previous_button(self) -> None:
        r = self.driver.find_element(
            *const.book_store_page_id['previous_button'])
        r.click()

    def click_next_button(self) -> None:
        r = self.driver.find_element(*const.book_store_page_id['next_button'])
        r.click()

    def check_is_button_element_active(
            self,
            button: str,
    ) -> bool:
        """Returns True, if element is disable.
        Button var takes Next / Previous"""
        button = button.lower().strip() + '_button'

        r = self.driver.find_element(*const.book_store_page_id[button])
        r = r.is_enabled()
        return r is False

    def check_is_book_expected(
            self,
            row: int,
            title: str = "",
            author: str = "",
            publisher: str = "",
    ) -> bool:
        """Returns True, if data on choosed row is expected"""
        r_list = []
        row -= 1
        result = True

        r = self.driver.find_elements(*const.book_store_page_id['table_rows'])
        table_row = r[row]
        table_row = table_row.text.lower().strip()

        if title != "":
            r_list.append(title.lower().strip() in table_row)
        if author != "":
            r_list.append(author.lower().strip() in table_row)
        if publisher != "":
            r_list.append(publisher.lower().strip() in table_row)

        if len(r_list) >= 1:
            for element in r_list:
                if element is False:
                    result = False
                    break
            return result
        else:
            logger.info(
                'No data was provided to check_is_book_expected method')
            return False

    def click_book_link(
            self,
            book_title: str,
    ) -> None:
        by_element, text = const.book_store_page_id
        r = self.driver.find_element(
            by_element,
            text.format(book_title)
        )
        r.click()

    def check_is_all_images_loaded(self) -> bool:
        result_list = []
        result = True

        r = WebDriverWait(self.driver, 5).until(
            lambda d: d.find_elements(*const.book_store_page_id['images'])
        )

        for i in range(len(r)-1):
            result_list.append(
                self.driver.execute_script(
                    'return arguments[0].naturalWidth > 0', r[i]
                )
            )

        for element in result_list:
            if element is False:
                result = False
                break

        return result
