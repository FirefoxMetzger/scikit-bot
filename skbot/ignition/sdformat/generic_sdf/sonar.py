import warnings

from .base import ElementBase


class Sonar(ElementBase):
  def __init__(self, *, sdf_version: str) -> None:
    warnings.warn("`Sonar` has not been implemented yet.")
    super().__init__(sdf_version=sdf_version)


"""<element name="sonar" required="0">
  <description>These elements are specific to the sonar sensor.</description>
  <element name="geometry" type="string" default="cone" required="0">
    <description>The sonar collision shape. Currently supported geometries are: "cone" and "sphere".</description>
  </element>
  <element name="min" type="double" default="0" required="1">
    <description>Minimum range</description>
  </element>
  <element name="max" type="double" default="1.0" required="1">
    <description>Max range</description>
  </element>

  <element name="radius" type="double" default="0.5" required="0">
    <description>Radius of the sonar cone at max range. This parameter is only used if geometry is "cone".</description>
  </element>
</element>"""
