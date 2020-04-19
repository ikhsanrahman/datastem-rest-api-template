from flask import Flask, Blueprint

from datastem_rest_api_template.utils.flask_celery import Celery
from datastem_rest_api_template.config import Config

celery = Celery()

# application factory pattern
def create_app():
    # create our base app object
    app = Flask(__name__)

    # all loaded extensions are now bound to this app object, return it for serving by a WSGI app
    return app
