import warnings

from .base import ElementBase


class Altimeter(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        warnings.warn("`Altimeter` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)
