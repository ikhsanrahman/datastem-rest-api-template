from flask import Flask, Blueprint
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from flask_migrate import Migrate
from flask_restx import Api

from app.utils.flask_celery import Celery
from app.config import config

login = LoginManager()
jwt = JWTManager()
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
    from app.models import db
    db.init_app(app)
    # attach flask-login and flask-jwt-extended to the app
    login.init_app(app)
    jwt.init_app(app)
    # initialize the flask migration service
    # this gives us access to commands `flask db migrate` and `flask db upgrade`
    flask_migrate.init_app(app, db)
    # init flask-socketio for long-polling & websocket communication to the browser
    socketio.init_app(app, cors_allowed_origins='*', async_mode='threading' if config.DEBUG else 'eventlet', message_queue=config.SOCKETIO_MESSAGE_QUEUE)
    # create the API object and attach our rest api routes
    blueprint = Blueprint('api', __name__)
    api = Api(blueprint,
        title='Datastem REST API template',
        version='1.0',
        description='Provides a gateway for all operations on the stored entities',
        prefix='/v1',
        default_mediatype='application/json;charset=utf-8',
        doc='/' if app.config.get('DEBUG') else False
    )
    from app.controllers.user_controller import api as user_api
    api.add_namespace(user_api)
    app.register_blueprint(blueprint)
    # all loaded extensions are now bound to this app object, return it for serving by a WSGI app
    return app
