from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


class ComboReadingProcessingWarning(Enum):
    NO_ACCOUNT = auto()
    DUPLICATE = auto()
    ABNORMAL_DATE = auto()


class ComboReadingFailureReason(Enum):
    FORMAT_ERROR = auto()
    DATA_TYPE_ERROR = auto()
    BODY_DATA_ERROR = auto()
    EMPTY_PARAMS = auto()
    MISSING_PARAM = auto()
    ENCRYPTION_ERROR = auto()
    INCOMPLETE_DATA = auto()
    OTHER_ERROR = auto()


class ComboReadingProcessingResult:
    decrypted_reading: Optional[str]


@dataclass(frozen=True)
class ComboReadingProcessingSuccess(ComboReadingProcessingResult):
    warning: Optional[ComboReadingProcessingWarning] = None
    decrypted_reading: Optional[str] = None


@dataclass(frozen=True)
class ComboReadingProcessingError(ComboReadingProcessingResult):
    reason: ComboReadingFailureReason
    decrypted_reading: Optional[str] = None
