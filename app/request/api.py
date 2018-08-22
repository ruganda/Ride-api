"""This module handles RequestApi class and its methods"""
from flask import jsonify, make_response, request, abort, current_app as app
from flask.views import MethodView
from app.models import Ride, Request
from app.database import Database, RequestBbQueries
from app.auth.decoractor import token_required


class RequestAPI(MethodView):
    """This class-based view for requesting a ride."""
    decorators = [token_required]

    def post(self, current_user, ride_id):
        """Post method view for requesting a ride"""
        database = Database(app.config['DATABASE_URL'])
        request_db = RequestBbQueries()

        passenger = current_user.username
        query = database.fetch_by_param('rides', 'id', ride_id)

        if query is None:
            abort(404)

        ride = Ride(query[0], query[1], query[2], query[3], query[4])

        if ride.driver != passenger:

            all_reqs = request_db.fetch_by_arg('passenger', passenger)
            # print(ride_id in all_reqs.keys)
            req_values = []
            for i in range(len(all_reqs)):
                # print(all_reqs[i]['ride_id'])
                req_values.append(str(all_reqs[i]['ride_id']))

            if str(ride_id) in req_values:
                return jsonify({'message': 'You already requested' +
                                ' to join this ride'}), 409

            request_db.send_request(ride_id, passenger)
            return jsonify({'message': 'A request to join this ride' +
                            " has been sent"}), 201
        else:
            return jsonify(
                {'message': "You can't request to join your own ride"}), 403

    def get(self, current_user, ride_id):
        '''Gets all ride requests for a specific ride'''
        database = Database(app.config['DATABASE_URL'])
        request_db = RequestBbQueries()
        # first check if the ride was created by the logged in driver
        driver = current_user.username
        query = database.fetch_by_param('rides', 'id', ride_id)
        if query is None:
            abort(404)

        ride = Ride(query[0], query[1], query[2], query[3], query[4])
        if ride.driver == driver:

            ride_requests = request_db.fetch_by_id(ride_id)

            return jsonify(ride_requests), 200
        abort(404)

    def put(self, current_user, ride_id, request_id):
        """Accept or reject a ride request"""
        database = Database(app.config['DATABASE_URL'])
        request_db = RequestBbQueries()
        # first check if the ride was created by the logged in driver
        driver = current_user.username
        query = database.fetch_by_param('rides', 'id', ride_id)
        if query is None:
            abort(404)

        ride = Ride(query[0], query[1], query[2], query[3], query[4])
        if ride.driver == driver:
            data = request.get_json()
            print(data['status'])
            if data['status'] == 'accepted' or data['status'] == 'rejected':

                request_db.update_request(request_id, data)
                response = {
                    'message': 'you have {} this ride request'
                    .format(data['status'])
                }
                return make_response(jsonify(response)), 200

            response = {
                'message': 'The status can only be in 3 states,' +
                'requested, accepted and rejected'
            }
            return make_response(jsonify(response)), 406
        abort(404)
