from modules.ui.base_page import BasePage
from modules.ui.ui_constants import const
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import logging
from selenium.common.exceptions import (TimeoutException,
                                        ElementClickInterceptedException)

logger = logging.getLogger(__name__)


class Table(BasePage):

    def __init__(self):
        super().__init__()

    def fill_search_field(
            self,
            search: str,
    ) -> None:
        """Fill the search field on the Book Store or Profile pages.

        Args:
            search (str): Search text to enter.
        """
        r = WebDriverWait(self.driver, 5).until(
            ec.visibility_of_element_located(
                const.book_store_page_id['search_field'])
        )
        r.send_keys(search)

    def click_previous_button(self) -> None:
        """Click the 'Previous' pagination button."""
        r = self.driver.find_element(
            *const.book_store_page_id['previous_button'])
        r.click()

    def click_next_button(self) -> None:
        """Click the 'Next' pagination button."""
        r = self.driver.find_element(*const.book_store_page_id['next_button'])
        r.click()

    def check_is_button_element_active(
            self,
            button: str,
    ) -> bool:
        """Check the status of table navigation buttons.

        Args:
            button (str): Next / Previous

        Returns:
            bool: True if the specified button is disabled.
        """
        button = button.lower().strip() + '_button'
        self.scroll_to(700)
        r = WebDriverWait(self.driver, 5).until(
            ec.visibility_of_element_located(const.book_store_page_id[button])
        )
        r = r.is_enabled()
        return r is False

    def check_is_book_expected(
            self,
            row: int,
            title: str = "",
            author: str = "",
            publisher: str = "",
    ) -> bool:
        """Check whether expected information exists on a specific table row
        (Book Store and Profile pages).

        Args:
            row (int): Row index to check.
            title (str, optional): Expected title. Defaults to "".
            author (str, optional): Expected author. Defaults to "".
            publisher (str, optional): Expected publisher. Defaults to "".

        Returns:
            bool: True if the provided data matches the row contents.
        """
        """Returns  (Book store and profile pages)"""
        self.wait_till_books_loaded()

        logger.debug('Data to compare: title = %s, author = %s, publshr = %s',
                     title, author, publisher)
        r_list = []
        result = True
        try:
            r = WebDriverWait(self.driver, 10).until(
                ec.visibility_of_all_elements_located(
                    const.book_store_page_id['table_rows'])
            )
        except TimeoutException:
            logger.info('Book not found')
            return False
        logger.debug('Rows: %s', r)
        table_row = r[row].text
        logger.debug('Row was found: %s', table_row)

        if title != "":
            r = (title in table_row)
            r_list.append(r)
        if author != "":
            r = (author in table_row)
            r_list.append(r)
        if publisher != "":
            r = (publisher in table_row)
            r_list.append(r)

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

    def check_no_books_found(self) -> bool:
        """Check whether the table is empty (no books found).

        Returns:
            bool: True if the table is empty.
        """
        r = WebDriverWait(self.driver, 5).until(
            ec.invisibility_of_element_located(
                const.book_store_page_id['second_table_row'])
        )
        return r

    def click_book_link(
            self,
            book_title: str,
    ) -> None:
        """Click a book link by its full title.

        Args:
            book_title (str): Full book title to click.
        """
        by_element, text = const.book_store_page_id['book_link_by_name']
        logger.debug('Book title: %s', book_title)

        i = 0
        max_i = 3

        while i <= max_i:
            try:
                self.scroll_lower(120)
                r = WebDriverWait(self.driver, 5).until(
                    ec.element_to_be_clickable(
                        (by_element,
                         text.format(book_title),)
                    )
                )
                r.click()
                break
            except TimeoutException:
                i += 1
            except ElementClickInterceptedException:
                i += 1
        if i == 4:
            raise Exception('Too many retries!')

    def check_are_all_images_loaded(self) -> bool:
        """Check whether all books images are loaded on the page.

        Returns:
            bool: True if all images for books are loaded.
        """
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

    def wait_till_books_loaded(self) -> None:
        """Wait until the books table is updated to avoid modal window
        interference while loading.
        """
        r = WebDriverWait(self.driver, 5).until(
                ec.visibility_of_all_elements_located(
                    const.book_store_page_id['table_rows']))
        rows_len = len(r)

        try:
            WebDriverWait(self.driver, 10).until(
                lambda d: len(d.find_elements(
                    *const.book_store_page_id['table_rows'])) != rows_len
            )
        except TimeoutException:
            pass
