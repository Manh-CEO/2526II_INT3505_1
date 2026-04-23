import unittest

from flask import json

from openapi_server.models.pet import Pet  # noqa: E501
from openapi_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_pets_create_pet(self):
        """Test case for pets_create_pet

        
        """
        pet = {"kind":"dog","name":"name","id":0,"age":60}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/pets',
            method='POST',
            headers=headers,
            data=json.dumps(pet),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_pets_delete_pet(self):
        """Test case for pets_delete_pet

        
        """
        headers = { 
        }
        response = self.client.open(
            '/pets/{pet_id}'.format(pet_id=56),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_pets_get_pet(self):
        """Test case for pets_get_pet

        
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/pets/{pet_id}'.format(pet_id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_pets_list_pets(self):
        """Test case for pets_list_pets

        
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/pets',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_pets_update_pet(self):
        """Test case for pets_update_pet

        
        """
        pet = {"kind":"dog","name":"name","id":0,"age":60}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/pets/{pet_id}'.format(pet_id=56),
            method='PUT',
            headers=headers,
            data=json.dumps(pet),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
