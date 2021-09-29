import warnings

from .base import ElementBase


class Sphere(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        warnings.warn("`Sphere` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)
