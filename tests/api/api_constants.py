class APIconstants:
    password_error_validation_message = (
        "Passwords must have at least one non alphanumeric character,"
        + " one digit ('0'-'9'), one uppercase ('A'-'Z'), one lowercase"
        + " ('a'-'z'), one special character and Password must be eight"
        + " characters or longer."
    )

    fields_are_required = 'UserName and Password required.'

    failed_auth = 'User authorization failed.'
    no_auth = 'User not authorized!'

    user_404 = 'User not found!'
    incorrect_user_id = 'User Id not correct!'

    books_fields = ['isbn', 'title', 'subTitle', 'author', 'publish_date',
                    'publisher', 'pages', 'description', 'website']

    no_such_book_in_users_book_list = ("ISBN supplied is not available in"
                                       + " User's Collection!")
    no_such_book_in_books_list = ("ISBN supplied is not available"
                                  + " in Books Collection!")


const = APIconstants()
