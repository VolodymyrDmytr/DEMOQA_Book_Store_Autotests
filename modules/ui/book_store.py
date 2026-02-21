from modules.ui.base_page import BasePage
from modules.ui.ui_constants import const
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import logging

logger = logging.getLogger(__name__)


class BookStore(BasePage):
    page_id_dict = const.book_store_page_id

    def __init__(self):
        super().__init__()

    # Book page
    def _get_alert(self):
        alert = WebDriverWait(self.driver, 10).until(
            ec.alert_is_present(),
        )
        return alert

    def press_back_to_store_button(self) -> None:
        r = WebDriverWait(self.driver, 5).until(
            ec.element_to_be_clickable(
                const.book_store_page_id['back_to_store_button'])
        )
        r.click()

    def press_add_to_collection_button(self) -> None:
        r = WebDriverWait(self.driver, 5).until(
            ec.element_to_be_clickable(
                const.book_store_page_id['Add_to_collection_button'])
        )
        logger.info('Add to collection book was clicked')
        r.click()

    def check_alert_text(
            self,
            book_collection_status: bool,
    ) -> bool:
        """book_collection_status - is book already in collection"""
        alert = self._get_alert()
        text = alert.text
        logger.debug('alert text (book page): %s', text)

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
        r = WebDriverWait(self.driver, 5).until(
            ec.visibility_of_all_elements_located(
                const.book_store_page_id['text'])
        )
        r = r[const.book_store_page_id[field_to_check]]
        actual_text = r.text
        logger.debug('Field %s: %s', field_to_check, actual_text)

        return str(actual_text).lower().strip() == (
            str(expected_text).lower().strip())
