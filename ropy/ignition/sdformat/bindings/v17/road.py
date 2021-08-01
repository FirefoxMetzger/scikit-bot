from dataclasses import dataclass
from .road_type import RoadType


@dataclass
class Road(RoadType):
    class Meta:
        name = "road"
