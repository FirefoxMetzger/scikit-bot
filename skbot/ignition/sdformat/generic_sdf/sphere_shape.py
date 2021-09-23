import warnings

from .base import ElementBase


class Sphere(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        warnings.warn("`Sphere` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)


"""<element name="sphere" required="0">
  <description>Sphere shape</description>
  <element name="radius" type="double" default="1" required="1">
    <description>radius of the sphere</description>
  </element>
</element>"""
