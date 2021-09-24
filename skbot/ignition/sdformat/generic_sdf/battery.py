import warnings

from .base import ElementBase


class Battery(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        warnings.warn("`Battery` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)
