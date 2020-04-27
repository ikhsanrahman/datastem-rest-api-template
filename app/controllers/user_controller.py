import datetime

from flask import current_app
from flask_restx import Resource, Namespace, fields
from flask_login import login_required, current_user
from flask_jwt_extended import create_access_token

from app.services.user_service import user_service

api = Namespace('user', description='User related operations')


user = api.model('User', {
    'id': fields.Integer(readOnly=True, required=False, description='The objects unique identifier'),
    'username': fields.String(required=True, description='The users username'),
    'email': fields.String(required=True, description='The users e-mail address'),
})

new_user_request = api.model('NewUserRequest', {
    'username': fields.String(required=True, description='The users new username'),
    'email': fields.String(required=True, description='The users new e-mail address'),
    'password': fields.String(required=True, description='The new password')
})

user_login_request = api.model('LoginUserRequest', {
    'username': fields.String(required=True, description='The username we want to log in with'),
    'password': fields.String(required=True, description='The password we want to log in with')
})

user_login_response = api.model('LoginUserResponse', {
    'token': fields.String(required=True, description='The user token after a successfull login')
})


@api.route('/')
class UserResource(Resource):
    @login_required
    @api.marshal_with(user)
    def get(self):
        """Get the logged in User"""
        return current_user
        # return user_service.get_all()

    @api.expect(user, skip_none=True)
    @api.marshal_with(user)
    def patch(self):
        """Edit the logged in User"""
        pass
        # return user_service.update(api.payload)

    @api.expect(new_user_request, validate=True)
    @api.marshal_with(user)
    def post(self):
        """Create a new User """
        pass

@api.route('/login')
class UserLoginResource(Resource):
    @api.expect(new_user_request, validate=True)
    @api.marshal_with(user_login_response)
    def post(self):
        # TODO: check login
        # user authenticated successfully, create an access token and sign it
        token = create_access_token({ 'user_id': 1 })
        return {'token': token }