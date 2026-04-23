import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.pet import Pet  # noqa: E501
from openapi_server import util


def pets_create_pet(body):  # noqa: E501
    """pets_create_pet

     # noqa: E501

    :param pet: 
    :type pet: dict | bytes

    :rtype: Union[Pet, Tuple[Pet, int], Tuple[Pet, int, Dict[str, str]]
    """
    pet = body
    if connexion.request.is_json:
        pet = Pet.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def pets_delete_pet(pet_id):  # noqa: E501
    """pets_delete_pet

     # noqa: E501

    :param pet_id: 
    :type pet_id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def pets_get_pet(pet_id):  # noqa: E501
    """pets_get_pet

     # noqa: E501

    :param pet_id: 
    :type pet_id: int

    :rtype: Union[Pet, Tuple[Pet, int], Tuple[Pet, int, Dict[str, str]]
    """
    return 'do some magic!'


def pets_list_pets():  # noqa: E501
    """pets_list_pets

     # noqa: E501


    :rtype: Union[List[Pet], Tuple[List[Pet], int], Tuple[List[Pet], int, Dict[str, str]]
    """
    return 'do some magic!'


def pets_update_pet(pet_id, body):  # noqa: E501
    """pets_update_pet

     # noqa: E501

    :param pet_id: 
    :type pet_id: int
    :param pet: 
    :type pet: dict | bytes

    :rtype: Union[Pet, Tuple[Pet, int], Tuple[Pet, int, Dict[str, str]]
    """
    pet = body
    if connexion.request.is_json:
        pet = Pet.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
