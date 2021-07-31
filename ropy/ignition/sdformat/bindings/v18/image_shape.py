from dataclasses import dataclass
from .image_shape_type import ImageType


@dataclass
class Image(ImageType):
    class Meta:
        name = "image"
