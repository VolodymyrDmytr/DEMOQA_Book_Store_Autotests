# DEMOQA_Book_Store_Autotests
API and UI test automation project for DemoQA Book Store using Pytest, Selenium, and Requests.

Additional used libraries
 - Logging
 - Faker
 - Random
 - os

Problems
 - There is no user list to create method to make unique data for creating unique user.
    Possibly, a local database can be created to handle users that have already been created.
    Deleting test data is required during Autotests, but during debaging tests so users aren`t deleted.
 - Captcha on the registration form
 - Modal windows close after the books list loads. If modal is open
 - Some Error messages exists just for a few moments (Register page)
 - No normal transition to profile page
 - After deleting an account and books in the modal, don`t perform aditional actions (e.g. the modal window does not disappear)

Tests can be added
 - Actions with invalid token

Additional info
 - Tests in test_url file is no more valid (Because of updates)


Auto tests are relevant for the website version dated February 23, 2026.
The site may behave differently after updates.

Tests count: 112
Passing time: 11 min 33 sec
