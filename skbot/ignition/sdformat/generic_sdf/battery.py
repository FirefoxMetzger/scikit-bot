import warnings

from .base import ElementBase


class Battery(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        warnings.warn("`Battery` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)


"""<!-- Battery -->
<element name="battery" required="*">
  <description>Description of a battery.</description>

  <attribute name="name" type="string" default="__default__" required="1">
    <description>Unique name for the battery.</description>
  </attribute>

  <element name="voltage" type="double" default="0.0" required="1">
    <description>Initial voltage in volts.</description>
  </element>
</element>
"""
