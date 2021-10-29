import logging
from typing import Tuple

from django.http import HttpRequest, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from dependency_injector.wiring import Provide

from genesis_combo_reading.apps.core.service.reading_processing import ComboReadingProcessingService
from genesis_combo_reading.apps.core.service.service_models.reading_processing_result import \
    ComboReadingProcessingSuccess, ComboReadingProcessingWarning, ComboReadingProcessingResult, \
    ComboReadingProcessingError, ComboReadingFailureReason


logger = logging.getLogger('get_gateway_data')


@method_decorator(csrf_exempt, name='dispatch')
class GetGatewayDataView(View):
    http_method_names = ['post']

    reading_processing_service: ComboReadingProcessingService = None

    def __init__(
            self,
            reading_processing_service: ComboReadingProcessingService = Provide[ComboReadingProcessingService],
            *args,
            **kwargs):
        self.reading_processing_service = reading_processing_service
        super().__init__(*args, **kwargs)

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        result = self.reading_processing_service.process_reading(request.body)

        status_code, error_code = self._get_status_and_error_code_for_result(result)

        return HttpResponse(f"{error_code}".encode('ascii'), status=status_code)

    def _get_status_and_error_code_for_result(self, result: ComboReadingProcessingResult) -> Tuple[int, int]:
        response_code: int
        error_code: int
        match result:
            case ComboReadingProcessingSuccess(warning=maybe_warning):
                response_code = 200

                match maybe_warning:
                    case None:
                        error_code = 200
                    case ComboReadingProcessingWarning.NO_ACCOUNT:
                        error_code = 2002
                    case ComboReadingProcessingWarning.DUPLICATE:
                        error_code = 2003
                    case ComboReadingProcessingWarning.ABNORMAL_DATE:
                        error_code = 2004
                    case unexpected_warning:
                        logger.warning(f"Received an unexpected warning {unexpected_warning}")
                        # Return an error back to device
                        response_code = 500
                        error_code = 500

            case ComboReadingProcessingError(reason=reason):
                response_code = 400

                match reason:
                    case ComboReadingFailureReason.FORMAT_ERROR:
                        error_code = 4001
                    case ComboReadingFailureReason.DATA_TYPE_ERROR:
                        error_code = 4004
                    case ComboReadingFailureReason.BODY_DATA_ERROR:
                        error_code = 4005
                    case ComboReadingFailureReason.EMPTY_PARAMS:
                        error_code = 4006
                    case ComboReadingFailureReason.MISSING_PARAM:
                        error_code = 4007
                    case ComboReadingFailureReason.ENCRYPTION_ERROR:
                        error_code = 4008
                    case ComboReadingFailureReason.INCOMPLETE_DATA:
                        error_code = 4009
                    case _:
                        # "Other" error
                        error_code = 4010
            case something_unexpected:
                logger.warning(f"Received unexpected reading processing result: {something_unexpected}")
                response_code = 500
                error_code = 500

        return response_code, error_code
