from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ComboReading:
    gateway_type: str
    gateway_id: str
    device_type: Optional[str]
    device_id: str
    extension_id: Optional[str]
    year: str
    month: str
    day: str
    hour: str
    minute: str
    second: str
    data_type: str
    value1: str
    value2: str
    value3: Optional[str]
    value4: Optional[str]
    value5: Optional[str]
    value6: Optional[str]
