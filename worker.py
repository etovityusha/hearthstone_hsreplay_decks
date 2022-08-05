import os

from celery import Celery
from celery.schedules import crontab

from controllers.etl.hsreplay_etl import HSReplayETL

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379/0")
celery.conf.beat_schedule = {
    'run_etl': {
        'task': 'run_etl',
        'schedule': crontab(hour="*/12"),
    },
}


@celery.task(name='run_etl')
def run_etl():
    return HSReplayETL()
