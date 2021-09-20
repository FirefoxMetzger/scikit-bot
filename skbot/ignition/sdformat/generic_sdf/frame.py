import warnings

from .base import ElementBase, NamedPoseBearing, Pose


class Frame(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        warnings.warn("`Frame` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)

    
# class Frame(NamedPoseBearing):
#     def __init__(
#         self, *, name: str, pose: Pose = None, attached_to: str = None
#     ) -> None:
#         super().__init__(name=name, pose=pose)
#         self.attached_to = attached_to

#         if self.attached_to == "":
#             self.attached_to = None


"""<!-- Frame -->
<element name="frame" required="*">
  <description>A frame of reference in which poses may be expressed.</description>

  <attribute name="name" type="string" default="" required="1">
    <description>
      Name of the frame. It must be unique whithin its scope (model/world),
      i.e., it must not match the name of another frame, link, joint, or model
      within the same scope.
    </description>
  </attribute>

  <attribute name="attached_to" type="string" default="" required="*">
    <description>
      If specified, this frame is attached to the specified frame. The specified
      frame must be within the same scope and may be defined implicitly, i.e.,
      the name of any //frame, //model, //joint, or //link within the same scope
      may be used.

      If missing, this frame is attached to the containing scope's frame. Within
      a //world scope this is the implicit world frame, and within a //model
      scope this is the implicit model frame.

      A frame moves jointly with the frame it is @attached_to. This is different
      from //pose/@relative_to. @attached_to defines how the frame is attached
      to a //link, //model, or //world frame, while //pose/@relative_to defines
      how the frame's pose is represented numerically. As a result, following
      the chain of @attached_to attributes must always lead to a //link,
      //model, //world, or //joint (implicitly attached_to its child //link). 
    </description>
  </attribute>

  <include filename="pose.sdf" required="0"/>

</element> <!-- End Frame -->
"""