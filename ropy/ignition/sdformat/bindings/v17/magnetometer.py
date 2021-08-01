from dataclasses import dataclass
from .magnetometer_type import MagnetometerType


@dataclass
class Magnetometer(MagnetometerType):
    class Meta:
        name = "magnetometer"
