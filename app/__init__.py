"""Creates module is the main application factory"""
from flask import Flask
from config import app_config
from app.database import Database
from app.error_handler import *


def create_app(config_name):
    """Creates the application and registers the blueprints
        with the application
    """
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    from app.request.views import REQUEST_APP
    from app.ride.views import RIDE_APP
    from app.auth.views import AUTH_BLUEPRINT
    # register_blueprint
    app.register_blueprint(AUTH_BLUEPRINT)
    app.register_blueprint(RIDE_APP)
    app.register_blueprint(REQUEST_APP)
    # register error handlers
    app.register_error_handler(404, not_found)
    app.register_error_handler(400, bad_request)
    app.register_error_handler(500, internal_server_error)
    app.register_error_handler(405, method_not_allowed)
    method_not_allowed
    return app
