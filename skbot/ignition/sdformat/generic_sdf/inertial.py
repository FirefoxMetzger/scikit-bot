import warnings

from .base import ElementBase


class Inertial(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        warnings.warn("`Inertial` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)
