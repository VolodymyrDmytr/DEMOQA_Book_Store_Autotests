import pytest
from modules.ui.ui_constants import const


@pytest.mark.ui
@pytest.mark.ui_book_page
@pytest.mark.not_logged_in
@pytest.mark.positive
def test_book_data_not_logged_user(ui_book_no_login):
    assert ui_book_no_login.check_url(
        const.book_url_format.format(ui_book_no_login.books[0]['isbn']))
    assert ui_book_no_login.check_text(
        'ISBN', ui_book_no_login.books[0]['isbn'])
    assert ui_book_no_login.check_text(
        'Title', ui_book_no_login.books[0]['title'])
    assert ui_book_no_login.check_text(
        'Author', ui_book_no_login.books[0]['author'])
    assert ui_book_no_login.check_text(
        'Publisher', ui_book_no_login.books[0]['publisher'])
    assert ui_book_no_login.check_text(
        'Total_Pages', ui_book_no_login.books[0]['pages'])
    assert ui_book_no_login.check_text(
        'Description', ui_book_no_login.books[0]['description'])
    assert ui_book_no_login.check_text(
        'Website', ui_book_no_login.books[0]['website'])


@pytest.mark.ui
@pytest.mark.ui_book_page
@pytest.mark.not_logged_in
@pytest.mark.positive
def test_back_to_store_button(ui_book_no_login):
    ui_book_no_login.press_back_to_store_button()
    # ui_book_no_login.press_go_to_book_store_button()
    assert ui_book_no_login.check_url(const.book_store_url)


@pytest.mark.ui
@pytest.mark.ui_book_page
@pytest.mark.not_logged_in
@pytest.mark.positive
def test_no_logged_in_elements(ui_book_no_login):
    assert ui_book_no_login.check_url(
        const.book_url_format.format(ui_book_no_login.books[0]['isbn']))
    assert ui_book_no_login.check_is_element_is_invisible(
        const.book_store_page_id['Add_to_collection_button'])
    assert ui_book_no_login.check_is_element_is_invisible(
        const.book_store_page_id['log_out_button'])
    assert ui_book_no_login.check_is_element_is_invisible(
        const.book_store_page_id['username_text'])


@pytest.mark.ui
@pytest.mark.ui_book_page
@pytest.mark.not_logged_in
@pytest.mark.positive
def test_login_button(ui_book_no_login):
    assert ui_book_no_login.check_url(
        const.book_url_format.format(ui_book_no_login.books[0]['isbn'])
    )
    ui_book_no_login.scroll_to(0)
    ui_book_no_login.press_login_button()
    assert ui_book_no_login.check_url(const.login_url)


@pytest.mark.ui
@pytest.mark.ui_book_page
def test_add_to_collection_button(ui_book_login):
    ui_book_login.press_add_to_collection_button()
    assert ui_book_login.check_alert_text(False)
    ui_book_login.accept_alert()

    ui_book_login.press_add_to_collection_button()
    assert ui_book_login.check_alert_text(True)
    ui_book_login.accept_alert()

    # Move to profile page
    ui_book_login.press_log_out_button()
    ui_book_login.fill_username_field(ui_book_login.username)
    ui_book_login.fill_password_field(ui_book_login.password)
    ui_book_login.press_login_button()

    assert ui_book_login.check_is_book_expected(
        1,
        ui_book_login.books[0]['title'],
        ui_book_login.books[0]['author'],
        ui_book_login.books[0]['publisher'],
    )


@pytest.mark.ui
@pytest.mark.ui_book_page
@pytest.mark.positive
def test_is_username_correct_book_page(ui_book_login):
    assert ui_book_login.check_username(ui_book_login.username)
