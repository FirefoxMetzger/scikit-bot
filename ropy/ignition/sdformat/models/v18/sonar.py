from dataclasses import dataclass
from .sonar_type import SonarType


@dataclass
class Sonar(SonarType):
    """
    These elements are specific to the sonar sensor.
    """
    class Meta:
        name = "sonar"
