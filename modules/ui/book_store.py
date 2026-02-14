from modules.ui.base_page import BasePage
from modules.ui.table import Table
from modules.ui.ui_constants import const
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import logging

logger = logging.getLogger(__name__)


class BookStore(BasePage, Table):
    page_id_dict = const.book_store_page_id

    def __init__(self):
        super().__init__()

    # Book page
    def _get_alert(self):
        alert = WebDriverWait(self.driver, 7).until(
            ec.alert_is_present(),
        )
        return alert

    def press_back_to_store_button(self) -> None:
        r = self.driver.find_element(
            *self.page_id_dict['back_to_store_button']
        )
        r.click()

    def press_add_to_collection_button(self) -> None:
        r = self.driver.find_element(
            *self.page_id_dict['Add_to_collection_button']
        )
        r.click()

    def check_alert_text(
            self,
            book_collection_status: bool,
    ) -> bool:
        """book_collection_status - is book already in collection"""
        alert = self._get_alert()
        text = alert.text

        if book_collection_status is True:
            return text == const.alert_already_exist_in_collection
        elif book_collection_status is False:
            return text == const.alert_book_added_to_collection

    def close_modal_window(self) -> None:
        alert = self._get_alert()
        alert.accept()

    def check_text(
            self,
            field_to_check: str,
            expected_text: str,
    ) -> bool:
        field_to_check = field_to_check.lower().strip() + '_id'
        r = self.driver.find_elements(*const.book_store_page_id['text'])
        actual_text = r[const.book_store_page_id[field_to_check]].text

        return actual_text == expected_text
