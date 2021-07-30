from dataclasses import dataclass, field
from typing import List

__NAMESPACE__ = "sdformat/image_shape"


@dataclass
class ImageType:
    """
    Parameters
    ----------
    uri: URI of the grayscale image file
    scale: Scaling factor applied to the image
    threshold: Grayscale threshold
    height: Height of the extruded boxes
    granularity: The amount of error in the model
    """

    class Meta:
        name = "imageType"

    uri: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    scale: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    threshold: List[int] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    height: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    granularity: List[int] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
