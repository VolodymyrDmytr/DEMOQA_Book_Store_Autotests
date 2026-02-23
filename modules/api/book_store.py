import requests
from modules.api.account import Account
import logging
import random
from modules.faker_settings import faker

logger = logging.getLogger(__name__)


class BookStore(Account):
    URL_book_store = 'https://demoqa.com/BookStore/v1'

    def __init__(self):
        super().__init__()

    def get_books_list(self) -> requests.Response:
        """Get the list of all books in the book store.

        Returns:
            requests.Response: list of books in Response
        """
        r = requests.get(f'{self.URL_book_store}/Books')
        return r

    def get_book(
            self,
            book_id: str,
    ) -> requests.Response:
        """Get a specific book by its ISBN.

        Args:
            book_id (str): Book ISBN.

        Returns:
            requests.Response: Response contains the book data.
        """
        r = requests.get(f'{self.URL_book_store}/Book?ISBN={book_id}')
        return r

    def post_users_books_list(
            self,
            user_id: str,
            id_list: list,
            token: str,
    ) -> requests.Response:
        """Add books to a user's collection.

        Args:
            user_id (str): ID of existing user
            id_list (list): list of books isbn`s
            token (str): Bearer token

        Returns:
            requests.Response: Contains isbn of added books
        E.g. {"books": [{"isbn": "9781491950296"}]}
        """
        formatted_id_list = []
        for element in id_list:
            isbn_dict = {'isbn': element}
            formatted_id_list.append(isbn_dict)
        logger.debug('formatted list: %s', formatted_id_list)

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

    def delete_all_users_books(
            self,
            user_id: str,
            token: str,
    ) -> requests.Response:
        """Delete all books from a user's collection.

        Args:
            user_id (str): ID of existing user
            token (str): Bearer token

        Returns:
            requests.Response: None in body
        """
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
        """Delete a specific book from a user's collection by ISBN.

        Args:
            book_id (str): book`s isbn in users collection
            user_id (str): ID of existing user
            token (str): Bearer token

        Returns:
            requests.Response: None in body
        """
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
        """Replace one book with another in a user's collection.

        Args:
            user_id (str): ID of existing user
            book_id_old (str): isbn of existing book in users collection
            book_id_new (str): isbn of new book to replace old in users
             collection
            token (str): Bearer token

        Returns:
            requests.Response: userId(str), username(str), books(list)
        """
        header = {
            'Authorization': f'Bearer {token}',
        }

        data = {
            'userId': str(user_id),
            'isbn': str(book_id_new),
        }

        r = requests.put(f'{self.URL_book_store}/Books/{book_id_old}',
                         headers=header, json=data)
        return r

    # Supporting methods
    def get_random_book(self) -> dict:
        """Return a random book's ISBN and its index in the books list.

        Returns:
            dict: 'book_id' and it`s 'book_number'
        result = {
            'book_id': book_id,
            'book_number': rand_int
            }
        """
        r = self.get_books_list()
        body = r.json()
        body = body['books']
        books_count = len(body)

        rand_int = random.randint(0, books_count-1)

        book_id = body[rand_int]['isbn']

        result = {
            'book_id': book_id,
            'book_number': rand_int
        }

        return result

    def get_random_books_list(self, books_count: int) -> list:
        """Return lists of random book ISBNs and their indexes.

        Args:
            books_count (int): how many books needs to be in the lists

        Returns:
            list: 2 lists, with their id and number in book list
        books_id_list, books_number_list
        """

        books_id_list = []
        books_number_list = []

        body = self.get_all_books_list()
        if books_count > len(body):
            logger.info(
                'Chosen book count is more than available. '
                'Requested: %s, available: %s',
                books_count, len(body))
            books_count = len(body)

        for _ in range(books_count):
            check = False
            while check is False:
                random_book = self.get_random_book()

                if random_book['book_id'] not in books_id_list:
                    books_id_list.append(random_book['book_id'])
                    books_number_list.append(random_book['book_number'])
                    check = True

        return books_id_list, books_number_list

    def get_unexisting_book_id(self) -> str:
        """Generate a non-existing ISBN for the book store.

        Returns:
            str: Book`s isbn
        """
        r = self.get_books_list()
        body = r.json()
        body = body['books']

        book_id = body[-1]['isbn'] + '1'

        return book_id

    def get_all_books_list(self) -> list:
        """Return the full list of books for easier access.

        Returns:
            list: List of all books.
        """
        r = self.get_books_list()
        body = r.json()
        books = body['books']

        return books

    def get_users_books(
            self,
            user_id: str,
            token: str,
    ) -> list:
        r = self.get_user(user_id, token)
        body = r.json()
        users_books = body['books']

        return users_books

    def get_random_book_dict(
            self,
    ) -> dict:
        """Return a random book as a dictionary.

        Returns:
            dict: All data for 1 book
        """
        r = self.get_books_list()
        body = r.json()
        body = body['books']
        books_count = len(body)
        rand_int = random.randint(0, books_count-1)
        book = body[rand_int]

        return book

    def no_found_book_title_generator(
            self,
            titles_count: int = 6
    ) -> list:
        """Generate titles that will not be found in the book store.

        Args:
            titles_count (int, optional): Number of titles to generate.
                Defaults to 6.

        Returns:
            list: List of book 'titles'
        """
        books = self.get_all_books_list()
        title_list = []
        for _ in range(titles_count):
            while True:
                add = True
                title = faker.word()

                for element in books:
                    if title in (element['title'], element['author'],
                                 element['publisher']):
                        add = False

                if add is True:
                    title_list.append(title)
                    break
        logger.debug('Title`s list (No found): %s', title_list)
        return title_list


book_store = BookStore()
books = book_store.get_all_books_list()
