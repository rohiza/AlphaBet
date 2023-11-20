import json
from flask import Blueprint, jsonify, request, current_app
from flask_socketio import SocketIO
from dataaccess.events import event_dao

events_bp = Blueprint(
    "events",
    __name__,
    url_prefix="/events/",
)

socketio = SocketIO(
    cors_allowed_origins="*",
    message_queue='redis://redis:6379',
)


@events_bp.route("create", methods=["POST"])
def create():
    try:

        payload = request.get_json()
        new_event = event_dao.create_events(payload['events'])
        socketio.emit(
            'event_created',
            json.dumps('event_created'),
            namespace='/updates',
        )

        return jsonify(new_event.as_dict()), 200

    except Exception as e:
        current_app.logger.error(f"{payload}")
        current_app.logger.error(f"create event got exception {e}")

        return jsonify({}), 500

@events_bp.route("get", methods=["GET"])
def get():
    try:

        event_id = request.args["id"]
        new_event = event_dao.get_event_by_id(event_id)

        return jsonify(new_event.as_dict()), 200

    except Exception as e:
        current_app.logger.error(f"{id}")
        current_app.logger.error(f"get event got exception {e}")

        return jsonify({}), 500


@events_bp.route("get_all", methods=["GET"])
def get_all():
    try:

        events = event_dao.get_all_events(query_args=request.args)
        events = [e.as_dict() for e in events]

        return jsonify(events), 200

    except Exception as e:
        current_app.logger.error(f"get all events got exception {e}")

        return jsonify({}), 500


@events_bp.route("delete", methods=["POST"])
def delete():
    try:

        event_id = request.get_json()["id"]
        res = event_dao.delete_event_by_id(event_id)

        if res:
            socketio.emit(
                'event_deleted',
                json.dumps({'event_id':event_id}),
                namespace='/updates',
            )

        res = "succeed" if res else "failed"

        return jsonify(res), 200

    except Exception as e:
        current_app.logger.error(f"delete event got exception {e}")

        return jsonify({}), 500


@events_bp.route("update", methods=["PUT"])
def update():
    try:

        data = request.get_json()
        res = event_dao.update_event_by_id(
            data["id"],
            data["values"],
        )
        if res:
            socketio.emit(
                'event_updated',
                json.dumps(data["values"]),
                namespace='/updates',
            )

        res = "succeed" if res else "failed"

        return jsonify(res), 200

    except Exception as e:
        current_app.logger.error(f"update event got exception {e}")

        return jsonify({}), 500
