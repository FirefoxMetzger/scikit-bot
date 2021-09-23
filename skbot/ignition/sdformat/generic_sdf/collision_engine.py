import warnings

from .base import ElementBase


class CollisionEngine(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        warnings.warn("`CollisionEngine` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)


"""<!-- Collision Engine -->
<element name="collision_engine" required="1">
  <description>The collision_engine tag specifies the type and properties of the collision detection engine.</description>

  <element name="ode" required="0">
    <attribute name="type" type="string" default="__default__" required="0">
      <description>The type of the collision detection engine. Current default in ODE is OPCODE.</description>
    </attribute>
  </element>

  <element name="bullet" required="0">
    <attribute name="type" type="string" default="__default__" required="0">
      <description>The type of the collision detection engine.</description>
    </attribute>
  </element>

</element> <!-- Collision Engine -->
"""
