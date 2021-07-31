from dataclasses import dataclass
from .heightmap_shape_type import HeightmapType


@dataclass
class Heightmap(HeightmapType):
    class Meta:
        name = "heightmap"
