from dataclasses import dataclass
from .ellipsoid_shape_type import EllipsoidType


@dataclass
class Ellipsoid(EllipsoidType):
    """
    Ellipsoid shape.
    """
    class Meta:
        name = "ellipsoid"
