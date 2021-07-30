from dataclasses import dataclass
from .air_pressure_type import AirPressureType


@dataclass
class AirPressure(AirPressureType):
    """
    These elements are specific to an air pressure sensor.
    """

    class Meta:
        name = "air_pressure"
