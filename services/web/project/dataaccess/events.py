from models.events import Event
from flask import Blueprint,jsonify,request,current_app
from functools import wraps
from db import db


def error_handler(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            current_app.logger.error(f"Error in {func.__name__}: {e}")
            # Optionally, you can re-raise the exception if you want it to propagate
            raise

    return wrapper

class EventDao():

    @error_handler
    def create_events(self, events):

        new_events = []

        for event in events:
            new_event = Event(**event)
            new_events.append(new_event.as_dict())
            db.session.add(new_event)

        db.session.commit()

        return new_events


    @error_handler
    def get_event_by_id(self, event_id):

        event = db.session.scalars(
            db.select(Event).where(Event.id == event_id)).first()

        return event

    @error_handler
    def get_all_events(self, query_args={}):
        stmt = db.select(Event)
        if query_args.get('wherekey', False):
            stmt = stmt.where(
                getattr(Event,query_args['wherekey']) == query_args['whereValue']

            )
        if query_args.get('orderBy', False):
            stmt = stmt.order_by(query_args['orderBy'])

        events = db.session.execute(stmt).scalars()

        return events

    @error_handler
    def delete_event_by_id(self, event_id):

        event = self.get_event_by_id(event_id)
        db.session.delete(event)
        db.session.commit()

        return event

    @error_handler
    def update_event_by_id(self, event_id, new_values):

        event = self.get_event_by_id(event_id)

        for key, value in new_values.items():
            if getattr(Event,key):
                setattr(event, key, value)

        db.session.commit()

        return event



event_dao = EventDao()
