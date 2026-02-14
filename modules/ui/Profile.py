from modules.ui.base_page import BasePage
from modules.ui.table import Table
from modules.ui.ui_constants import const
import logging

logger = logging.getLogger(__name__)


class Profile(BasePage, Table):
    page_id_dict = const.profile_page_id

    def __init__(self):
        super().__init__()

    def press_go_to_book_store_button(self) -> None:
        r = self.driver.find_element(
            *const.profile_page_id['go_to_book_store_button'])
        r.click()

    def press_delete_account_button(self) -> None:
        r = self.driver.find_element(
            *const.profile_page_id['delete_account_button']
        )
        r.click()

    def press_delete_all_books_button(self) -> None:
        r = self.driver.find_element(
            *const.profile_page_id['delete_all_books_button']
        )
        r.click()

    def delete_book(
            self,
            book_number: int,
    ) -> None:
        book_number -= 1

        r = self.driver.find_elements(
            *const.profile_page_id['delete_book_button'])
        r[book_number].click()
