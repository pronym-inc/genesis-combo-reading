from dataclasses import dataclass


@dataclass(frozen=True)
class ComboReadingEncryptionConfig:
    enable_encryption: bool
    secret: str
    executable_dir: str
