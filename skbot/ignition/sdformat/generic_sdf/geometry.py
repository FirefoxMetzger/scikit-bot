import warnings

from .base import ElementBase


class Geometry(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        warnings.warn("`Geometry` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)


"""<!-- Geometry -->
<element name="geometry" required="1">
  <description>The shape of the visual or collision object.</description>

  <element name="empty" required="0">
    <description>You can use the empty tag to make empty geometries.</description>
  </element> <!-- End empty -->

  <include filename="box_shape.sdf" required="0"/>
  <include filename="capsule_shape.sdf" required="0"/>
  <include filename="cylinder_shape.sdf" required="0"/>
  <include filename="ellipsoid_shape.sdf" required="0"/>
  <include filename="heightmap_shape.sdf" required="0"/>
  <include filename="image_shape.sdf" required="0"/>
  <include filename="mesh_shape.sdf" required="0"/>
  <include filename="plane_shape.sdf" required="0"/>
  <include filename="polyline_shape.sdf" required="0"/>
  <include filename="sphere_shape.sdf" required="0"/>

</element><!-- End Geometry -->
"""
