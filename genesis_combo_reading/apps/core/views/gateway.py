import logging

from dependency_injector.wiring import Provide
from django.http import HttpRequest, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from genesis_combo_reading.apps.core.service.sync_time import ComboSyncTimeService

logger = logging.getLogger('get_gateway_data')


@method_decorator(csrf_exempt, name='dispatch')
class GatewayView(View):
    http_method_names = ['post']

    time_service: ComboSyncTimeService = None

    def __init__(
            self,
            time_service: ComboSyncTimeService = Provide[ComboSyncTimeService],
            *args,
            **kwargs):
        self.time_service = time_service
        super().__init__(*args, **kwargs)

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        dt = self.time_service.get_datetime()
        local_dt = self.time_service.get_local_datetime()
        dt_format = "%Y/%m/%d %H:%M:%S"
        return HttpResponse(f"2000\r\n{dt.strftime(dt_format)}\r\n{local_dt.strftime(dt_format)}")
