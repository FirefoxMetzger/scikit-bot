from dataclasses import dataclass
from .battery_type import BatteryType


@dataclass
class Battery(BatteryType):
    """
    Description of a battery.
    """

    class Meta:
        name = "battery"
