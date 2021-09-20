import warnings

from .base import ElementBase


class Polyline(ElementBase):
  def __init__(self, *, sdf_version: str) -> None:
    warnings.warn("`Polyline` has not been implemented yet.")
    super().__init__(sdf_version=sdf_version)

"""<element name="polyline" required="0">
  <description>Defines an extruded polyline shape</description>

  <element name="point" type="vector2d" default="0 0" required="+">
    <description>
      A series of points that define the path of the polyline.
    </description>
  </element>

  <element name="height" type="double" default="1.0" required="1">
    <description>Height of the polyline</description>
  </element>

</element>
"""