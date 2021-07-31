from dataclasses import dataclass
from .logical_camera_type import LogicalCameraType


@dataclass
class LogicalCamera(LogicalCameraType):
    class Meta:
        name = "logical_camera"
