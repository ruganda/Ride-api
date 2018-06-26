from flask import Flask
from config import app_config

def create_app(config_name):
    """Creates the application and registers the blueprints 
        with the application
    """
    app = Flask(__name__)  
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    return app