from django.conf import settings

from genesis_combo_reading.apps.core.containers import Container
from genesis_combo_reading.conf.generic.celery import app as celery_app

container = Container()
container.config.from_dict(settings.__dict__)

__all__ = ('celery_app', 'container')
