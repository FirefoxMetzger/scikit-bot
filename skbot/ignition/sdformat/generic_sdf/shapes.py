import warnings

from .base import ElementBase


class Polyline(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        warnings.warn("`Polyline` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)


class Plane(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        warnings.warn("`Plane` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)


class Mesh(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        warnings.warn("`Mesh` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)


class Image(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        warnings.warn("`Image` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)


class Heightmap(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        warnings.warn("`Heightmap` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)


class Ellipsoid(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        warnings.warn("`Ellipsoid` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)


class Cylinder(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        warnings.warn("`Cylinder` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)


class Capsule(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        warnings.warn("`Capsule` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)


class Box(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        warnings.warn("`Box` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)
