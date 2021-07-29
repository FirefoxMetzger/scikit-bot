from dataclasses import dataclass
from .geometry_type import GeometryType


@dataclass
class Geometry(GeometryType):
    """
    The shape of the visual or collision object.
    """
    class Meta:
        name = "geometry"
