import pytest
import logging
from http import HTTPStatus
from tests.api.api_constants import const
import random

logger = logging.getLogger(__name__)


@pytest.mark.api
@pytest.mark.api_book_store
@pytest.mark.api_book_store_books_list
@pytest.mark.positive
def test_books_list(api):
    r = api.get_books_list()
    body = r.json()

    assert r.status_code == HTTPStatus.OK.value
    assert len(body) == 9

    for i in range(len(body)-1):
        assert body[i].keys() == const.books_fields


@pytest.mark.api
@pytest.mark.api_book_store
@pytest.mark.api_book_store_book
@pytest.mark.positive
def test_get_book(api):
    random_book = api.get_random_book()

    r = api.get_books_list()
    body = r.json()
    book_in_list = body[random_book['book_number']]

    r = api.get_book(random_book['book_id'])
    body = r.json()

    assert r.status_code == HTTPStatus.OK.value

    for element in const.books_fields:
        assert body[element] == book_in_list[element]


@pytest.mark.api
@pytest.mark.api_book_store
@pytest.mark.api_book_store_book
@pytest.mark.negative
def test_get_unexisting_book(api):
    book_id = api.get_unexisting_book_id()

    r = api.get_book(book_id)
    body = r.json()

    assert r.status_code == HTTPStatus.BAD_REQUEST.value
    assert body['code'] == '1205'
    assert body['message'] == const.no_such_book_in_books_list


@pytest.mark.api
@pytest.mark.api_book_store
@pytest.mark.api_book_store_adding_books_to_users_list
@pytest.mark.positive
def test_adding_books_in_users_list_and_check_them_in_users_list(my_user):
    books_id_list, books_number_list = my_user.get_random_books_list(3)

    # Adding books
    r = my_user.post_users_books_list(
        my_user.user_id, books_id_list, my_user.token)
    body = r.json()

    assert r.status_code == HTTPStatus.CREATED.value

    for i in range(len(body)):
        assert body[i]['isbn'] == books_id_list[i]

    # Checking books presence and data correctness in users list
    r = my_user.get_user(my_user.user_id, my_user.token)
    body = r.json()
    users_books = body['books']

    assert r.status_code == HTTPStatus.OK.value

    r = my_user.get_books_list()
    all_books_list = r.json()

    for i in range(users_books):
        for element in users_books:
            for keys in const.books_fields:
                assert (element[i][keys] ==
                        all_books_list[books_number_list[i]][keys])

    my_user.delete_all_users_books(my_user.user_id, my_user.token)


@pytest.mark.api
@pytest.mark.api_book_store
@pytest.mark.positive
def test_deleting_book_from_users_list(my_user):
    books_id_list, books_number_list = my_user.get_random_books_list(3)

    my_user.post_users_books_list(
        my_user.user_id, books_id_list, my_user.token)

    number = random.randint(0, len(books_id_list)-1)

    book_id_to_delete = books_id_list[number]
    book_number_to_delete = books_number_list[number]

    del books_number_list[number]
    del books_id_list[number]

    r = my_user.delete_book_from_users_book_list(
        book_id_to_delete, my_user.user_id, my_user.token)

    assert r.status_code == HTTPStatus.NO_CONTENT.value
    assert r.text == ""

    # Check that book still exist in all books list
    r = my_user.get_books_list()
    all_books_list = r.json()

    assert all_books_list[book_number_to_delete]['isbn'] == book_id_to_delete

    r = my_user.get_user(my_user.user_id, my_user.token)
    body = r.json()
    users_book_list = body['books']

    assert r.status_code == HTTPStatus.OK.value

    for i in range(len(users_book_list)):
        for element in users_book_list:
            for key in const.books_fields:
                element[i][key] == all_books_list[books_number_list[i]][key]

    my_user.delete_all_users_books(my_user.user_id, my_user.token)


@pytest.mark.api
@pytest.mark.api_book_store
@pytest.mark.negative
def test_deleting_unexisting_book_from_users_list(my_user):
    random_book = my_user.get_random_book()

    my_user.post_users_books_list(
        my_user.user_id, {"isbn": random_book['book_id']}, my_user.token)

    my_user.delete_book_from_users_book_list(
        random_book['book_id'], my_user.user_id, my_user.token)

    r = my_user.delete_book_from_users_book_list(
        random_book['book_id'], my_user.user_id, my_user.token)
    body = r.json()

    assert r.status_code == HTTPStatus.BAD_REQUEST.value
    assert body['code'] == '1206'
    assert body['message'] == const.no_such_book_in_users_book_list


@pytest.mark.api
@pytest.mark.api_book_store
@pytest.mark.positive
def test_deleting_all_users_books(my_user):
    books_id_list = my_user.get_random_books_list(3)
    books_id_list = books_id_list[0]

    my_user.post_users_books_list(
        my_user.user_id, books_id_list, my_user.token)

    r = my_user.delete_all_users_books(my_user.user_id, my_user.token)

    assert r.status_code == HTTPStatus.NO_CONTENT.value
    assert r.text == ""

    r = my_user.get_user(my_user.user_id, my_user.token)
    body = r.json()

    assert body['books'] == []


@pytest.mark.api
@pytest.mark.api_book_store
@pytest.mark.negative
def test_deleting_all_users_books_twice(my_user):
    books_id_list = my_user.get_random_books_list(3)
    books_id_list = books_id_list[0]

    my_user.post_users_books_list(
        my_user.user_id, books_id_list, my_user.token)

    my_user.delete_all_users_books(my_user.user_id, my_user.token)
    r = my_user.delete_all_users_books(my_user.user_id, my_user.token)

    assert r.status_code == HTTPStatus.NO_CONTENT.value
    assert r.text == ""


@pytest.mark.api
@pytest.mark.api_book_store
@pytest.mark.positive
def test_changing_users_book(my_user):
    random_book_1 = my_user.get_random_book()

    my_user.post_users_books_list(
        my_user.user_id, {"isbn": random_book_1['book_id']}, my_user.token)

    result = False
    while result is False:
        random_book_2 = my_user.get_random_book()

        if random_book_1['book_id'] != random_book_2['book_id']:
            result = True

    r = my_user.change_book_in_users_book_list(
        my_user.user_id,
        random_book_1['book_id'],
        random_book_2['book_id'],
        my_user.token
    )

    assert r.status_code == HTTPStatus.OK.value

    r = my_user.get_books_list()
    all_books_list = r.json()
    changed_book = all_books_list[random_book_2['book_number']]

    r = my_user.get_user(my_user.user_id, my_user.token)
    body = r.json()
    users_book = body['books'][0]

    for key in const.books_fields:
        assert users_book[key] == changed_book[key]


@pytest.mark.api
@pytest.mark.api_book_store
@pytest.mark.negative
def test_changing_users_book_on_the_same(my_user):
    random_book = my_user.get_random_book()

    my_user.post_users_books_list(
        my_user.user_id, {"isbn": random_book['book_id']}, my_user.token)

    r = my_user.change_book_in_users_book_list(
        my_user.user_id,
        random_book['book_id'],
        random_book['book_id'],
        my_user.token
    )

    assert r.status_code == HTTPStatus.OK.value

    r = my_user.get_books_list()
    all_books_list = r.json()
    changed_book = all_books_list[random_book['book_number']]

    r = my_user.get_user(my_user.user_id, my_user.token)
    body = r.json()
    users_book = body['books'][0]

    for key in const.books_fields:
        assert users_book[key] == changed_book[key]


@pytest.mark.api
@pytest.mark.api_book_store
@pytest.mark.negative
def test_changing_users_book_on_unexisting(my_user):
    random_book = my_user.get_random_book()

    my_user.post_users_books_list(
        my_user.user_id, {"isbn": random_book['book_id']}, my_user.token)

    r = my_user.change_book_in_users_book_list(
        my_user.user_id,
        random_book['book_id'],
        my_user.get_unexisting_book_id(),
        my_user.token
    )

    assert r.status_code == HTTPStatus.OK.value

    r = my_user.get_books_list()
    all_books_list = r.json()
    changed_book = all_books_list[random_book['book_number']]

    r = my_user.get_user(my_user.user_id, my_user.token)
    body = r.json()
    users_book = body['books'][0]

    for key in const.books_fields:
        assert users_book[key] == changed_book[key]
