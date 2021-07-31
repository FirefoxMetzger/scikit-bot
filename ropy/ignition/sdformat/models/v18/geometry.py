from dataclasses import dataclass
from .geometry_type import GeometryType


@dataclass
class Geometry(GeometryType):
    class Meta:
        name = "geometry"
