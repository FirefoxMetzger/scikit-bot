from dataclasses import dataclass
from .visual_type import VisualType


@dataclass
class Visual(VisualType):
    class Meta:
        name = "visual"
