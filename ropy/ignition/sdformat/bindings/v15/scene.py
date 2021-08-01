from dataclasses import dataclass
from .scene_type import SceneType


@dataclass
class Scene(SceneType):
    class Meta:
        name = "scene"
