import warnings

from .base import ElementBase


class Box(ElementBase):
  def __init__(self, *, sdf_version: str) -> None:
    warnings.warn("`Box` has not been implemented yet.")
    super().__init__(sdf_version=sdf_version)

"""<element name="box" required="0">
  <description>Box shape</description>
  <element name="size" type="vector3" default="1 1 1" required="1">
    <description>The three side lengths of the box. The origin of the box is in its geometric center (inside the center of the box).</description>
  </element>
</element>
"""