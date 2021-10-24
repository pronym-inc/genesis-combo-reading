from datetime import datetime
from typing import Dict
from unittest.mock import MagicMock

from django.test import TestCase
from pytz import UTC

from genesis_combo_reading.apps.core.containers import Container
from genesis_combo_reading.apps.core.models import BloodPressureReading, GlucoseReading, LogEntry
from genesis_combo_reading.apps.core.service.reading_processing import ComboReadingProcessingService
from genesis_combo_reading.apps.core.service.service_models.reading_processing_result import \
    ComboReadingProcessingSuccess, ComboReadingProcessingWarning, ComboReadingProcessingError, ComboReadingFailureReason


def render_reading_data(data: Dict[str, str]) -> str:
    return "\r\n".join([f"{k}={v}" for k, v in data.items()])


MOCK_BP_READING_CONTENT = {
    'GatewayType': '9011B',
    'GatewayID': '0000000022',
    'DeviceType': '3260',
    'DeviceID': '0204000888555',
    'ExtensionID': '0',
    'Year': '2008',
    'Month': '3',
    'Day': '3',
    'Hour': '8',
    'Minute': '16',
    'Second': '0',
    'DataType': '2',
    'Value1': '112',
    'Value2': '92',
    'Value3': '66'
}

MOCK_GLUCOSE_READING_CONTENT = {
    'GatewayType': '9011B',
    'GatewayID': '0000000022',
    'DeviceType': '3260',
    'DeviceID': '0204000888555',
    'ExtensionID': '0',
    'Year': '2018',
    'Month': '11',
    'Day': '4',
    'Hour': '9',
    'Minute': '14',
    'Second': '2',
    'DataType': '1',
    'Value1': '112',
    'Value4': '1'
}

MOCK_BP_READING_STR = render_reading_data(MOCK_BP_READING_CONTENT)
MOCK_GLUCOSE_READING_STR = render_reading_data(MOCK_GLUCOSE_READING_CONTENT)

MOCK_ENCRYPTED_CONTENT = "secresecrretsrcrecet"


class ComboReadingProcessingServiceTestCase(TestCase):
    service: ComboReadingProcessingService

    def setUp(self) -> None:
        self.mock_encryption_service = MagicMock()
        self.service = Container().reading_processing_service(encryption_service=self.mock_encryption_service)

    def test_process_reading_valid_bp_reading(self):
        self.mock_encryption_service.decrypt.return_value = MOCK_BP_READING_STR

        result = self.service.process_reading(MOCK_ENCRYPTED_CONTENT)

        # We should have a log entry.
        self.assertEqual(LogEntry.objects.count(), 1)
        log_entry = LogEntry.objects.get()
        self.assertTrue(log_entry.processing_succeeded)
        self.assertTrue(log_entry.decryption_succeeded)
        self.assertEqual(log_entry.content, MOCK_ENCRYPTED_CONTENT)
        self.assertEqual(log_entry.decrypted_content, MOCK_BP_READING_STR)

        # Reading should be saved.
        self.assertEqual(BloodPressureReading.objects.count(), 1)
        reading = BloodPressureReading.objects.get()
        self._assert_reading_datetime_matches_data(MOCK_BP_READING_CONTENT, reading.reading_datetime)

        self.assertEqual(reading.meid, MOCK_BP_READING_CONTENT['DeviceID'])
        self.assertEqual(reading.systolic_measurement, int(MOCK_BP_READING_CONTENT['Value1']))
        self.assertEqual(reading.diastolic_measurement, int(MOCK_BP_READING_CONTENT['Value2']))
        self.assertEqual(reading.pulse, int(MOCK_BP_READING_CONTENT['Value3']))

        # Result should be successful, with no warning.
        self.assertIsInstance(result, ComboReadingProcessingSuccess)
        self.assertIsNone(result.warning)

    def test_process_reading_valid_glucose_reading(self):
        self.mock_encryption_service.decrypt.return_value = MOCK_GLUCOSE_READING_STR

        result = self.service.process_reading(MOCK_ENCRYPTED_CONTENT)

        # Reading should be saved.
        self.assertEqual(GlucoseReading.objects.count(), 1)
        reading = GlucoseReading.objects.get()
        self._assert_reading_datetime_matches_data(MOCK_GLUCOSE_READING_CONTENT, reading.reading_datetime)

        self.assertEqual(reading.meid, MOCK_GLUCOSE_READING_CONTENT['DeviceID'])

        self.assertEqual(reading.blood_glucose, int(MOCK_GLUCOSE_READING_CONTENT['Value1']))
        self.assertEqual(reading.measurement_type, int(MOCK_GLUCOSE_READING_CONTENT['Value4']))

        # Result should be successful, with no warning.
        self.assertIsInstance(result, ComboReadingProcessingSuccess)
        self.assertIsNone(result.warning)

    def test_process_reading_duplicate_reading(self):
        self.mock_encryption_service.decrypt.return_value = MOCK_GLUCOSE_READING_STR

        # Process the reading once and then again as a duplicate.
        self.service.process_reading(MOCK_ENCRYPTED_CONTENT)
        result = self.service.process_reading(MOCK_ENCRYPTED_CONTENT)

        # There should be two log entries.
        self.assertEqual(LogEntry.objects.count(), 2)

        # There should only be one record in the database.
        self.assertEqual(GlucoseReading.objects.count(), 1)

        self.assertIsInstance(result, ComboReadingProcessingSuccess)
        self.assertEqual(result.warning, ComboReadingProcessingWarning.DUPLICATE)

    def test_process_reading_cannot_be_decrypted(self):
        self.mock_encryption_service.decrypt.return_value = None

        result = self.service.process_reading(MOCK_ENCRYPTED_CONTENT)

        # There should be a log entry that failed to decrypt.
        self.assertEqual(LogEntry.objects.count(), 1)
        log_entry = LogEntry.objects.get()
        self.assertFalse(log_entry.processing_succeeded)
        self.assertFalse(log_entry.decryption_succeeded)
        self.assertEqual(log_entry.content, MOCK_ENCRYPTED_CONTENT)

        # Should not have saved a reading.
        self.assertEqual(GlucoseReading.objects.count(), 0)

        self.assertIsInstance(result, ComboReadingProcessingError)
        self.assertEqual(result.reason, ComboReadingFailureReason.ENCRYPTION_ERROR)

    def _assert_reading_datetime_matches_data(self, data: Dict[str, str], dt: datetime) -> None:
        self.assertEqual(
            dt,
            UTC.localize(datetime(
                int(data['Year']),
                int(data['Month']),
                int(data['Day']),
                int(data['Hour']),
                int(data['Minute']),
                int(data['Second'])
            ))
        )
