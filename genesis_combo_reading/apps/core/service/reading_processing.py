from abc import ABC
from datetime import datetime
from typing import Optional

from pytz import UTC

from dependency_injector.wiring import Provide

from genesis_combo_reading.apps.core.service.reading_encryption import ComboReadingEncryptionService
from genesis_combo_reading.apps.core.service.service_models.reading import ComboReading
from genesis_combo_reading.apps.core.service.service_models.reading_processing_result import \
    ComboReadingProcessingResult, ComboReadingProcessingSuccess, ComboReadingFailureReason, ComboReadingProcessingError, \
    ComboReadingProcessingWarning


class ComboReadingProcessingService(ABC):
    _encryption_service: ComboReadingEncryptionService
    _encryption_key: str

    def process_reading(self, raw_reading: str) -> ComboReadingProcessingResult:
        ...


class ComboReadingProcessingServiceImpl(ComboReadingProcessingService):
    _encryption_service: ComboReadingEncryptionService

    def __init__(self, encryption_service=Provide[ComboReadingEncryptionService]):
        self._encryption_service = encryption_service

    def process_reading(self, raw_reading: str) -> ComboReadingProcessingResult:
        result = self._process_reading_and_get_result(raw_reading)
        # Log it.
        self._log_reading(raw_reading, result)

        return result

    def _process_reading_and_get_result(self, raw_reading: str) -> ComboReadingProcessingResult:
        # Decrypt it.
        decrypted_reading = self._decrypt_reading(raw_reading)
        if decrypted_reading is None:
            return ComboReadingProcessingError(
                reason=ComboReadingFailureReason.ENCRYPTION_ERROR,
                decrypted_reading=decrypted_reading
            )

        # See if it's a duplicate.
        if self._determine_if_reading_is_duplicate(decrypted_reading):
            return ComboReadingProcessingSuccess(
                warning=ComboReadingProcessingWarning.DUPLICATE,
                decrypted_reading=decrypted_reading
            )

        # Parse it.
        parsed_reading = self._parse_reading(decrypted_reading)
        if parsed_reading is None:
            return ComboReadingProcessingError(
                reason=ComboReadingFailureReason.BODY_DATA_ERROR,
                decrypted_reading=decrypted_reading
            )

        # Save it
        self._save_reading(parsed_reading)
        return ComboReadingProcessingSuccess(
            warning=None,
            decrypted_reading=decrypted_reading
        )

    def _decrypt_reading(self, encrypted_reading: str) -> Optional[str]:
        return self._encryption_service.decrypt(encrypted_reading)

    def _determine_if_reading_is_duplicate(self, decrypted_reading: str) -> bool:
        from genesis_combo_reading.apps.core.models import LogEntry
        return LogEntry.objects.filter(decrypted_content=decrypted_reading).count() > 0

    def _log_reading(
            self,
            raw_reading: str,
            result: ComboReadingProcessingResult
    ) -> None:
        from genesis_combo_reading.apps.core.models import LogEntry
        LogEntry.objects.create(
            content=raw_reading,
            decrypted_content=result.decrypted_reading,
            decryption_succeeded=result.decrypted_reading is not None,
            processing_succeeded=isinstance(result, ComboReadingProcessingSuccess)
        )

    def _parse_reading(self, raw_reading: bytes) -> Optional[ComboReading]:
        cleaned_lines = raw_reading.decode('ascii').splitlines()
        data = {
            key: value for key, value in
            map(lambda x: x.split('='), cleaned_lines)
        }

        kwargs = {
            'gateway_type': data.get('GatewayType'),
            'gateway_id': data.get('GatewayID'),
            'device_type': data.get('DeviceType'),
            'device_id': data.get('DeviceID'),
            'extension_id': data.get('ExtensionID'),
            'year': data.get('Year'),
            'month': data.get('Month'),
            'day': data.get('Day'),
            'hour': data.get('Hour'),
            'minute': data.get('Minute'),
            'second': data.get('Second'),
            'data_type': data.get('DataType'),
            'value1': data.get('Value1'),
            'value2': data.get('Value2'),
            'value3': data.get('Value3'),
            'value4': data.get('Value4'),
            'value5': data.get('Value5'),
            'value6': data.get('Value6')

        }
        return ComboReading(**kwargs)

    def _save_reading(self, reading: ComboReading) -> None:
        reading_dt = UTC.localize(datetime(
            int(reading.year),
            int(reading.month),
            int(reading.day),
            int(reading.hour),
            int(reading.minute),
            int(reading.second)
        ))
        from genesis_combo_reading.apps.core.models import GlucoseReading, BloodPressureReading
        if reading.data_type == '1':
            GlucoseReading.objects.create(
                reading_datetime=reading_dt,
                meid=reading.device_id,
                blood_glucose=reading.value1,
                measurement_type=reading.value4
            )
        elif reading.data_type == '2':
            BloodPressureReading.objects.create(
                reading_datetime=reading_dt,
                meid=reading.device_id,
                systolic_measurement=reading.value1,
                diastolic_measurement=reading.value2,
                pulse=reading.value3,
                mean_pressure=reading.value4,
                average_measurement=reading.value5,
                ihb_index=reading.value6
            )
