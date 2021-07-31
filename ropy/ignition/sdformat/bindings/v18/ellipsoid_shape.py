from dataclasses import dataclass
from .ellipsoid_shape_type import EllipsoidType


@dataclass
class Ellipsoid(EllipsoidType):
    class Meta:
        name = "ellipsoid"
