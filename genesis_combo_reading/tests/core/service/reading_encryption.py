from django.test import TestCase
from testfixtures import Replacer
from testfixtures.popen import MockPopen

from genesis_combo_reading.apps.core.containers import Container
from genesis_combo_reading.apps.core.service.reading_encryption import \
    ComboReadingEncryptionService
from genesis_combo_reading.apps.core.service.reading_encryption_config import ComboReadingEncryptionConfig

TEST_AES_KEY = '0123456789ABCDEF'

DECRYPTED_TEXT = 'this is our message to keep secret'
ENCRYPTED_TEXT = 'ABCDEFABCDEFABCD'
CONFIG = ComboReadingEncryptionConfig(
    enable_encryption=True,
    secret=TEST_AES_KEY,
    executable_dir="/usr/bin"
)


class ComboReadingEncryptionServiceTestCase(TestCase):
    service: ComboReadingEncryptionService = Container().reading_encryption_service(config=CONFIG)

    def setUp(self) -> None:
        self.Popen = MockPopen()
        self.r = Replacer()
        self.r.replace('genesis_combo_reading.apps.core.service.reading_encryption.Popen', self.Popen)
        self.addCleanup(self.r.restore)

    def test_encrypt(self):
        self.Popen.set_default(stdout=ENCRYPTED_TEXT.encode('ascii'))
        self.assertEqual(
            self.service.encrypt(DECRYPTED_TEXT),
            ENCRYPTED_TEXT
        )

    def test_decrypt(self):
        self.Popen.set_default(stdout=DECRYPTED_TEXT.encode('ascii'))
        self.assertEqual(
            self.service.decrypt(ENCRYPTED_TEXT),
            DECRYPTED_TEXT
        )
