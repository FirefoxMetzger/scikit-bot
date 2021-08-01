from dataclasses import dataclass, field
from typing import List

__NAMESPACE__ = "sdformat/sonar"


@dataclass
class SonarType:
    """
    These elements are specific to the sonar sensor.

    Parameters
    ----------
    geometry: The sonar collision shape. Currently supported geometries
        are: "cone" and "sphere".
    min: Minimum range
    max: Max range
    radius: Radius of the sonar cone at max range. This parameter is
        only used if geometry is "cone".
    """

    class Meta:
        name = "sonarType"

    geometry: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
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
