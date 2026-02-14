from modules.ui.demo_qa import DemoQA

import pytest


@pytest.fixture
def ui():
    user = DemoQA()

    user.go_to()

    yield user

    user.teardown()


@pytest.fixture
def ui_login():
    user = DemoQA()

    user.go_to()
    user.press_login_button()

    yield user

    user.teardown()


@pytest.fixture
def ui_register():
    user = DemoQA()

    user.go_to()
    user.press_login_button()
    user.press_register_button()

    yield user

    user.teardown()
