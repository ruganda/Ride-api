from flask.views import MethodView
from flask import jsonify, request, abort, make_response
from app.models import User


class RegistrationView(MethodView):
    """This class-based view registers a new user."""

    def post(self):
        """registers a user"""
        data = request.get_json()
        # Query to see if the user already exists
        user_object = User(
            data['name'], data['username'], data['password'])
        user = user_object.get_single_user(data['username'])
        print(user)
        if not user:
            try:
                # Register the user
                name = data['name']
                username = data['username']
                password = data['password']
                user = User(name=name, username=username,
                            password=password)
                user.insert_data(user)

                response = {
                    'message': 'You registered successfully. Please login.',
                }
                return make_response(jsonify(response)), 201

            except Exception as e:
                response = {
                    'message': str(e)
                }
                return make_response(jsonify(response)), 401
        else:
            response = {

                'message': 'User already exists. Please login.'
            }

            return make_response(jsonify(response)), 409
