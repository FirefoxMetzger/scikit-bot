from dataclasses import dataclass
from .joint_type import JointType


@dataclass
class Joint(JointType):
    """A joint connects two links with kinematic and dynamic properties.

    By default, the pose of a joint is expressed in the child link
    frame.
    """

    class Meta:
        name = "joint"
