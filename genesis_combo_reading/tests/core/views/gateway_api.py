from datetime import datetime
from unittest.mock import MagicMock

from django.test import RequestFactory, TestCase

from genesis_combo_reading.apps.core.views.gateway import GatewayView

FAKE_REQUEST = """FunctionName=GetDateTime\r\nGatewayType=09014A\r\nGatewayID=901410923000001E\r\nDeviceType=3250\r\nDeviceID=3250000014110038"""  # noqa


class GetGatewayDataViewTestCase(TestCase):

    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.time_service = MagicMock()
        self.view = GatewayView.as_view(time_service=self.time_service)
        self.view.time_service = self.time_service

    def test_should_successfully_return_datetime(self):
        self.time_service.get_datetime.return_value = datetime(2019, 1, 2, 17, 3, 6)
        self.time_service.get_local_datetime.return_value = datetime(2019, 1, 2, 8, 3, 6)
        request = self.factory.post(
            'DeliverData/GatewayAPI.aspx',
            FAKE_REQUEST,
            content_type="text/plain; charset=us-ascii"
        )
        response = self.view(request)

        self.assertEqual(
            response.content,
            b'2000\r\n2019/01/02 17:03:06\r\n2019/01/02 08:03:06'
        )
