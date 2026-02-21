from modules.ui.base_page import BasePage
from modules.ui.ui_constants import const
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import (TimeoutException,
                                        ElementClickInterceptedException,
                                        StaleElementReferenceException)
import logging

logger = logging.getLogger(__name__)


class Profile(BasePage):
    page_id_dict = const.profile_page_id

    def __init__(self):
        super().__init__()

    def _get_alert_profile(self):
        r = WebDriverWait(self.driver, 5).until(
            ec.alert_is_present()
        )
        return r

    def press_go_to_book_store_button_profile(self) -> None:
        while True:
            try:
                self.driver.execute_script('window.scrollBy(0,90)')
                r = WebDriverWait(self.driver, 5).until(
                    ec.element_to_be_clickable(
                        const.profile_page_id['go_to_book_store_button'])
                )
                r.click()
                break
            except TimeoutException:
                logger.info(
                    'Back to book store button not found. Scroll down!')
            except StaleElementReferenceException:
                logger.info(
                    'StaleElementReferenceException error (go to store)'
                )
        self.driver.execute_script('window.scrollBy(0,0)')

    def press_delete_account_button(self) -> None:
        r = WebDriverWait(self.driver, 5).until(
            ec.visibility_of_element_located(
                const.profile_page_id['delete_account_button'])
        )
        r.click()

    def press_delete_all_books_button(self) -> None:
        while True:
            try:
                self.driver.execute_script('window.scrollBy(0,90)')
                r = WebDriverWait(self.driver, 10).until(
                    ec.element_to_be_clickable(
                        const.profile_page_id['delete_all_books_button'])
                )
                logger.info('delete_all_books_button was found')
                r.click()
                logger.info('delete_all_books_button was clicked')
                break
            except TimeoutException:
                logger.info('No element found')
            except ElementClickInterceptedException:
                logger.info('Can not click on delete_all_books_button')

    def press_delete_book_button(
            self,
            book_id: int,
    ) -> None:
        by, element = const.profile_page_id['delete_book_button_format']
        element = element.format(book_id)
        logger.debug('book id to delete: %s', book_id)
        r = WebDriverWait(self.driver, 5).until(
            ec.element_to_be_clickable((by, element))
        )
        r.click()

    def actions_with_modal(
            self,
            action: str,
    ) -> None:
        """action = x / cancel / ok"""
        r = WebDriverWait(self.driver, 10,
                          ignored_exceptions=StaleElementReferenceException
                          ).until(
            ec.visibility_of_element_located(const.profile_page_id['modal'])
        )
        action = action.lower().strip()
        if action == 'x':
            element = const.profile_page_id['modal_x_button']
        elif action == 'cancel':
            element = const.profile_page_id['modal_cancel_button']
        elif action == 'ok':
            element = const.profile_page_id['modal_ok_button']
        else:
            logger.info(
                'Incorrect action was provided to \
                    actions_with_delete_book_modal method. \
                        Provided: %s', action)

        r = WebDriverWait(self.driver, 5).until(
            ec.element_to_be_clickable(element)
        )
        r.click()

    def check_modal_text(
            self,
            deleting: str,
    ) -> bool:
        """deleting_type = one book / all books / account"""
        deleting = deleting.lower().strip()

        if deleting == 'one book':
            exp_title = const.delete_book_modal_title
            exp_text = const.delete_book_modal_text
        elif deleting == 'all books':
            exp_title = const.delete_all_books_modal_title
            exp_text = const.delete_all_books_modal_text
        elif deleting == 'account':
            exp_title = const.delete_account_title
            exp_text = const.delete_account_text
        else:
            logger.info('Wrong deleting_type was provided to check_modal_text \
                method. Provided: %s', deleting)
            return False

        WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable(
                const.profile_page_id['modal_ok_button'])
        )

        r = WebDriverWait(self.driver, 10).until(
            ec.visibility_of_element_located(
                const.profile_page_id['modal_title'])
        )
        title = r.text.strip()

        r = WebDriverWait(self.driver, 5).until(
            ec.visibility_of_element_located(
                const.profile_page_id['modal_text'])
        )
        text = r.text.strip()

        logger.debug('Modal: Title = %s, Text = %s', title, text)

        r_title = (exp_title == title)
        r_text = (exp_text == text)

        if r_title is True and r_text is True:
            return True
        else:
            return False

    def accept_alert(self) -> None:
        alert = self._get_alert_profile()
        alert.accept()

    def check_success_delete_book_alert_text(
            self,
            alert_type: str
    ) -> bool:
        """alert_type: one_book / all_books / all_books_no_book"""
        alert_type = alert_type.lower().strip()
        if alert_type == 'one_book':
            msg = const.delete_one_book_alert
        elif alert_type == 'all_books':
            msg = const.delete_all_books_alert
        elif alert_type == 'all_books_no_book':
            msg = const.delete_books_alert_no_books
        else:
            logger.error('wrong alert type was provided. Provided: %s',
                         alert_type)
            return False

        alert = self._get_alert_profile()

        return alert.text.strip() == msg
