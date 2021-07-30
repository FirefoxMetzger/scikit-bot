from dataclasses import dataclass
from .heightmap_shape_type import HeightmapType


@dataclass
class Heightmap(HeightmapType):
    """
    A heightmap based on a 2d grayscale image.
    """

    class Meta:
        name = "heightmap"
