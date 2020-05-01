import bcrypt
from flask_login.mixins import UserMixin
from flask_jwt_extended import decode_token

from app import login
from app.models import db
from app.models.util import TimestampMixin, EmailType


class User(db.Model, TimestampMixin, UserMixin):
    # primary key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # object properties
    username = db.Column(db.UnicodeText, nullable=False, unique=True)
    email = db.Column(EmailType, nullable=False, unique=True)
    password_hash = db.Column(db.Unicode(255), nullable=False)

    @property
    def password(self):
        raise AttributeError('password not readable')

    @password.setter
    def password(self, password):
        # bcrypt expects bytes as input
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        # bcrypt expects bytes as input
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

# let flask-login know how it can get to a user
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# let flask-login know how to use Flask-JWT-Extended
@login.request_loader
def load_user_from_request(request):
    # get the Authorization header
    auth_header = request.headers.get('Authorization', '')
    # echeck if the auth header was provided and not empty
    if auth_header != '':
        try:
            # check if we can decode it into a valid JWT token
            token_data = decode_token(auth_header)
            # token was successfully decoded (previous line throws exception otherwise)
            # check if the user is in the database (maybe in the future if the user wasn't deleted?)
            user = User.query.get(int(token_data['identity']['user_id']))
            if user:
                # user is available, return it
                return user
        except:
            # token decoding failed, is either invalid or expired
            pass
    return None
