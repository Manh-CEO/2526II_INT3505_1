import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.book import Book  # noqa: E501
from openapi_server.models.book_input import BookInput  # noqa: E501
from openapi_server.models.get_books_id404_response import GETBooksId404Response  # noqa: E501
from openapi_server import util


def g_et_books():  # noqa: E501
    """g_et_books

    Lß║Ñy danh s├ích tß║Ñt cß║ú c├íc cuß╗æn s├ích # noqa: E501


    :rtype: Union[List[Book], Tuple[List[Book], int], Tuple[List[Book], int, Dict[str, str]]
    """
    return 'do some magic!'


def g_et_books_id(id):  # noqa: E501
    """g_et_books_id

    Lß║Ñy th├┤ng tin chi tiß║┐t cß╗ºa mß╗Öt cuß╗æn s├ích # noqa: E501

    :param id: 
    :type id: str

    :rtype: Union[Book, Tuple[Book, int], Tuple[Book, int, Dict[str, str]]
    """
    return 'do some magic!'


def p_ost_books(body):  # noqa: E501
    """p_ost_books

    Th├¬m mß╗Öt cuß╗æn s├ích mß╗¢i # noqa: E501

    :param book_input: 
    :type book_input: dict | bytes

    :rtype: Union[Book, Tuple[Book, int], Tuple[Book, int, Dict[str, str]]
    """
    book_input = body
    if connexion.request.is_json:
        book_input = BookInput.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
