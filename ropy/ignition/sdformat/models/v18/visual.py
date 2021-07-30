from dataclasses import dataclass
from .visual_type import VisualType


@dataclass
class Visual(VisualType):
    """The visual properties of the link.

    This element specifies the shape of the object (box, cylinder, etc.)
    for visualization purposes.
    """

    class Meta:
        name = "visual"
