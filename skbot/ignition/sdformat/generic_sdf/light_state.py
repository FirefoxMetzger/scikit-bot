import warnings

from .base import ElementBase


class Light(ElementBase):
  def __init__(self, *, sdf_version: str) -> None:
    warnings.warn("`Light` has not been implemented yet.")
    super().__init__(sdf_version=sdf_version)

"""<!-- State information for a light -->
<element name="light" required="*">
  <description>Light state</description>

  <attribute name="name" type="string" default="__default__" required="1">
    <description>Name of the light</description>
  </attribute>

  <include filename="pose.sdf" required="0"/>
</element> <!-- End Light -->
"""