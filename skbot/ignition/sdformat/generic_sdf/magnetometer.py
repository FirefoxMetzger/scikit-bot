import warnings

from .base import ElementBase


class Magnetometer(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        warnings.warn("`Magnetometer` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)


"""<element name="magnetometer" required="0">
  <description>These elements are specific to a Magnetometer sensor.</description>
  <element name="x" required="0">
    <description>
      Parameters related to the body-frame X axis of the magnetometer
    </description>
    <include filename="noise.sdf" required="0"/>
  </element>
  <element name="y" required="0">
    <description>
      Parameters related to the body-frame Y axis of the magnetometer
    </description>
    <include filename="noise.sdf" required="0"/>
  </element>
  <element name="z" required="0">
    <description>
      Parameters related to the body-frame Z axis of the magnetometer
    </description>
    <include filename="noise.sdf" required="0"/>
  </element>
</element>"""
