import pytest
from modules.ui.ui_constants import const
from tests.test_data import data


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
    ui.go_to_url(const.book_url_format.format(data.random_book_id))
    assert ui.check_title(const.error_page_title)


@pytest.mark.ui
@pytest.mark.ui_urls
def test_book_store_page(ui):
    ui.go_to_url(const.book_store_url)
    assert ui.check_title(const.error_page_title)
