from flask.views import MethodView
from flask import jsonify, request, abort, make_response
from app.models import Ride
from app.auth.decoractor import token_required


class RideAPI(MethodView):
    decorators = [token_required]
    def post(self, current_user):
        """offers a new ride"""
        data = request.json
        origin = data['origin']
        destination = data['destination']
        date = data['date']
        ride = Ride(origin=origin, destination=destination, date=date)
        try:
            all_rides = ride.fetch_all()
            for this_ride in all_rides:
                if this_ride['origin'] == ride.origin and \
                        this_ride['destination'] == ride.destination\
                        and this_ride['date'] == ride.date and \
                        this_ride['driver'] == current_user[2]:
                    response = {
                        'message': 'This ride already exists.',
                    }
                    return make_response(jsonify(response)), 409
            driver = current_user[2]
            ride.insert(driver)

            response = {
                'message': 'You offered a ride successfully.',
            }
            return make_response(jsonify(response)), 201

        except Exception as e:
            response = {
                'message': str(e)
            }
            return make_response(jsonify(response)), 500