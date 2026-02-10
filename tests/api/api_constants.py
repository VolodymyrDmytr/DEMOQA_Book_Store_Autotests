class APIconstants:
    a = "Passwords must have at least one non alphanumeric character,"
    a += " one digit ('0'-'9'), one uppercase ('A'-'Z'), one lowercase"
    a += " ('a'-'z'), one special character and Password must be eight"
    a += " characters or longer."
    password_error_validation_message = a

    fields_are_required = 'UserName and Password required.'

    failed_auth = 'User authorization failed'
    no_auth = 'User not authorized!'

    user_404 = 'User not found!'
    incorrect_user_id = 'User Id not correct!'


const = APIconstants()
