from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from flask.views import MethodView
from flask import jsonify, request, make_response
from app.models import User
from app.validate import validate_user, validate_login


class RegistrationView(MethodView):
    """This class-based view registers a new user."""

    def post(self):
        """registers a user"""
        data = request.get_json()
        validate = validate_user(data)
        if validate == 'valid':
            # Query to see if the user already exists
            user_object = User(
                data['name'], data['username'], data['password'])
            user = user_object.get_single_user(data['username'])
            if not user:
                try:
                    # Register the user
                    name = data['name']
                    username = data['username']
                    password = data['password']
                    user = User(name=name, username=username,
                                password=generate_password_hash(password, method='sha256'))
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
        return jsonify({'message': validate}), 406


class LoginView(MethodView):
    """This class-based view handles user login and access token generation."""

    def post(self):
        '''Logs in a registered user and returns a token'''
        data = request.get_json()
        validate = validate_login(data)
        if validate == 'valid':
            try:
                user = User(data['username'], data['password'])
                user_object = user.get_single_user(data['username'])
                if user_object == None:
                    response = {
                        'message': 'user not found , please register an account to continue.'
                    }
                    return make_response(jsonify(response)), 401

                current_user = User(
                    username=user_object[2], password=user_object[3])

                if current_user and current_user.username == data['username'] and \
                        check_password_hash(current_user.password, data['password']):
                    # Generate the access token
                    token = jwt.encode({'username': current_user.username, 'exp': datetime.utcnow()
                                        + timedelta(days=10, minutes=60)}, 'donttouch')
                    if token:
                        response = {
                            'message': 'You logged in successfully.',
                            'token': token.decode('UTF-8')
                        }
                        return make_response(jsonify(response)), 200
                else:

                    response = {
                        'message': 'Invalid username or password, Please try again.'
                    }
                    return make_response(jsonify(response)), 401
            except Exception as e:
                response = {
                    'message': str(e)
                }
                return make_response(jsonify(response)), 500
        return jsonify({'message': validate}), 406
