from celery import Celery
import os

# Initialize Celery
celery = Celery('app',broker=os.environ['CACHE_REDIS_URL'])

# Define your Celery tasks here
@celery.task
def check_database():
    result = db.session.execute("SELECT * FROM events").scalar()
    print(result)
    # Task implementation
