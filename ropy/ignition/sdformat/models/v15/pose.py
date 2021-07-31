from dataclasses import dataclass
from .pose_type import PoseType


@dataclass
class Pose(PoseType):
    class Meta:
        name = "pose"
