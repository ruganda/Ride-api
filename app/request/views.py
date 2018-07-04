"""Handle endpoints for the REQUEST_app blue prints """
from flask import Blueprint
from app.request.api import RequestAPI

REQUEST_APP = Blueprint('REQUEST_APP', __name__)

REQUEST_VIEW = RequestAPI.as_view('request_api')
REQUEST_APP.add_url_rule('/api/v2/rides/<ride_id>/requests',
                         view_func=REQUEST_VIEW, methods=['POST', ])

REQUEST_APP.add_url_rule('/api/v2/users/rides/<ride_id>/requests',
                         view_func=REQUEST_VIEW, methods=['GET', ])

REQUEST_APP.add_url_rule('/api/v2/users/rides/<ride_id>/requests/<request_id>',
                         view_func=REQUEST_VIEW, methods=['PUT', ])
