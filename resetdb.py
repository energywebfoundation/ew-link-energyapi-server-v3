#!/usr/bin/env python3

import os
from config import db

from swagger_server.models.asset_model import Asset

if os.path.exists("assets.db"):
    os.remove("assets.db")

db.create_all()

db.session.commit()