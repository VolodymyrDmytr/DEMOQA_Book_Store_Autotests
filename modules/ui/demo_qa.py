from modules.ui.book_store import BookStore
from modules.ui.login_page import LoginPage
from modules.ui.profile import Profile
from modules.ui.register_page import Register
from modules.ui.ui_constants import const


class DemoQA(BookStore, LoginPage, Profile, Register):
    URL = const.book_store_url
