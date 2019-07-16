import connexion
import six

from flask import make_response, abort
from config import db
from swagger_server.models.asset_model import Asset, AssetSchema

def asset_asset_iddelete(asset_id):  # noqa: E501
    """Delete an asset and it's metering data

     # noqa: E501

    :param asset_id: 
    :type asset_id: int

    :rtype: None
    """
    return 'do some magic!'


def asset_post(role, energy_unit, is_accumulated, manufacturer=None, model=None, serial_number=None, latitude=None, longitude=None):  # noqa: E501
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


def get_asset(asset_id):  # noqa: E501
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

