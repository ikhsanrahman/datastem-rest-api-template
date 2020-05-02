import datetime

from flask import current_app
from flask_restx import Resource, Namespace, fields
from flask_login import login_required, current_user

from app.services.user_service import user_service

api = Namespace('common', description='Common operations not related to an entity')


@api.route('/ping')
class PingResource(Resource):
    def get(self):
        """Unsecured ping route"""
        return 'pong'

@api.route('/ping_secured')
class SecuredPingResource(Resource):
    @login_required
    def get(self):
        """Secured ping route"""
        return 'pong'
