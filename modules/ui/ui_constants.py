from selenium.webdriver.common.by import By


class UIConstants:
    base_url = 'https://demoqa.com/'
    login_url = base_url + 'login'
    book_store_url = base_url + 'books'
    profile_url = base_url + 'profile'

    same_elements_id = {
        'log_out_button': (By.ID, 'submit'),
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
    }

    book_store_page_id = {
        'search_field': (By.ID, 'searchBox'),
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
        'log_out_button': (By.ID, 'submit'),
        'username_text': (By.ID, 'userName-value'),
    }

    profile_page_id = {
        'search': (),
        'go_to_book_store_button': (),
        'delete_account_button': (),
        'delete_all_books_button': (),
        'delete_book_button': (),
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
        'log_out_button': (By.ID, 'submit'),
        'username_text': (By.ID, 'userName-value'),
    }


const = UIConstants()
