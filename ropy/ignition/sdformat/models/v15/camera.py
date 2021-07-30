from dataclasses import dataclass
from .camera_type import CameraType


@dataclass
class Camera(CameraType):
    """
    These elements are specific to camera sensors.
    """

    class Meta:
        name = "camera"
