import json

from datetime import datetime, timedelta
from db import db,create_tables

from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_apscheduler import APScheduler
from events_api import events_bp
from config import Config
from cache import cache
from flask_apscheduler import APScheduler
from sqlalchemy import text



def create_app(config_class=Config):

    app = Flask(__name__)
    app.config.from_object(config_class)
    app.logger.info('create app')

    scheduler = APScheduler()

    scheduler.init_app(app)
    db.init_app(app)
    cache.init_app(app)
    cache.clear()

    with app.app_context():
        create_tables(db)
        app.register_blueprint(events_bp)

    socketio = SocketIO(
        app,
        cors_allowed_origins="*",
        message_queue=app.config['CACHE_REDIS_URL'],
    )

    @socketio.on('connect', namespace='/updates')
    def handle_connect(json):
        app.logger.info('received json: ' + str(json))

    @app.route('/')
    def hello():
        return render_template('index.html')

    return app, socketio, scheduler

app,socketio,scheduler = create_app()



def check_database_table():
    with app.app_context():
        # Get current local time

        try:
            local_now = datetime.now().replace(second=0)

            exact_thirty_minutes_start = local_now + timedelta(minutes=30)
            exact_thirty_minutes_end = exact_thirty_minutes_start + timedelta(minutes=1)

            formatted_exact_time_start = exact_thirty_minutes_start.strftime("%Y-%m-%d %H:%M:%S")
            formatted_exact_time_end = exact_thirty_minutes_end.strftime("%Y-%m-%d %H:%M:%S")

            query = text("""select * from events WHERE start_time >= :formatted_exact_time_start and start_time <=
                         :formatted_exact_time_end""")

            events = db.session.execute(query, {
                'formatted_exact_time_start': formatted_exact_time_start,
                'formatted_exact_time_end': formatted_exact_time_end,
            }).fetchall()

            for e in events:
                socketio.emit(
                    f'{e.title} will start in 30 mins',
                    json.dumps('event_reminders'),
                    namespace='/updates',
                )
        except Exception as e:
            app.logger.error(f'schedul job failed {e}')

def init_scheduler(
    scheduler,
    job,
):
    scheduler.add_job(
        id='Scheduled Task',
        func=job,
        trigger='interval',
        seconds=60,
    )
    scheduler.start()

init_scheduler(
    scheduler,
    check_database_table,
)
