from dataclasses import dataclass
from .cylinder_shape_type import CylinderType


@dataclass
class Cylinder(CylinderType):
    """
    Cylinder shape.
    """
    class Meta:
        name = "cylinder"
