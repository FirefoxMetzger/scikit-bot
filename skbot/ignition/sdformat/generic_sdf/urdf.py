import warnings

from .base import ElementBase, should_warn_unsupported


class URDF(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        if should_warn_unsupported():
            warnings.warn("`URDF` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)
