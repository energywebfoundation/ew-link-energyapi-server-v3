from datetime import datetime
from config import db, ma
from marshmallow import fields

class Energy(db.Model):
    __tablename__ = "energy"
    id = db.Column(db.Integer, primary_key=True)
    energy = db.Column(db.Float(64))
    measurement_time = db.Column(
        db.DateTime, default=datetime.utcnow
    )
    created = db.Column(
        db.DateTime, default=datetime.utcnow
    )
    updated = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    
class EnergySchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(strict=True, **kwargs)

    class Meta:
        model = Energy
        sqla_session = db.session