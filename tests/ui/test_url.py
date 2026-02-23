# Tests are not valid

import pytest
from modules.ui.ui_constants import const
from modules.api.book_store import book_store


@pytest.mark.ui
@pytest.mark.ui_urls
def test_login_page(ui):
    ui.go_to_url(const.login_url)
    assert ui.check_title(const.error_page_title)


@pytest.mark.ui
@pytest.mark.ui_urls
def test_register_page(ui):
    ui.go_to_url(const.register_url)
    assert ui.check_title(const.error_page_title)


@pytest.mark.ui
@pytest.mark.ui_urls
def test_profile_page(ui):
    ui.go_to_url(const.profile_url)
    assert ui.check_title(const.error_page_title)


@pytest.mark.ui
@pytest.mark.ui_urls
def test_book_page(ui):
    book = book_store.get_random_book()
    ui.go_to_url(const.book_url_format.format(book['book_id']))
    assert ui.check_title(const.error_page_title)


@pytest.mark.ui
@pytest.mark.ui_urls
def test_book_store_page(ui):
    ui.go_to_url(const.book_store_url)
    assert ui.check_title(const.error_page_title)
