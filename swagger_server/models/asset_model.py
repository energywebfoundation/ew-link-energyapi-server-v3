from datetime import datetime
from config import db, ma
from marshmallow import fields

class Asset(db.Model):
    __tablename__ = "asset"
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(32))
    manufacturer = db.Column(db.String(32))
    model = db.Column(db.String(32))
    serial_number = db.Column(db.String(32))
    latitude = db.Column(db.Float(64))
    longitude = db.Column(db.Float(64))
    energy_unit = db.Column(db.String(32))
    is_accumulated = db.Column(db.Boolean)
    created = db.Column(
        db.DateTime, default=datetime.utcnow
    )
    updated = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    
class AssetSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(strict=True, **kwargs)

    class Meta:
        model = Asset
        sqla_session = db.session