import connexion
import six

from datetime import datetime

from flask import make_response, abort

from config import db
from api.model.asset_model import Asset, AssetSchema
from api.model.energy_model import Energy, EnergySchema

def delete(asset_id):  # noqa: E501
    """Delete an asset and it's metering data

     # noqa: E501

    :param asset_id: 
    :type asset_id: int

    :rtype: None
    """
    return 'do some magic!'


def post(role, energy_unit, is_accumulated, manufacturer=None, model=None, serial_number=None, latitude=None, longitude=None):  # noqa: E501
    """Create a new asset, returns asset id

     # noqa: E501

    :param role: Whether this assset is a producer, consumer or both (like a battery)
    :type role: dict | bytes
    :param energy_unit: 
    :type energy_unit: dict | bytes
    :param is_accumulated: 
    :type is_accumulated: bool
    :param manufacturer: 
    :type manufacturer: str
    :param model: 
    :type model: str
    :param serial_number: 
    :type serial_number: str
    :param latitude: 
    :type latitude: float
    :param longitude: 
    :type longitude: float

    :rtype: Asset
    """

    asset = {
        "role": role,
        "energy_unit": energy_unit,
        "is_accumulated": is_accumulated,
    }

    schema = AssetSchema()
    new_asset = schema.load(asset, session=db.session).data

    db.session.add(new_asset)
    db.session.commit()

    data = schema.dump(new_asset).data
    
    return data, 201


def get(asset_id):  # noqa: E501
    """Get asset information by id

     # noqa: E501

    :param asset_id: 
    :type asset_id: int

    :rtype: Asset
    """

    # Query db by asset id
    update_asset = Asset.query.filter(Asset.id == asset_id).one_or_none()

    if update_asset is not None:
        schema = AssetSchema()
        # get python object from db object
        data = schema.dump(update_asset).data
        return data, 200
    else:
        abort(404, f"Asset not found for ID: {asset_id}")


def get_energy(asset_id, time_start=None, time_end=None, limit=5):  # noqa: E501
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

    update_energy = Energy.query.filter(Energy.measurement_time > time_start, Energy.measurement_time <= time_end).limit(limit).all()


    if update_energy is not None:
        schema = EnergySchema(many=True)
        # get python object from db object
        data = schema.dump(update_energy).data
        return data, 200
    else:
        abort(404, f"Asset not found for ID: {asset_id}")

def post_energy(asset_id, energy, measurement_time):  # noqa: E501
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

    energy_data = {
        "energy": energy,
        "measurement_time": measurement_time,
    }

    schema = EnergySchema()
    new_energy = schema.load(energy_data, session=db.session).data

    db.session.add(new_energy)
    db.session.commit()

    data = schema.dump(new_energy).data

    return data, 201
