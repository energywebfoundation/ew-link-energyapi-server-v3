#!/usr/bin/env python3

import os
from config import db

from api.model.asset_model import Asset
from api.model.energy_model import Energy

if os.path.exists("assets.db"):
    os.remove("assets.db")

db.create_all()

db.session.commit()