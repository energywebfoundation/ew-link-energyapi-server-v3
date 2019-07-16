# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.asset import Asset  # noqa: E501
from swagger_server.models.asset_role import AssetRole  # noqa: E501
from swagger_server.models.energy_unit import EnergyUnit  # noqa: E501
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.test import BaseTestCase


class TestAssetController(BaseTestCase):
    """AssetController integration test stubs"""

    def test_asset_asset_iddelete(self):
        """Test case for asset_asset_iddelete

        Delete an asset and it's metering data
        """
        response = self.client.open(
            '/v3/asset/{assetID}'.format(asset_id=56),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_asset_post(self):
        """Test case for asset_post

        Create a new asset, returns asset id
        """
        query_string = [('role', AssetRole()),
                        ('manufacturer', 'manufacturer_example'),
                        ('model', 'model_example'),
                        ('serial_number', 'serial_number_example'),
                        ('latitude', 1.2),
                        ('longitude', 1.2),
                        ('energy_unit', EnergyUnit()),
                        ('is_accumulated', True)]
        response = self.client.open(
            '/v3/asset',
            method='POST',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_asset(self):
        """Test case for get_asset

        Get asset information by id
        """
        response = self.client.open(
            '/v3/asset/{assetID}'.format(asset_id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
