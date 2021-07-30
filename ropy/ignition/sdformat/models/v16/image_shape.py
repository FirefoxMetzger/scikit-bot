from dataclasses import dataclass
from .image_shape_type import ImageType


@dataclass
class Image(ImageType):
    """
    Extrude a set of boxes from a grayscale image.
    """

    class Meta:
        name = "image"
