import warnings

from .base import ElementBase


class Capsule(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        warnings.warn("`Capsule` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)
