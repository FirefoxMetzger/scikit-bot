from dataclasses import dataclass
from .surface_type import SurfaceType


@dataclass
class Surface(SurfaceType):
    class Meta:
        name = "surface"
