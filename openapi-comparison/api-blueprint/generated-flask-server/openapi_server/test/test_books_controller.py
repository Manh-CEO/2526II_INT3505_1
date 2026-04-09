import unittest

from flask import json

from openapi_server.models.lyth_ng_tin_chi_ti_tcamtcu_nsch404_response import LYThNgTinChiTiTCAMTCuNSCh404Response  # noqa: E501
from openapi_server.models.th_mmtcu_nsch_mi201_response import ThMMTCuNSChMI201Response  # noqa: E501
from openapi_server.models.th_mmtcu_nsch_mi_request import ThMMTCuNSChMIRequest  # noqa: E501
from openapi_server.test import BaseTestCase


class TestBooksController(BaseTestCase):
    """BooksController integration test stubs"""

    def test_ly_danh_sch_tt_ccc_cun_sch(self):
        """Test case for ly_danh_sch_tt_ccc_cun_sch

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

    def test_ly_thng_tin_chi_tit_ca_mt_cun_sch(self):
        """Test case for ly_thng_tin_chi_tit_ca_mt_cun_sch

        Lấy thông tin chi tiết của một cuốn sách
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/books/{id}'.format(id='1'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_thm_mt_cun_sch_mi(self):
        """Test case for thm_mt_cun_sch_mi

        Thêm một cuốn sách mới
        """
        body = openapi_server.ThMMTCuNSChMIRequest()
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/books',
            method='POST',
            headers=headers,
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
