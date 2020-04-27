import os
import dotenv
dotenv.load_dotenv()

class Config(object):
    # Static configuration options
    # enable flask-sqlalchemy event system
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ENGINE_OPTIONS = {
        # 'pool_pre_ping': False, # if we test a connection before issuing statements to it, usefull for debugging, not for production
        # 'pool_recycle': 1800,  # how long (in seconds) a connection may live, always closed/refreshed after this period
        # 'pool_size': 10, # max number of tcp connections in our pool
        # 'max_overflow': 0, # how much extra (on top of pool_size) connections we allow, not efficient -> disable
        # 'pool_timeout': 30,  # how long we are willing to wait for the pool to give us back a connection
    }
    # embed some variables by which we can check our runtime environment
    MAX_CONTENT_LENGTH = 300 * 1024 * 1024
    # Celery config keys
    timezone = 'Europe/Amsterdam',
    enable_utc = True
    # configurable variables via environment
    # The secret key is used by Flask to encrypt session cookies.
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    # The shared key is used to authenticate the REST API's internally
    SHARED_KEY = os.environ.get('SHARED_KEY')
    PROJ = os.environ.get('PROJ', 'development')
    DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
    SQLALCHEMY_ECHO = os.environ.get('SQLALCHEMY_ECHO', 'True').lower() == 'true'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND')
    SOCKETIO_MESSAGE_QUEUE = os.environ.get('SOCKETIO_MESSAGE_QUEUE')


# create the class instance (imported in __init__.py)
config = Config()
