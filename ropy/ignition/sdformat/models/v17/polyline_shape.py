from dataclasses import dataclass
from .polyline_shape_type import PolylineType


@dataclass
class Polyline(PolylineType):
    """
    Defines an extruded polyline shape.
    """
    class Meta:
        name = "polyline"
