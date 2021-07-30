from dataclasses import dataclass
from .frame_type import FrameType


@dataclass
class Frame(FrameType):
    """
    A frame of reference to which a pose is relative.
    """

    class Meta:
        name = "frame"
