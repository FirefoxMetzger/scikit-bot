from dataclasses import dataclass
from .sonar_type import SonarType


@dataclass
class Sonar(SonarType):
    class Meta:
        name = "sonar"
