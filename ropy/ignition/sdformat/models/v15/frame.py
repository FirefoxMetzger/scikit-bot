from dataclasses import dataclass
from .frame_type import FrameType


@dataclass
class Frame(FrameType):
    class Meta:
        name = "frame"
