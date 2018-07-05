"""Handles rides class based views"""
from flask.views import MethodView
from flask import jsonify, request, make_response, current_app as app
from app.models import Ride
from app.auth.decoractor import token_required
from app.validate import validate_date, validate_ride
from app.database import Database


class RideAPI(MethodView):
    """A class based view to handle rides"""
    decorators = [token_required]

    def post(self, current_user):
        """offers a new ride"""
        database = Database(app.config['DATABASE_URL'])
        data = request.get_json()

        if validate_date(data['date']) != 'valid':
            return jsonify({'message': validate_date(data['date'])}), 406

        elif validate_ride(data) == 'valid':

            driver = current_user.username
            ride_query = database.get_argument(
                table='rides', column=driver, arg=driver)

            if ride_query is None:
                database.insert_ride_data(data, driver)
                response = {
                    'message': 'You offered a ride successfully.',
                }
                return make_response(jsonify(response)), 201

            return jsonify({'message': 'Ride already exists'}), 409

    def get(self, current_user, ride_id):
        """Method for passenger to view  rides"""
        database = Database(app.config['DATABASE_URL'])
        if ride_id:
            query = database.fetch_single_element(ride_id)
            print(query)
            if query:
                ride = Ride(query[0], query[1], query[2], query[3], query[4])
                response = {'id': ride.ride_id, "origin": ride.origin,
                            'destination': ride.destination,
                            "date_time": ride.date_time, 'driver': ride.driver}
                return jsonify(response), 200
            return jsonify({'msg': "Ride not found "}), 404

        else:
            rides = database.fetch_all()
            if rides == []:
                return jsonify(
                    {"msg": " There are no rides rides at the moment"
                     }), 200
            return jsonify(rides), 200
