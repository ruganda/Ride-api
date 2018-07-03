"""This module handles RequestApi class and its methods"""
from flask import jsonify, make_response, request, abort
from flask.views import MethodView
from app.auth.decoractor import token_required
from app.models import Database, Request, Ride
from flask import current_app as app


class RequestAPI(MethodView):
    """This class-based view for requesting a ride."""
    decorators = [token_required]

    def post(self, current_user, ride_id):
        """Post method view for requesting a ride"""
        database = Database(app.config['DATABASE_URL'])
        database.create_tables()

        if ride_id:
            """ first check if the person making a request is the driver/owner
                if the owner wants to respond to his own ride . stop him.
            """"
        ride = Ride(id=ride_id)
        the_ride = ride.find_by_id(ride_id)
        if the_ride is None:
            abort(404)
        if the_ride['driver'] != current_user[2]:

            try:
                request = Request(ride_id=ride_id)
                passenger = current_user[2]
                all_reqs = request.find_by_id(ride_id)
                for req in all_reqs:
                    req = {"Id": req['Id'], "ride_id": req['ride_id'],
                           "status": req['status'],
                           "passenger": req['passenger']}
                    if req in all_reqs:
                        return jsonify({'msg': 'You already requested' +
                                        ' to join this ride'}), 409

                request.insert(ride_id, passenger)
                return jsonify({'msg': 'A request to join this ride' +
                                " has been sent"}), 201

            except Exception as e:
                response = {
                    'message': str(e)
                }
                return make_response(jsonify(response)), 500
        return jsonify(
            {'message': "You can't request to join your own ride"}), 403

    def get(self, current_user, ride_id):
        '''Gets all ride requests for a specific ride'''
        database = Database(app.config['DATABASE_URL'])
        database.create_tables()

        # first check if the ride was created by the logged in driver
        ride = Ride(id=ride_id)
        the_ride = ride.find_by_id(ride_id)
        if the_ride is None:
            abort(404)

        if the_ride['driver'] == current_user[2]:
            request = Request(ride_id=ride_id)
            requests = request.find_by_id(ride_id)
            if requests == []:
                return jsonify({"msg": "You haven't recieved any ride" +
                                " requests yet"}), 200
            return jsonify(requests), 200
        abort(404)

    def put(self, current_user, ride_id, request_id):
        """Accept or reject a ride request"""
        database = Database(app.config['DATABASE_URL'])
        database.create_tables()

        # first check if the ride was created by the logged in driver
        ride = Ride(id=ride_id)
        the_ride = ride.find_by_id(ride_id)
        if the_ride is None:
            abort(404)

        if the_ride['driver'] == current_user[2]:
            data = request.get_json()
            if data['status'] == 'accepted' or data['status'] == 'rejected':
                try:
                    req = Request(id=request_id, ride_id=ride_id)
                    req.update_request(request_id, data)
                    response = {
                        'message': 'you have {} this ride request'
                        .format(data['status'])
                    }
                    return make_response(jsonify(response)), 200
                except Exception as e:
                    response = {
                        'message': str(e)
                    }
                    return make_response(jsonify(response)), 500
            response = {
                'message': 'The status can only be in 3 states,' +
                'requested, accepted and rejected'
            }
            return make_response(jsonify(response)), 406
        abort(404)
