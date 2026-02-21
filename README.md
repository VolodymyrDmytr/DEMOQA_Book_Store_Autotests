# DEMOQA_Book_Store_Autotests
API and UI test automation project for DemoQA Book Store using Pytest, Selenium, and Requests.

Additional used libraries
 - logging
 - Faker
 - Random
 - os

There is a problem with delete all books button on profile page. So, tests are not stable.
Also
 - capcha on register form

# TODO change register in conftest to something else 

# TODO after merging branches, add getting books can from server, not a constant

# TODO after merging branches, add correct password generator to api tests

# TODO move ui register in conftest to API part
# TODO move ui deliting account in conftest to API part after branch merge
# TODO make different fixtures for tests that requires new user and don`t

# TODO add parametrize to test_profile_book_search after merging (Needs to generate)
# TODO test_go_to_book_page (profile) add parametrize after brench merge
