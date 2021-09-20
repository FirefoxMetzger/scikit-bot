import warnings

from .base import ElementBase


class Altimeter(ElementBase):
  def __init__(self, *, sdf_version: str) -> None:
    warnings.warn("`Altimeter` has not been implemented yet.")
    super().__init__(sdf_version=sdf_version)

"""<element name="altimeter" required="0">
  <description>These elements are specific to an altimeter sensor.</description>

  <element name="vertical_position" required="0">
    <description>
      Noise parameters for vertical position
    </description>
    <include filename="noise.sdf" required="0"/>
  </element>

  <element name="vertical_velocity" required="0">
    <description>
      Noise parameters for vertical velocity
    </description>
    <include filename="noise.sdf" required="0"/>
  </element>

</element>
"""