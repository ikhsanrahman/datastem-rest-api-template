from app.models import db
from app.models.util import TimestampMixin, EmailType

class User(db.Model, TimestampMixin):
    # primary key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # object properties
    username = db.Column(db.UnicodeText, nullable=False)
    email = db.Column(EmailType, nullable=False)
    password = db.Column(db.Unicode(255), nullable=False)
