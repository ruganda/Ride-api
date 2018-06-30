from flask import Blueprint
from app.ride.api import RideAPI, DriverAPI

ride_app = Blueprint('ride_app', __name__)

ride_view = RideAPI.as_view('ride_api')
driver_view = DriverAPI.as_view('driver_api')

ride_app.add_url_rule('/api/v2/rides/', defaults={'r_id': None},
                      view_func=ride_view, methods=['GET', ])
ride_app.add_url_rule('/api/v2/users/rides/', view_func=ride_view,
                      methods=['POST', ])
ride_app.add_url_rule('/api/v2/rides/<int:r_id>', view_func=ride_view,
                      methods=['GET', ])
# add url rule for driver view
ride_app.add_url_rule('/api/v2/users/rides/', view_func=driver_view,
                      methods=['GET', ])
