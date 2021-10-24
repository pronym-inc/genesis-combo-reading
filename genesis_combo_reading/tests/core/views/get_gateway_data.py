from unittest.mock import MagicMock

from django.http import HttpResponse
from django.test import RequestFactory, TestCase

from genesis_combo_reading.apps.core.service.service_models.reading_processing_result import \
    ComboReadingProcessingSuccess, ComboReadingProcessingWarning, ComboReadingProcessingResult, \
    ComboReadingProcessingError, ComboReadingFailureReason
from genesis_combo_reading.apps.core.views.get_gateway_data import GetGatewayDataView


class GetGatewayDataViewTestCase(TestCase):

    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.processing_service = MagicMock()
        self.view = GetGatewayDataView.as_view(reading_processing_service=self.processing_service)
        self.view.reading_processing_service = self.processing_service

    def test_should_successfully_process_glucose_reading(self):
        response = self._send_mock_response(ComboReadingProcessingSuccess())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'200')

    def test_process_no_account(self):
        response = self._send_mock_response(ComboReadingProcessingSuccess(ComboReadingProcessingWarning.NO_ACCOUNT))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'2002')

    def test_process_duplicate(self):
        response = self._send_mock_response(ComboReadingProcessingSuccess(ComboReadingProcessingWarning.DUPLICATE))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'2003')

    def test_process_abnormal_date(self):
        response = self._send_mock_response(ComboReadingProcessingSuccess(ComboReadingProcessingWarning.ABNORMAL_DATE))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'2004')

    def test_process_format_error(self):
        response = self._send_mock_response(ComboReadingProcessingError(ComboReadingFailureReason.FORMAT_ERROR))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'4001')

    def test_process_data_type_error(self):
        response = self._send_mock_response(ComboReadingProcessingError(ComboReadingFailureReason.DATA_TYPE_ERROR))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'4004')

    def test_process_body_data_error(self):
        response = self._send_mock_response(ComboReadingProcessingError(ComboReadingFailureReason.BODY_DATA_ERROR))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'4005')

    def test_process_empty_params_error(self):
        response = self._send_mock_response(ComboReadingProcessingError(ComboReadingFailureReason.EMPTY_PARAMS))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'4006')

    def test_process_missing_param_error(self):
        response = self._send_mock_response(ComboReadingProcessingError(ComboReadingFailureReason.MISSING_PARAM))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'4007')

    def test_process_encryption_error(self):
        response = self._send_mock_response(ComboReadingProcessingError(ComboReadingFailureReason.ENCRYPTION_ERROR))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'4008')

    def test_process_incomplete_data(self):
        response = self._send_mock_response(ComboReadingProcessingError(ComboReadingFailureReason.INCOMPLETE_DATA))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'4009')

    def test_process_other_error(self):
        response = self._send_mock_response(ComboReadingProcessingError(ComboReadingFailureReason.OTHER_ERROR))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'4010')

    def _send_mock_response(self, result: ComboReadingProcessingResult) -> HttpResponse:
        self.processing_service.process_reading.return_value = result
        request = self.factory.post(
            'DeliverData/GetGatewayData.aspx',
            "dummy",
            content_type="text/plain; charset=us-ascii"
        )
        return self.view(request)
