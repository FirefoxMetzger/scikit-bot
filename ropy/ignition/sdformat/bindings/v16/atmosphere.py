from dataclasses import dataclass
from .atmosphere_type import AtmosphereType


@dataclass
class Atmosphere(AtmosphereType):
    class Meta:
        name = "atmosphere"
