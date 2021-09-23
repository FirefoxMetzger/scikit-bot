import warnings

from .base import ElementBase


class Capsule(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        warnings.warn("`Capsule` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)


"""<element name="capsule" required="0">
  <description>Capsule shape</description>
  <element name="radius" type="double" default="0.5" required="1">
    <description>Radius of the capsule</description>
  </element>
  <element name="length" type="double" default="1" required="1">
    <description>Length of the cylindrical portion of the capsule along the z axis</description>
  </element>
</element>
"""
