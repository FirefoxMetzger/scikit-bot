import warnings

from .base import ElementBase


class Ellipsoid(ElementBase):
  def __init__(self, *, sdf_version: str) -> None:
    warnings.warn("`Ellipsoid` has not been implemented yet.")
    super().__init__(sdf_version=sdf_version)

"""<element name="ellipsoid" required="0">
  <description>Ellipsoid shape</description>
  <element name="radii" type="vector3" default="1 1 1" required="1">
    <description>The three radii of the ellipsoid. The origin of the ellipsoid is in its geometric center (inside the center of the ellipsoid).</description>
  </element>
</element>
"""