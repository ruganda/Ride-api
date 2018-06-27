from functools import wraps
from flask import request, jsonify
import jwt
from app.models import User
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try: 
            data = jwt.decode(token, 'donttouch')
            user = User(data['username'])
            current_user = user.get_single_user(data['username'])
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

    