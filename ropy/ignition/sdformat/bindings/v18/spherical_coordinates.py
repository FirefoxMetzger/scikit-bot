from dataclasses import dataclass
from .spherical_coordinates_type import SphericalCoordinatesType


@dataclass
class SphericalCoordinates(SphericalCoordinatesType):
    class Meta:
        name = "spherical_coordinates"
