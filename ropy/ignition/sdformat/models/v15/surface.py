from dataclasses import dataclass
from .surface_type import SurfaceType


@dataclass
class Surface(SurfaceType):
    """
    The surface parameters.
    """
    class Meta:
        name = "surface"
