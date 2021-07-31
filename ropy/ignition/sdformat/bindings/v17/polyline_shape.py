from dataclasses import dataclass
from .polyline_shape_type import PolylineType


@dataclass
class Polyline(PolylineType):
    class Meta:
        name = "polyline"
