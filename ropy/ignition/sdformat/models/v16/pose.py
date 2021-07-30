from dataclasses import dataclass
from .pose_type import PoseType


@dataclass
class Pose(PoseType):
    """
    A position(x,y,z) and orientation(roll, pitch yaw) with respect to the
    specified frame.
    """

    class Meta:
        name = "pose"
