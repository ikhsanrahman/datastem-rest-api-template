from flask import abort
from sqlalchemy import or_
from flask_jwt_extended import create_access_token

from app.services.service import BaseService
from app.models.user import User


class UserService(BaseService):
    def new_user(self, user_data):
        try:
            return self.insert(user_data)
        except:
            abort(409)

    def login(self, username, password):
        # check if we have a user with this username or e-mail
        user = User.query.filter(or_(User.username == username, User.email == username)).first()
        if user:
            if user.check_password(password):
                # correct username & password, generate a JWT token and sign it
                return create_access_token({ 'user_id': user.id })
            else:
                # wrong password
                abort(401)
        else:
            # no user by that username or e-mail
            abort(401)


user_service = UserService(User)
