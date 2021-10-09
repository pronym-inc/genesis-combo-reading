import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'genesis_combo_reading.conf.environments.vagrant')

app = Celery('genesis_combo_reading_celery')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Set up recurring tasks
app.conf.beat_schedule = {
    # 'some_scheduled_task': {
    #     'task': 'genesis_combo_reading.apps.orders.tasks.my_scheduled_task',
    #     'schedule': crontab(hour='2', minute='30')
    # }
}
