import warnings
from typing import List, Any

from .base import ElementBase, NamedPoseBearing, Pose
from .frame import Frame


class Light(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        warnings.warn("`Light` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)


# class Light(NamedPoseBearing):
#     def __init__(
#         self,
#         *,
#         name: str,
#         pose: Pose = None,
#         frames: List["Frame"] = None,
#     ) -> None:
#         super().__init__(name=name, pose=pose)

#         self.frames = frames

#         if frames is None:
#             self.frames = list()

#     @classmethod
#     def from_specific(cls, light: Any, *, version: str) -> "Light":
#         raise NotImplementedError()
