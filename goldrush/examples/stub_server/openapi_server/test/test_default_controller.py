# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from openapi_server.models.area import Area  # noqa: E501
from openapi_server.models.balance import Balance  # noqa: E501
from openapi_server.models.dig import Dig  # noqa: E501
from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.license import License  # noqa: E501
from openapi_server.models.license_list import LicenseList  # noqa: E501
from openapi_server.models.report import Report  # noqa: E501
from openapi_server.models.treasure_list import TreasureList  # noqa: E501
from openapi_server.models.wallet import Wallet  # noqa: E501
from openapi_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_cash(self):
        """Test case for cash

        
        """
        body = 'body_example'
        response = self.client.open(
            '/All-Cups/highloadcup/raw/main/goldrush/swagger.yaml/cash',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_dig(self):
        """Test case for dig

        
        """
        body = Dig()
        response = self.client.open(
            '/All-Cups/highloadcup/raw/main/goldrush/swagger.yaml/dig',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_explore_area(self):
        """Test case for explore_area

        
        """
        body = Area(pos_x=0, pos_y=0)
        response = self.client.open(
            '/All-Cups/highloadcup/raw/main/goldrush/swagger.yaml/explore',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_balance(self):
        """Test case for get_balance

        
        """
        response = self.client.open(
            '/All-Cups/highloadcup/raw/main/goldrush/swagger.yaml/balance',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_health_check(self):
        """Test case for health_check

        
        """
        response = self.client.open(
            '/All-Cups/highloadcup/raw/main/goldrush/swagger.yaml/health-check',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_issue_license(self):
        """Test case for issue_license

        
        """
        body = [56]
        response = self.client.open(
            '/All-Cups/highloadcup/raw/main/goldrush/swagger.yaml/licenses',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_licenses(self):
        """Test case for list_licenses

        
        """
        response = self.client.open(
            '/All-Cups/highloadcup/raw/main/goldrush/swagger.yaml/licenses',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
