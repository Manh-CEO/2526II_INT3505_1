import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.book import Book  # noqa: E501
from openapi_server.models.book_input import BookInput  # noqa: E501
from openapi_server import util


def books_get():  # noqa: E501
    """Lấy danh sách tất cả các cuốn sách

     # noqa: E501


    :rtype: Union[List[Book], Tuple[List[Book], int], Tuple[List[Book], int, Dict[str, str]]
    """
    return 'do some magic!'


def books_id_get(id):  # noqa: E501
    """Lấy thông tin chi tiết của một cuốn sách

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: Union[Book, Tuple[Book, int], Tuple[Book, int, Dict[str, str]]
    """
    return 'do some magic!'


def books_post(body):  # noqa: E501
    """Thêm một cuốn sách mới

     # noqa: E501

    :param book_input: 
    :type book_input: dict | bytes

    :rtype: Union[Book, Tuple[Book, int], Tuple[Book, int, Dict[str, str]]
    """
    book_input = body
    if connexion.request.is_json:
        book_input = BookInput.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
