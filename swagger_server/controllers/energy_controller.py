import connexion
import six


def asset_asset_id_energy_get(asset_id, role, time_start=None, time_end=None, limit=None):  # noqa: E501
    """Get energy measurements of asset

     # noqa: E501

    :param asset_id: 
    :type asset_id: int
    :param role: Role of energy asset for which the measurement is returned
    :type role: str
    :param time_start: Date in RFC 3339 format. ie. 2018-03-14T17:11:19+00:00
    :type time_start: str
    :param time_end: Date in RFC 3339 format. ie. 2018-03-14T17:12:20+00:00
    :type time_end: str
    :param limit: How many items to return at one time (max 10)
    :type limit: int

    :rtype: List[Energy]
    """
    return 'do some magic!'


def asset_asset_id_energy_post(asset_id, energy, measurement_time):  # noqa: E501
    """Publish new energy measurement

     # noqa: E501

    :param asset_id: 
    :type asset_id: int
    :param energy: Registered in the asset energy unit
    :type energy: float
    :param measurement_time: Time of measurement in the device, in RFC 3339 format. ie. 2018-03-14T17:12:20+00:00
    :type measurement_time: str

    :rtype: Energy
    """
    return 'do some magic!'
