import warnings

from .base import ElementBase, should_warn_unsupported


class Visual(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        if should_warn_unsupported():
            warnings.warn("`Visual` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)
