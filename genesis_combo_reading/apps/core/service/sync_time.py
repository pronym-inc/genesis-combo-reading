from abc import ABC
from datetime import datetime

from django.utils.timezone import now


class ComboSyncTimeService(ABC):
    def get_datetime(self) -> datetime:
        ...

    def get_local_datetime(self) -> datetime:
        ...


class ComboSyncTimeServiceImpl(ComboSyncTimeService):

    def get_datetime(self) -> datetime:
        return now()

    def get_local_datetime(self) -> datetime:
        return now()
