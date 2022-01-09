import warnings

from .base import ElementBase, should_warn_unsupported


class Link(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        if should_warn_unsupported():
            warnings.warn("`Link` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)
