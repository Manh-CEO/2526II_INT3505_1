import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.lyth_ng_tin_chi_ti_tcamtcu_nsch404_response import LYThNgTinChiTiTCAMTCuNSCh404Response  # noqa: E501
from openapi_server.models.th_mmtcu_nsch_mi201_response import ThMMTCuNSChMI201Response  # noqa: E501
from openapi_server.models.th_mmtcu_nsch_mi_request import ThMMTCuNSChMIRequest  # noqa: E501
from openapi_server import util


def ly_danh_sch_tt_ccc_cun_sch():  # noqa: E501
    """Lấy danh sách tất cả các cuốn sách

     # noqa: E501


    :rtype: Union[List[object], Tuple[List[object], int], Tuple[List[object], int, Dict[str, str]]
    """
    return 'do some magic!'


def ly_thng_tin_chi_tit_ca_mt_cun_sch(id):  # noqa: E501
    """Lấy thông tin chi tiết của một cuốn sách

     # noqa: E501

    :param id: ID của cuốn sách
    :type id: str

    :rtype: Union[ThMMTCuNSChMI201Response, Tuple[ThMMTCuNSChMI201Response, int], Tuple[ThMMTCuNSChMI201Response, int, Dict[str, str]]
    """
    return 'do some magic!'


def thm_mt_cun_sch_mi(body=None):  # noqa: E501
    """Thêm một cuốn sách mới

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: Union[ThMMTCuNSChMI201Response, Tuple[ThMMTCuNSChMI201Response, int], Tuple[ThMMTCuNSChMI201Response, int, Dict[str, str]]
    """
    body = body
    if connexion.request.is_json:
        body = ThMMTCuNSChMIRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
