import connexion
import six

from datetime import datetime, timezone

from flask import make_response, abort
from sqlalchemy import func

from config import db
from api.model.asset_model import Asset, AssetSchema
from api.model.energy_model import Energy, EnergySchema
from util import ISO8601_to_UTC

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

    :param role: Whether this assset is a producer or consumer
    :type role: str
    :param energy_unit: 
    :type energy_unit: str
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

def patch(asset_id, manufacturer=None, model=None, serial_number=None, latitude=None, longitude=None):  # noqa: E501
    """Update asset information by id

     # noqa: E501

    :param asset_id: 
    :type asset_id: int
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

    # Query db by asset id
    update_asset = Asset.query.filter(Asset.id == asset_id).one_or_none()

    if update_asset is not None:
        schema = AssetSchema()
        # get python object from db object
        data = schema.dump(update_asset).data
        return "TODO: update asset info", 200
    else:
        abort(404, f"Asset not found for ID: {asset_id}")

def get_energy(asset_id, time_start=None, time_end=None, accumulated=False, limit=5):  # noqa: E501
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
    # Query db by asset id
    update_asset = Asset.query.filter(Asset.id == asset_id).one_or_none()

    if update_asset is None:
        abort(404, f"Asset not found for ID: {asset_id}")


    time_start = ISO8601_to_UTC(time_start)
    time_end = ISO8601_to_UTC(time_end)
    if accumulated and not update_asset.is_accumulated:
        sum_energy = Energy.query.with_entities(
            func.group_concat(Energy.id).label("ids"),
            func.sum(Energy.energy).label("energy"),
            func.max(Energy.created).label("created"),
            func.max(Energy.measurement_time).label("measurement_time"),
            func.max(Energy.updated).label("updated")).filter(Energy.asset_id == asset_id, Energy.measurement_time.between(time_start, time_end)).first()
        schema = EnergySchema()
        data = schema.dump(sum_energy).data
        data['ids'] = sum_energy.ids
    else:
        update_energy = Energy.query.filter(Energy.asset_id == asset_id, Energy.measurement_time.between(time_start, time_end))
        if accumulated:
            # get the latest measurement
            update_energy = update_energy.order_by(Energy.measurement_time.desc()).limit(1).first()
            schema = EnergySchema()
        else:
            update_energy = update_energy.limit(limit).all()
            schema = EnergySchema(many=True)
        # get python object from db object
        data = schema.dump(update_energy).data

    from flask_sqlalchemy import get_debug_queries

    info = get_debug_queries()[1]
    #print(info.statement, info.parameters, info.duration, sep='\n')

    return data, 200

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

    this_asset = Asset.query.filter(Asset.id == asset_id).one_or_none()

    if this_asset is not None:
        try:
            measurement_time = ISO8601_to_UTC(measurement_time)
        except ValueError as e:
            abort(404, str(e))

        energy_data = Energy(energy=energy, measurement_time=measurement_time)
        this_asset.measurements.append(energy_data)
        db.session.commit()

        schema = EnergySchema()
        data = schema.dump(energy_data).data

        return data, 201
    else:
        abort(404, f"Asset not found for ID: {asset_id}")
