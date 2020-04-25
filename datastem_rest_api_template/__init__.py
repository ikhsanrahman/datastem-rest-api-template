from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_migrate import Migrate

from datastem_rest_api_template.utils.flask_celery import Celery
from datastem_rest_api_template.config import config

db = SQLAlchemy()
celery = Celery()
socketio = SocketIO()
flask_migrate = Migrate()

# application factory pattern
def create_app():
    # create our base app object
    app = Flask(__name__)
    # set app config
    app.config.from_object(config)
    # attach database to the app
    db.init_app(app)
    # initialize the flask migration service
    # this gives us access to commands `flask db migrate` and `flask db upgrade`
    flask_migrate.init_app(app, db)

    socketio.init_app(app, cors_allowed_origins='*', async_mode='threading' if config.DEBUG else 'eventlet', message_queue=config.SOCKETIO_MESSAGE_QUEUE)
    # all loaded extensions are now bound to this app object, return it for serving by a WSGI app
    return app
