from dataclasses import dataclass, field
from typing import List

__NAMESPACE__ = "sdformat/logical_camera"


@dataclass
class LogicalCameraType:
    """These elements are specific to logical camera sensors.

    A logical camera reports objects that fall within a frustum.
    Computation should be performed on the CPU.

    Parameters
    ----------
    near: Near clipping distance of the view frustum
    far: Far clipping distance of the view frustum
    aspect_ratio: Aspect ratio of the near and far planes. This is the
        width divided by the height of the near or far planes.
    horizontal_fov: Horizontal field of view of the frustum, in radians.
        This is the angle between the frustum's vertex and the edges of
        the near or far plane.
    """
    class Meta:
        name = "logical_cameraType"

    near: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    far: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    aspect_ratio: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    horizontal_fov: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
