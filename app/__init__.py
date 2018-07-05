"""Creates module is the main application factory"""
from flask import Flask
from config import app_config
from app.database import Database

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
    return app

