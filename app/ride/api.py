"""Handles rides class based views"""
from flask.views import MethodView
from flask import jsonify, request, make_response, current_app as app
from app.models import Ride
from app.auth.decoractor import token_required
from app.validate import validate_date, validate_ride
from app.database import Database, RideBbQueries


class RideAPI(MethodView):
    """A class based view to handle rides"""
    decorators = [token_required]

    def post(self, current_user):
        """offers a new ride"""
        database = Database(app.config['DATABASE_URL'])
        ride_db = RideBbQueries()
        data = request.get_json()
        if validate_date(data['date']) != 'valid':
            return jsonify({'message': validate_date(data['date'])}), 406

        elif validate_ride(data) == 'valid':

            driver = current_user.username

            rides_query = ride_db.fetch_all()
            for ride in rides_query:
                if ride['origin'] == data['origin'] and \
                        ride['destination'] == data['destination']\
                        and str(ride['date']) == str(data['date']) and \
                        ride['driver'] == current_user.username:
                    response = {
                        'message': 'This ride already exists.',
                    }
                    return make_response(jsonify(response)), 409
            ride_db.insert_ride_data(data, driver)
            response = {
                'message': 'You offered a ride successfully.',
            }
            return make_response(jsonify(response)), 201
        return jsonify({'message': validate_ride(data)}), 406

    def get(self, current_user, ride_id):
        """Method for passenger to view  rides"""
        database = Database(app.config['DATABASE_URL'])
        ride_db = RideBbQueries()
        if ride_id:
            query = database.fetch_by_param('rides', 'id', ride_id)
            if query:
                ride = Ride(query[0], query[1], query[2], query[3], query[4])
                response = {'id': ride.ride_id, "origin": ride.origin,
                            'destination': ride.destination,
                            "date_time": ride.date_time, 'driver': ride.driver,
                            'is_owner': ride.drive == current_user}
                return jsonify(response), 200
            return jsonify({'message': "Ride not found "}), 404

        else:
            rides = ride_db.fetch_all()
            return jsonify(rides), 200
