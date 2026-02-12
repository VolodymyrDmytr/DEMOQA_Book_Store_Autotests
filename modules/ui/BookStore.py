from selenium.webdriver.support.select import Select
from modules.ui.BasePage import BasePage
from modules.ui.ui_constants import const
import logging

logger = logging.getLogger(__name__)


class BookStore(BasePage):
    URL = const.book_store_url

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
        button = button.lower().strip() + '_button_check_state'

        r = self.driver.find_element(*const.book_store_page_id[button])
        r = r.is_enabled()
        return r is False

    def change_page(
            self,
            page: int,
    ) -> None:
        r = self.driver.find_element(*const.book_store_page_id['page_field'])
        r.send_keys(page)

    def check_page(
            self,
            exp_page: str | int,
    ) -> bool:
        """Returns True, if current page is expected"""
        r = self.driver.find_element(*const.book_store_page_id['page_field'])

        return r.text.lower().strip() == str(exp_page).lower().strip()

    def select_row_number_on_page(
            self,
            rows_per_page: str,
    ) -> None:
        r = self.driver.find_elements(
            *const.book_store_page_id['rows_per_page_options'])
        if rows_per_page not in r.text:
            logger.warning(
                '''Choosed rows per page is not exist.
                Choosed rows per page: %s''', rows_per_page),

        r = self.driver.find_element(
            *const.book_store_page_id['rows_per_page_select'])
        select = Select(r)
        select.select_by_value(rows_per_page)

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
            full_book_title: str,
    ) -> None:
        by_element, text = const.book_store_page_id
        r = self.driver.find_element(
            by_element,
            text.format(full_book_title)
        )
        r.click()

    def check_element_absence(
            self,
            element: str,
    ) -> bool:
        pass
