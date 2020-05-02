import datetime

from flask import current_app
from flask_restx import Resource, Namespace, fields
from flask_login import login_required, current_user

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

    @login_required
    @api.expect(user, skip_none=True)
    @api.marshal_with(user)
    def patch(self):
        """Edit the logged in User"""
        pass
        # return user_service.update(api.payload)

    # @login_required
    @api.expect(new_user_request, validate=True)
    @api.marshal_with(user)
    def post(self):
        """Create a new User """
        return user_service.new_user(api.payload)

@api.route('/login')
class UserLoginResource(Resource):
    @api.expect(user_login_request, validate=True)
    @api.marshal_with(user_login_response)
    def post(self):
        # send username and password to the user service to check the login
        # if it fails the user service raises an Exception, therefore if the login function
        # returns we can assume it succeeded
        token = user_service.login(**api.payload)
        return {'token': token }
