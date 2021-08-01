from dataclasses import dataclass
from .gps_type import GpsType


@dataclass
class Gps(GpsType):
    class Meta:
        name = "gps"
