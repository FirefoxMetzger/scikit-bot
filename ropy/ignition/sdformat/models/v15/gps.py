from dataclasses import dataclass
from .gps_type import GpsType


@dataclass
class Gps(GpsType):
    """
    These elements are specific to the GPS sensor.
    """

    class Meta:
        name = "gps"
