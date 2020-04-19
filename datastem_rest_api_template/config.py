import os
import dotenv
dotenv.load_dotenv()

class Config(object):
    # Static configuration options
    # enable flask-sqlalchemy event system, we don't use it and it costs cpu time + memory
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # embed some variables by which we can check our runtime environment
    MAX_CONTENT_LENGTH = 300 * 1024 * 1024
    # Celery config keys
    timezone = 'Europe/Amsterdam',
    enable_utc = True
    # configurable variables via environment
    # The secret key is used by Flask to encrypt session cookies.
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # The shared key is used to authenticate the REST API's internally
    SHARED_KEY = os.environ.get('SHARED_KEY')
    PROJ = os.environ.get('PROJ', 'development')
    DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
    SQLALCHEMY_ECHO = os.environ.get('SQLALCHEMY_ECHO', 'True').lower() == 'true'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND')


# create the class instance (imported in __init__.py)
config = Config()
