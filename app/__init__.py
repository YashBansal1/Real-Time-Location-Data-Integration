# app/__init__.py

from flask import Flask
from flask_restful import Api
from .api import configure_api
from .logger import setup_logger

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    # Initialize API
    api = Api(app)
    configure_api(api)

    # Setup logger
    setup_logger(app)

    return app
