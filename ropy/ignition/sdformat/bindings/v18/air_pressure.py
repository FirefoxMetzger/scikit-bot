from dataclasses import dataclass
from .air_pressure_type import AirPressureType


@dataclass
class AirPressure(AirPressureType):
    class Meta:
        name = "air_pressure"
