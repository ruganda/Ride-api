from flask import Blueprint

from app.request.api import RequestAPI

request_app = Blueprint('request_app', __name__)

request_view = RequestAPI.as_view('request_api')
request_app.add_url_rule('/api/v2/rides/<ride_id>/requests',
                         view_func=request_view, methods=['POST', ])

request_app.add_url_rule('/api/v2/users/rides/<ride_id>/requests',
                         view_func=request_view, methods=['GET', ])

request_app.add_url_rule('/api/v2/users/rides/<ride_id>/requests/<request_id>',
                         view_func=request_view, methods=['PUT', ])
