from datetime import datetime

import sqlalchemy as sa

from app.models import db

class TimestampMixin(object):
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)


class EmailType(sa.types.TypeDecorator):
    impl = sa.Unicode

    def __init__(self, length=255, *args, **kwargs):
        super(EmailType, self).__init__(length=length, *args, **kwargs)

    def process_bind_param(self, value, dialect):
        if value is not None:
            return value.lower()
        return value

    @property
    def python_type(self):
        return self.impl.type.python_type
