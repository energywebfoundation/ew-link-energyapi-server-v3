from datetime import datetime
from config import db, ma
from marshmallow import fields
from sqlalchemy import Column, Integer, ForeignKey, types, sql

class Energy(db.Model):
    __tablename__ = "energy"
    id = db.Column(db.Integer, primary_key=True)
    energy = db.Column(db.Float(64))
    measurement_time = db.Column(
        db.DateTime(), default=sql.func.now()
    )
    created = db.Column(
        db.DateTime(), default=sql.func.now() # use db to set timestamp
    )
    updated = db.Column(
        db.DateTime(), default=sql.func.now(), onupdate=sql.func.now()
    )
    asset_id = Column(Integer, ForeignKey('asset.id'))
    
class EnergySchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(strict=True, **kwargs)

    class Meta:
        model = Energy
        sqla_session = db.session