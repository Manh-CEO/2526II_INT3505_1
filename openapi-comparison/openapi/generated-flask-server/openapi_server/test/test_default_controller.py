import unittest

from flask import json

from openapi_server.models.book import Book  # noqa: E501
from openapi_server.models.book_input import BookInput  # noqa: E501
from openapi_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_books_get(self):
        """Test case for books_get

        Lấy danh sách tất cả các cuốn sách
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/books',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_books_id_get(self):
        """Test case for books_id_get

        Lấy thông tin chi tiết của một cuốn sách
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/books/{id}'.format(id='id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_books_post(self):
        """Test case for books_post

        Thêm một cuốn sách mới
        """
        book_input = {"author":"author","isbn":"isbn","title":"title"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/books',
            method='POST',
            headers=headers,
            data=json.dumps(book_input),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
