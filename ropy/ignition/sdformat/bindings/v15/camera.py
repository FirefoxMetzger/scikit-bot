from dataclasses import dataclass
from .camera_type import CameraType


@dataclass
class Camera(CameraType):
    class Meta:
        name = "camera"
