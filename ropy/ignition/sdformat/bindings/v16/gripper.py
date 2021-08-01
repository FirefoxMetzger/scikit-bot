from dataclasses import dataclass
from .gripper_type import GripperType


@dataclass
class Gripper(GripperType):
    class Meta:
        name = "gripper"
