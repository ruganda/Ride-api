import uuid

from flask import abort, jsonify, make_response, request
from flask.views import MethodView

from app.auth.decoractor import token_required
from app.models import Request


class RequestAPI(MethodView):
    """This class-based view for requesting a ride."""
    decorators = [token_required]
    def post(self,current_user, ride_id):
        if ride_id:
            try:
                request = Request()
                passenger = current_user[2]
                all_reqs = request.fetch_all()
                for req in  all_reqs:
                    req= {"Id":req['Id'],"ride":req['ride'],"passenger":req['passenger']}
                    if req in all_reqs:
                        return jsonify({'msg': 'You already requested to join this ride' }), 409
                    else:
                        request.insert(ride_id, passenger)  
                        return jsonify({'msg': 'A request to join this ride has been sent' }), 201 
            
            except Exception as e:
                response = {
                    'message': str(e)
                }
                return make_response(jsonify(response)), 500

    