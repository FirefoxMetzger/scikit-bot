from dataclasses import dataclass
from .battery_type import BatteryType


@dataclass
class Battery(BatteryType):
    class Meta:
        name = "battery"
