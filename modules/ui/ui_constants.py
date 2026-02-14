from selenium.webdriver.common.by import By


class UIConstants:
    base_url = 'https://demoqa.com/'
    login_url = base_url + 'login'
    book_store_url = base_url + 'books'
    profile_url = base_url + 'profile'
    register_url = base_url + 'register'

    book_url = 'https://demoqa.com/books?search=9781449337711'
    # TODO ^ need to make it a random book

    page_title = 'demosite'
    error_page_title = 'Error'

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
    }

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
        'book_link_by_name': (By.XPATH, "//a[contains(text(),'{}')]"),
        'log_out_button': (By.ID, 'submit'),
        'login_button': (By.ID, 'login'),
        'images': (By.XPATH, "//img[@alt='book-image']"),
        # Book page
        'back_to_store_button': (),
        'Add_to_collection_button': (),
        'text': (By.XPATH, "//label[@id='userName-value']"),
        'isbn_id': 1,
        'title_id': 2,
        'sub_title_id': 3,
        'author_id': 4,
        'publisher_id': 5,
        'total_pages_id': 6,
        'description_id': 7,
        'website_id': 8,
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
        'delete_book_button': (By.ID, 'delete-record-undefined'),
        'log_out_button': (
            By.XPATH,
            '//button[contains(text(),"Log out")]'
        ),
    }


const = UIConstants()
