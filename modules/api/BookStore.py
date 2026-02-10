import requests
from modules.api.Account import Account
import logging

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

        r = requests.post(f'{self.URL_book_store}/Books',
                          headers=header, json=data)
        return r

    def delete_users_books_list(
            self,
            book_id: str,
            token: str,
    ) -> requests.Response:
        header = {
            'Authorization': f'Bearer {token}',
        }

        r = requests.delete(f'{self.URL_book_store}/Books?UserId={book_id}',
                            headers=header)
        return r

    def delete_book_from_users_list(
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
