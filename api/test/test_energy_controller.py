# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from api.model.energy import Energy  # noqa: E501
from api.test import BaseTestCase


class TestEnergyController(BaseTestCase):
    """EnergyController integration test stubs"""

    def test_asset_asset_id_energy_get(self):
        """Test case for asset_asset_id_energy_get

        Get energy measurements of asset
        """
        query_string = [('role', 'role_example'),
                        ('time_start', '2013-10-20T19:20:30+01:00'),
                        ('time_end', '2013-10-20T19:20:30+01:00'),
                        ('limit', 56)]
        response = self.client.open(
            '/v3/asset/{assetID}/energy'.format(asset_id=56),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_asset_asset_id_energy_post(self):
        """Test case for asset_asset_id_energy_post

        Publish new energy measurement
        """
        query_string = [('energy', 1.2),
                        ('measurement_time', '2013-10-20T19:20:30+01:00')]
        response = self.client.open(
            '/v3/asset/{assetID}/energy'.format(asset_id=56),
            method='POST',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
