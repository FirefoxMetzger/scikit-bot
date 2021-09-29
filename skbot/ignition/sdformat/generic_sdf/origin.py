from typing import Any

from .base import ElementBase, Pose


class Origin(ElementBase):
    def __init__(self, *, pose: Pose = None, sdf_version: str) -> None:
        super().__init__(sdf_version=sdf_version)

        if pose is None:
            self.pose = Pose(sdf_version=sdf_version)
        else:
            self.pose = pose

    @classmethod
    def from_specific(cls, specific: Any, *, version: str) -> "Origin":
        return Origin(
            pose=Pose.from_specific(specific.pose, version=version),
            sdf_version=version,
        )
