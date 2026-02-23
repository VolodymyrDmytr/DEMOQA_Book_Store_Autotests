from faker import Faker
import re

faker = Faker()
Faker.seed(123)

correct_password_setting = (15, True, True, True, True)
password_pattern = ("^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*["
                    + "^a-zA-Z0-9_+\\[\\]\\{\\}\\(\\)]).{8,}$")


def correct_password() -> str:
    """Generates and returns valid password"""
    result = False

    while result is not True:
        password = faker.password(*correct_password_setting)

        if re.fullmatch(password_pattern, password) is not None:
            result = True

    return password
