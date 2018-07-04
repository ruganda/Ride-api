from flask.views import MethodView
from flask import jsonify, request, abort, make_response
from app.models import Database, Ride
from app.auth.decoractor import token_required
from app.validate import validate_date, validate_ride
from flask import current_app as app


class RideAPI(MethodView):
    decorators = [token_required]

    def post(self, current_user):
        """offers a new ride"""
        database = Database(app.config['DATABASE_URL'])
        database.create_tables()

        data = request.json
        origin = data['origin']
        destination = data['destination']
        date = data['date']

        if validate_date(date) != 'valid':
            return jsonify({'message': validate_date(date)}), 406

        elif validate_ride(data) == 'valid':

            ride = Ride(origin=origin, destination=destination, date=date)

            try:
                all_rides = ride.fetch_all()
                for this_ride in all_rides:
                    if this_ride['origin'] == ride.origin and \
                            this_ride['destination'] == ride.destination\
                            and str(this_ride['date']) == str(ride.date) and \
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
        return jsonify({'message': validate_ride(data)}), 406

    def get(self, current_user, r_id):
        """Method for passenger to view  rides"""
        database = Database(app.config['DATABASE_URL'])
        database.create_tables()

        if r_id:
            try:
                ride = Ride(id=r_id)
                ride = ride.find_by_id(r_id)
                if ride:
                    return jsonify(ride), 200
                return jsonify({'msg': "Ride not found "}), 404
            except Exception as e:
                response = {
                    'message': str(e)
                }
                return make_response(jsonify(response)), 500
        else:
            try:
                ride = Ride()
                rides = ride.fetch_all()
                if rides == []:
                    return jsonify(
                        {"msg": " There are no rides rides at the moment"
                         }), 200
                return jsonify(rides), 200
            except Exception as e:
                response = {
                    'message': str(e)
                }
                return make_response(jsonify(response)), 500


class DriverAPI(MethodView):
    """"This class based view handles driver methods"""
    decorators = [token_required]

    def get(self, current_user):
        """Helps a driver viell all his  """
        database = Database(app.config['DATABASE_URL'])
        database.create_tables()

        ride = Ride()
        driver = current_user[2]
        RIDES = ride.fetch_all_by_driver(driver)
        if RIDES == []:
            return jsonify(
                {"msg": "You have not offered any rides yet"
                 }), 200
        return jsonify(RIDES), 200
