from dataclasses import dataclass
from .atmosphere_type import AtmosphereType


@dataclass
class Atmosphere(AtmosphereType):
    """
    The atmosphere tag specifies the type and properties of the atmosphere
    model.
    """
    class Meta:
        name = "atmosphere"
