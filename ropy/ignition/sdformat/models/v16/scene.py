from dataclasses import dataclass
from .scene_type import SceneType


@dataclass
class Scene(SceneType):
    """
    Specifies the look of the environment.
    """

    class Meta:
        name = "scene"
