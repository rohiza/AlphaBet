from datetime import datetime
from db import db


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False, default='new event')
    description = db.Column(db.String(200), default='default event description')
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    location = db.Column(db.String(100))
    creation_time = db.Column(db.DateTime, default=datetime.utcnow)

    def as_dict(self):
        return {
           c.name: getattr(self, c.name)
           for c in self.__table__.columns
       }
