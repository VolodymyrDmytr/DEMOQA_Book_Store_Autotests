import pytest
from modules.ui.ui_constants import const
from modules.api.book_store import book_store


@pytest.mark.ui
@pytest.mark.ui_profile_page
@pytest.mark.positive
def test_check_username(ui_profile):
    assert ui_profile.check_username(ui_profile.username)


@pytest.mark.ui
@pytest.mark.ui_profile_page
@pytest.mark.positive
def test_log_out_button(ui_profile):
    ui_profile.press_log_out_button()
    assert ui_profile.check_url(const.login_url)


@pytest.mark.ui
@pytest.mark.ui_profile_page
@pytest.mark.positive
def test_collection_is_empty_for_new_user(ui_profile):
    assert ui_profile.check_no_books_found()


@pytest.mark.ui
@pytest.mark.ui_profile_page
@pytest.mark.positive
def test_go_to_book_store_button(ui_profile):
    ui_profile.press_go_to_book_store_button_profile()
    assert ui_profile.check_url(const.book_store_url)


@pytest.mark.ui
@pytest.mark.ui_profile_page
@pytest.mark.positive
def test_profile_book_search(ui_profile_with_books):
    ui_profile_with_books.fill_search_field(
        ui_profile_with_books.books[0]['title']
    )
    assert ui_profile_with_books.check_is_book_expected(
        1,
        ui_profile_with_books.books[0]['title'],
        ui_profile_with_books.books[0]['author'],
        ui_profile_with_books.books[0]['publisher']
    )


@pytest.mark.ui
@pytest.mark.ui_book_store
@pytest.mark.negative
@pytest.mark.parametrize(
    'search_data', book_store.no_found_book_title_generator())
def test_unsuccess_search_profile(ui_profile_with_books, search_data):
    ui_profile_with_books.fill_search_field(search_data)
    assert ui_profile_with_books.check_no_books_found()


@pytest.mark.ui
@pytest.mark.ui_profile_page
@pytest.mark.positive
def test_account_deleting(ui_profile_for_delete):
    ui_profile_for_delete.wait_till_books_loaded()
    ui_profile_for_delete.press_delete_account_button()
    ui_profile_for_delete.actions_with_modal('ok')
    ui_profile_for_delete.actions_with_modal('x')
    ui_profile_for_delete.press_log_out_button()

    ui_profile_for_delete.fill_username_field(ui_profile_for_delete.username)
    ui_profile_for_delete.fill_password_field(ui_profile_for_delete.password)
    ui_profile_for_delete.press_login_button()

    assert ui_profile_for_delete.check_url(const.login_url)
    assert ui_profile_for_delete.check_error_text()


@pytest.mark.ui
@pytest.mark.ui_profile_page
@pytest.mark.positive
def test_account_deleting_modal(ui_profile):
    ui_profile.wait_till_books_loaded()
    ui_profile.press_delete_account_button()
    assert ui_profile.check_modal_text('account')

    ui_profile.actions_with_modal('x')
    assert ui_profile.check_url(const.profile_url)

    ui_profile.actions_with_modal('cancel')
    assert ui_profile.check_url(const.profile_url)


@pytest.mark.ui
@pytest.mark.ui_profile_page
@pytest.mark.positive
def test_book_deleting_modal(ui_profile_with_books):
    ui_profile_with_books.wait_till_books_loaded()

    ui_profile_with_books.press_delete_book_button(
        ui_profile_with_books.books[0]['isbn'])
    ui_profile_with_books.actions_with_modal('x')
    assert ui_profile_with_books.check_is_book_expected(
        1,
        ui_profile_with_books.books[0]['title'],
        ui_profile_with_books.books[0]['author'],
        ui_profile_with_books.books[0]['publisher'],
    )

    ui_profile_with_books.press_delete_book_button(
        ui_profile_with_books.books[0]['isbn'])
    ui_profile_with_books.actions_with_modal('cancel')
    assert ui_profile_with_books.check_is_book_expected(
        1,
        ui_profile_with_books.books[0]['title'],
        ui_profile_with_books.books[0]['author'],
        ui_profile_with_books.books[0]['publisher'],
    )

    ui_profile_with_books.press_delete_book_button(
        ui_profile_with_books.books[0]['isbn'])

    assert ui_profile_with_books.check_modal_text('one book')

    ui_profile_with_books.actions_with_modal('ok')
    assert ui_profile_with_books.check_success_delete_book_alert_text(
        'one_book')
    ui_profile_with_books.accept_alert()
    assert ui_profile_with_books.check_is_book_expected(
        1,
        ui_profile_with_books.books[1]['title'],
        ui_profile_with_books.books[1]['author'],
        ui_profile_with_books.books[1]['publisher'],
    )


@pytest.mark.ui
@pytest.mark.ui_profile_page
@pytest.mark.positive
def test_deleting_all_books_modal(ui_profile_with_books):
    assert ui_profile_with_books.check_is_book_expected(
        2,
        ui_profile_with_books.books[1]['title'],
        ui_profile_with_books.books[1]['author'],
        ui_profile_with_books.books[1]['publisher'],
    )
    assert ui_profile_with_books.check_is_book_expected(
        1,
        ui_profile_with_books.books[0]['title'],
        ui_profile_with_books.books[0]['author'],
        ui_profile_with_books.books[0]['publisher'],
    )

    ui_profile_with_books.press_delete_all_books_button()
    assert ui_profile_with_books.check_modal_text('all books')

    ui_profile_with_books.actions_with_modal('x')
    assert ui_profile_with_books.check_is_book_expected(
        2,
        ui_profile_with_books.books[1]['title'],
        ui_profile_with_books.books[1]['author'],
        ui_profile_with_books.books[1]['publisher'],
    )
    assert ui_profile_with_books.check_is_book_expected(
        1,
        ui_profile_with_books.books[0]['title'],
        ui_profile_with_books.books[0]['author'],
        ui_profile_with_books.books[0]['publisher'],
    )

    ui_profile_with_books.press_delete_all_books_button()
    ui_profile_with_books.actions_with_modal('cancel')
    assert ui_profile_with_books.check_is_book_expected(
        2,
        ui_profile_with_books.books[1]['title'],
        ui_profile_with_books.books[1]['author'],
        ui_profile_with_books.books[1]['publisher'],
    )

    ui_profile_with_books.press_delete_all_books_button()
    assert ui_profile_with_books.check_is_book_expected(
        1,
        ui_profile_with_books.books[0]['title'],
        ui_profile_with_books.books[0]['author'],
        ui_profile_with_books.books[0]['publisher'],
    )

    ui_profile_with_books.actions_with_modal('ok')
    ui_profile_with_books.actions_with_modal('x')
    ui_profile_with_books.press_log_out_button()

    ui_profile_with_books.fill_username_field(ui_profile_with_books.username)
    ui_profile_with_books.fill_password_field(ui_profile_with_books.password)
    ui_profile_with_books.press_login_button()

    assert ui_profile_with_books.check_no_books_found()


@pytest.mark.ui
@pytest.mark.ui_profile_page
@pytest.mark.positive
def test_go_to_book_page(ui_profile_with_books):
    book_id = ui_profile_with_books.books[0]['isbn']
    book_title = ui_profile_with_books.books[0]['title']

    ui_profile_with_books.click_book_link(book_title)

    assert ui_profile_with_books.check_url(
        const.book_url_format.format(book_id))
