from django.apps import AppConfig

from genesis_combo_reading import container
from . import views


class CoreConfig(AppConfig):
    name = 'genesis_combo_reading.apps.core'

    def ready(self) -> None:
        container.wire(modules=[views])
