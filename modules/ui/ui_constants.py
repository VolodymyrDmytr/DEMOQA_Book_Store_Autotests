from selenium.webdriver.common.by import By


class UIConstants:
    base_url = 'https://demoqa.com/'
    login_url = base_url + 'login'
    book_store_url = base_url + 'books'
    profile_url = base_url + 'profile'
    register_url = base_url + 'register'
    book_url_format = base_url + 'books?search={}'

    page_title = 'demosite'
    error_page_title = 'Error'

    base_page_element = (By.CLASS_NAME, 'card-up')

    same_elements_id = {
        'username_text': (By.ID, 'userName-value'),
        'next_button': (By.CLASS_NAME, '-next'),
        'next_button_check_state': (
            By.XPATH,
            "//button[normalize-space()='Next']"),
        'previous_button': (By.CLASS_NAME, '-previous'),
        'previous_button_check_state': (
            By.XPATH,
            "//button[normalize-space()='Previous']"),
        'page_field': (By.XPATH, '//input[@type="number"]'),
        'rows_per_page_select': (By.TAG_NAME, 'select'),
        'rows_per_page_options': (By.TAG_NAME, 'option'),
        'table_rows': (By.CLASS_NAME, 'rt-tr-group'),
        'book_link_by_name': (By.LINK_TEXT, '{}'),
    }

    login_page_id = {
        'username_field': (By.ID, 'userName'),
        'password_field': (By.ID, 'password'),
        'login_button': (By.ID, 'login'),
        'register_button': (By.ID, 'newUser'),
        'profile_href': (By.LINK_TEXT, 'profile'),
        'log_out_button': (By.ID, 'submit'),
        'username_text': (By.ID, 'userName-value'),
        'error_message': (By.ID, 'name')
    }
    login_error_message = 'Invalid username or password!'

    register_page_id = {
        'first_name_field_id': (By.ID, 'firstname'),
        'last_name_field_id': (By.ID, 'lastname'),
        'username_field_id': (By.ID, 'userName'),
        'password_field_id': (By.ID, 'password'),
        'register_button_id': (By.ID, 'register'),
        'back_to_login_id': (By.ID, 'gotologin'),
        'error_message': (By.ID, 'output')
    }
    user_exists_error = 'User exists !'
    invalid_password = ("Passwords must have at least one non alphanumeric "
                        + "character, one digit ('0'-'9'), one uppercase "
                        + "('A'-'Z'), one lowercase ('a'-'z'), one special "
                        + "character and Password must be eight characters or "
                        + "longer.")
    alert_success_register_text = 'User registered!'

    book_store_page_id = {
        # Main page
        'search_field': (By.ID, 'searchBox'),
        'next_button': (
            By.XPATH,
            "//button[normalize-space()='Next']"),
        'previous_button': (
            By.XPATH,
            "//button[normalize-space()='Previous']"),
        'table_rows': (By.TAG_NAME, 'tr'),
        'second_table_row': (By.XPATH, '(//tr)[2]'),
        'book_link_by_name': (By.LINK_TEXT, '{}'),
        # (By.XPATH, "//a[contains(text(),'{}')]"),
        'log_out_button': (By.ID, 'submit'),
        'login_button': (By.ID, 'login'),
        'images': (By.XPATH, "//img[@alt='book-image']"),
        # Book page
        'back_to_store_button': (
            By.XPATH, "(//button[@id='addNewRecordButton'])[1]"),
        'Add_to_collection_button': (
            By.XPATH, "(//button[@id='addNewRecordButton'])[2]"),
        'username_text': (By.XPATH, "(//label[@id='userName-value'])[1]"),
        'text': (By.XPATH, "//label[@id='userName-value']"),
        'isbn_id': 0,
        'title_id': 1,
        'sub_title_id': 2,
        'author_id': 3,
        'publisher_id': 4,
        'total_pages_id': 5,
        'description_id': 6,
        'website_id': 7,
    }

    alert_already_exist_in_collection = (
        'Book already present in the your collection!')
    alert_book_added_to_collection = 'Book added to your collection.'

    profile_page_id = {
        'go_to_book_store_button': (By.ID, 'gotoStore'),
        'delete_account_button': (
            By.XPATH, "//button[contains(text(),'Delete Account')]"),
        'delete_all_books_button': (
            By.XPATH,
            "//button[contains(text(),'Delete All Books')]"
        ),
        'delete_book_button_format': (By.ID, 'delete-record-{}'),
        'log_out_button': (
            By.XPATH,
            '//button[contains(text(),"Log out")]'
        ),
        'modal_x_button': (By.CLASS_NAME, 'btn-close'),
        'modal_cancel_button': (By.ID, 'closeSmallModal-cancel'),
        'modal_ok_button': (By.ID, 'closeSmallModal-ok'),
        'modal_title': (By.ID, 'example-modal-sizes-title-sm'),
        'modal_text': (By.CLASS_NAME, 'modal-body'),
        'modal': (By.CLASS_NAME, 'modal-content'),
    }
    delete_book_modal_title = 'Delete Book'
    delete_book_modal_text = 'Do you want to delete this book?'

    delete_all_books_modal_title = 'Delete All Books'
    delete_all_books_modal_text = 'Do you want to delete all books?'

    delete_account_title = 'Delete Account'
    delete_account_text = 'Do you want to delete your account?'

    delete_books_alert_no_books = "No books available in your's collection!"
    delete_all_books_alert = 'All books deleted'
    delete_one_book_alert = 'Book deleted.'


const = UIConstants()
