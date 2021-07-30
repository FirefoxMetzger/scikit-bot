from dataclasses import dataclass
from .magnetometer_type import MagnetometerType


@dataclass
class Magnetometer(MagnetometerType):
    """
    These elements are specific to a Magnetometer sensor.
    """

    class Meta:
        name = "magnetometer"
