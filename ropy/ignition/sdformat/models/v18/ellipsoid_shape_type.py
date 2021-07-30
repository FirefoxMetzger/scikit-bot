from dataclasses import dataclass, field
from typing import List

__NAMESPACE__ = "sdformat/ellipsoid_shape"


@dataclass
class EllipsoidType:
    """
    Parameters
    ----------
    radii: The three radii of the ellipsoid. The origin of the ellipsoid
        is in its geometric center (inside the center of the ellipsoid).
    """

    class Meta:
        name = "ellipsoidType"

    radii: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
            "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
        },
    )
