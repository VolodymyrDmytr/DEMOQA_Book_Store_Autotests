import pytest
import logging
from modules.ui.ui_constants import const
from tests.test_data import data

logger = logging.getLogger(__name__)


@pytest.mark.ui
@pytest.mark.ui_book_store
@pytest.mark.positive
def test_images_are_loaded(ui):
    assert ui.check_are_all_images_loaded()
    assert ui.check_title(const.page_title)


@pytest.mark.ui
@pytest.mark.ui_book_store
@pytest.mark.positive
@pytest.mark.parametrize(
    'search_data, exp_data',
    [(data.books[0]['title'][:3], data.books[0]['title']),
     (data.books[3]['author'][2:], data.books[3]['author']),
     (data.books[6]['publisher'][:5], data.books[6]['publisher'])])
def test_success_search(ui, search_data, exp_data):
    ui.fill_search_field(search_data)
    assert ui.check_is_book_expected(1, exp_data)


@pytest.mark.ui
@pytest.mark.ui_book_store
@pytest.mark.negative
@pytest.mark.parametrize(
    'search_data', data.no_found_for_search)
def test_unsuccess_search(ui, search_data):
    ui.fill_search_field(search_data)
    assert ui.check_no_books_found()


@pytest.mark.ui
@pytest.mark.ui_book_store
@pytest.mark.positive
def test_login_button(ui):
    ui.press_login_button()
    assert ui.check_url(const.login_url)


@pytest.mark.ui
@pytest.mark.ui_book_store
@pytest.mark.positive
def test_table_buttons_are_disabed(ui):
    assert ui.check_is_button_element_active('next')
    assert ui.check_is_button_element_active('previous')


@pytest.mark.ui
@pytest.mark.ui_book_store
@pytest.mark.positive
@pytest.mark.parametrize(
    'book_title', data.books
)
def test_books_links(ui, book_title):
    ui.click_book_link(book_title['title'])
    assert ui.check_url(const.book_url_format.format(book_title['isbn']))


@pytest.mark.ui
@pytest.mark.ui_book_store
@pytest.mark.positive
def test_log_out_button(ui_login):
    ui_login.fill_username_field(ui_login.username)
    ui_login.fill_password_field(ui_login.password)
    ui_login.press_login_button()
    ui_login.press_go_to_book_store_button_profile()

    ui_login.press_log_out_button()
    assert ui_login.check_url(const.login_url)


@pytest.mark.ui
@pytest.mark.ui_book_store
@pytest.mark.positive
def test_is_username_correct(ui_login):
    ui_login.fill_username_field(ui_login.username)
    ui_login.fill_password_field(ui_login.password)
    ui_login.press_login_button()
    ui_login.press_go_to_book_store_button_profile()

    assert ui_login.check_username(ui_login.username)
