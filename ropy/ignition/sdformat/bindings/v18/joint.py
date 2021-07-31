from dataclasses import dataclass
from .joint_type import JointType


@dataclass
class Joint(JointType):
    class Meta:
        name = "joint"
