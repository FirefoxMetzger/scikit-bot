from dataclasses import dataclass
from .plane_shape_type import PlaneType


@dataclass
class Plane(PlaneType):
    """
    Plane shape.
    """
    class Meta:
        name = "plane"
