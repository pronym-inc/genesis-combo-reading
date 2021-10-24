import os
from abc import ABC
from subprocess import Popen, PIPE
from typing import Optional

from dependency_injector.wiring import Provide

from genesis_combo_reading.apps.core.service.reading_encryption_config import ComboReadingEncryptionConfig


class ComboReadingEncryptionService(ABC):
    def decrypt(self, message: str) -> Optional[str]:
        ...

    def encrypt(self, message: str) -> str:
        ...


class ComboReadingEncryptionServiceImpl(ComboReadingEncryptionService):
    _config: ComboReadingEncryptionConfig

    def __init__(self, config: ComboReadingEncryptionConfig = Provide['config']):
        self._config = config

    def encrypt(self, message: str) -> str:
        if self._config.enable_encryption:
            return self._call_and_return_command_result(message, 'encrypt')
        return message

    def decrypt(self, message: str) -> str:
        if self._config.enable_encryption:
            return self._call_and_return_command_result(message, 'decrypt')
        return message

    def _call_and_return_command_result(self, message: str, command: str) -> str:
        po = Popen(
            [self._get_executable_path(command), message, self._config.secret],
            stdout=PIPE
        )
        result = po.communicate()[0]
        return result.decode('ascii')

    def _get_executable_path(self, command: str) -> str:
        return os.path.join(self._config.executable_dir, command)
