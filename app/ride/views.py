"""Handles adding endponts to the blueprints"""
from flask import Blueprint
from app.ride.api import RideAPI

RIDE_APP = Blueprint('RIDE_APP', __name__)

RIDE_VIEW = RideAPI.as_view('ride_api')

RIDE_APP.add_url_rule('/api/v2/rides/', defaults={'ride_id': None},
                      view_func=RIDE_VIEW, methods=['GET', ])
RIDE_APP.add_url_rule('/api/v2/users/rides/', view_func=RIDE_VIEW,
                      methods=['POST', ])
RIDE_APP.add_url_rule('/api/v2/rides/<int:ride_id>', view_func=RIDE_VIEW,
                      methods=['GET', ])
