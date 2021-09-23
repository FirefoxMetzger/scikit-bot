import warnings

from .base import ElementBase


class Contact(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        warnings.warn("`Contact` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)


"""<element name="contact" required="0">
  <description>These elements are specific to the contact sensor.</description>

  <element name="collision" type="string" default="__default__" required="1">
    <description>name of the collision element within a link that acts as the contact sensor.</description>
  </element> <!-- End Collision -->

  <element name="topic" type="string" default="__default_topic__" required="1">
    <description>Topic on which contact data is published.</description>
  </element>

</element> <!-- End Contact -->
"""
