from dataclasses import dataclass
from .altimeter_type import AltimeterType


@dataclass
class Altimeter(AltimeterType):
    class Meta:
        name = "altimeter"
