from dataclasses import dataclass
from .altimeter_type import AltimeterType


@dataclass
class Altimeter(AltimeterType):
    """
    These elements are specific to an altimeter sensor.
    """

    class Meta:
        name = "altimeter"
