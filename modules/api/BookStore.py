import requests
from modules.api.Account import Account
import logging
import random

logger = logging.getLogger(__name__)


class BookStore(Account):
    URL_book_store = 'https://demoqa.com/BookStore/v1'

    def __init__(self):
        super().__init__()

    def get_books_list(self):
        r = requests.get(f'{self.URL_book_store}/Books')
        return r

    def get_book(
            self,
            book_id: str,
    ) -> requests.Response:
        r = requests.get(f'{self.URL_book_store}/Books?UserId={book_id}')
        return r

    def post_users_books_list(
            self,
            user_id: str,
            id_list: list,
            token: str,
    ) -> requests.Response:
        formatted_id_list = []
        for element in id_list:
            formatted_id_list.append(
                '{' + f"'isbn': {element}" + '}')
        logger.debug('formatted list: %s', formatted_id_list)\

        header = {
            'Authorization': f'Bearer {token}',
        }

        data = {
            'userId': user_id,
            'collectionOfIsbns': formatted_id_list,
        }
        logger.debug('post books method data: %s', data)

        r = requests.post(f'{self.URL_book_store}/Book',
                          headers=header, json=data)
        return r

    def delete_all_users_books(
            self,
            user_id: str,
            token: str,
    ) -> requests.Response:
        header = {
            'Authorization': f'Bearer {token}',
        }

        r = requests.delete(f'{self.URL_book_store}/Books?UserId={user_id}',
                            headers=header)
        return r

    def delete_book_from_users_book_list(
            self,
            book_id: str,
            user_id: str,
            token: str,
    ) -> requests.Response:
        header = {
            'Authorization': f'Bearer {token}',
        }

        data = {
            'isbn': book_id,
            'userId': user_id,
        }

        r = requests.delete(f'{self.URL_book_store}/Book',
                            headers=header, json=data)
        return r

    def change_book_in_users_book_list(
            self,
            user_id: str,
            book_id_old: str,
            book_id_new: str,
            token: str,
    ) -> requests.Response:
        header = {
            'Authorization': f'Bearer {token}',
        }

        data = {
            'userId': user_id,
            'isbn': book_id_new,
        }

        r = requests.put(f'{self.URL_book_store}/Books/{book_id_old}',
                         headers=header, json=data)
        return r

    def get_random_book(self):
        """Returns dict with 'book_id' and it`s 'book_bumber'"""
        r = self.get_books_list()
        body = r.json()
        books_count = len(body)

        rand_int = random.randint(0, books_count-1)

        book_id = body[rand_int]['isbn']

        result = {
            'book_id': book_id,
            'book_number': rand_int
        }

        return result

    def get_random_books_list(self, books_count: int) -> list:
        """Returns 2 lists, with their id and number in book list"""
        books_id_list = []
        books_number_list = []

        r = self.get_books_list()
        body = r.json()

        if books_count > len(body):
            logger.info(
                '''Choosen book lenght is more than books available.
                Choosed count: %s, so all books were added (%s)''',
                books_count, len(body))
            books_count = len(body)

        for i in range(books_count):
            random_book = self.get_random_book()

            if random_book['book_id'] not in books_id_list:
                books_id_list.append({'isbn': random_book['book_id']})
                books_number_list.append(random_book['book_number'])

        return books_id_list, books_number_list

    def get_unexisting_book_id(self) -> str:
        r = self.get_books_list()
        body = r.json()
        body_len = len(body)

        book_id = body[body_len-1]['isbn'] + '1'

        return book_id
