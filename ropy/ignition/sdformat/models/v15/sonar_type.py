from dataclasses import dataclass, field
from typing import List

__NAMESPACE__ = "sdformat/sonar"


@dataclass
class SonarType:
    """
    Parameters
    ----------
    min: Minimum range
    max: Max range
    radius: Radius of the sonar cone at max range.
    """

    class Meta:
        name = "sonarType"

    min: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    max: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    radius: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
