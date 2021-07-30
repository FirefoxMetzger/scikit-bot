from dataclasses import dataclass
from .logical_camera_type import LogicalCameraType


@dataclass
class LogicalCamera(LogicalCameraType):
    """These elements are specific to logical camera sensors.

    A logical camera reports objects that fall within a frustum.
    Computation should be performed on the CPU.
    """

    class Meta:
        name = "logical_camera"
