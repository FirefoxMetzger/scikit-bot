from dataclasses import dataclass
from .joint_type import JointType


@dataclass
class Joint(JointType):
    """
    A joint connections two links with kinematic and dynamic properties.
    """
    class Meta:
        name = "joint"
