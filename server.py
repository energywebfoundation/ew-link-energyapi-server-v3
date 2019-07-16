#!/usr/bin/env python3

"""
Starts the API server
"""

from flask import render_template
import config

connex_app = config.connex_app
connex_app.add_api("swagger.yml", arguments={'title': 'Energy Measurement API'}, pythonic_params=True)

if __name__ == "__main__":
    connex_app.run(debug=True)
