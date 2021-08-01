from dataclasses import dataclass
from .projector_type import ProjectorType


@dataclass
class Projector(ProjectorType):
    class Meta:
        name = "projector"
