import warnings

from .base import ElementBase


class Cylinder(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        warnings.warn("`Cylinder` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)


"""<element name="cylinder" required="0">
  <description>Cylinder shape</description>
  <element name="radius" type="double" default="1" required="1">
    <description>Radius of the cylinder</description>
  </element>
  <element name="length" type="double" default="1" required="1">
    <description>Length of the cylinder along the z axis</description>
  </element>
</element>
"""
