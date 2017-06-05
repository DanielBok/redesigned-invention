from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.types import TypeDecorator

from Dashboard.extensions import db


class AwareDateTime(TypeDecorator):
    impl = DateTime(timezone=True)

    def process_bind_param(self, value, dialect):
        if isinstance(value, datetime) and value.tzinfo is None:
            raise ValueError('{!r} must be TZ-aware'.format(value))
        return value

    def __repr__(self):
        return "AwareDateTime()"


class ResourceMixin(object):
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        return db.session.commit()

    def __str__(self):
        obj_id = hex(id(self))
        columns = self.__table__.c.keys()
        values = ', '.join("%s=%r" % (n, getattr(self, n)) for n in columns)
        return '<%s %s(%s)>' % (obj_id, self.__class__.__name__, values)
