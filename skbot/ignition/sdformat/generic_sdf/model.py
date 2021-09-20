from itertools import chain
from typing import List, Any


from .base import ElementBase, PoseBearing, Pose
from .link import Link
from .include import Include
from .frame import Frame
from .joint import Joint
from ..exceptions import ParseError

class Model(ElementBase):
    pass
    # def __init__(
    #     self,
    #     *,
    #     name: str,
    #     pose: Pose = None,
    #     placement_frame: str = None,
    #     canonical_link: str = None,
    #     links: List[Link],
    #     include: List[Include],
    #     models: List["Model"],
    #     frames: List[Frame],
    #     joints: List[Joint],
    # ) -> None:
    #     super().__init__(name=name, pose=pose)
    #     self.placement_frame = placement_frame
    #     self.canonical_link = canonical_link
    #     self.links = links
    #     self.include = include
    #     self.models = models
    #     self.frames = frames
    #     self.joints = joints

    #     if self.canonical_link is None:
    #         if len(links) > 0:
    #             self.canonical_link = links[0].name
    #         elif len(include) > 0:
    #             self.canonical_link = include[0].name
    #         elif len(models) > 0:
    #             self.canonical_link = f"{models[0].name}::{models[0].canonical_link}"
    #         else:
    #             raise ParseError(f"Can not determine canonical link of `{name}`.")

    #     if self.placement_frame is None:
    #         self.placement_frame = "__model__"

    #     implicit_frames = [el.name for el in chain(models, include)]
    #     all_frames = [el.name for el in chain(links, include, models, frames, joints)]
    #     unique_frames = set(all_frames)

    #     if len(all_frames) != len(unique_frames):
    #         duplicated = [name for x in unique_frames if all_frames.count(x) > 1]
    #         raise ParseError(
    #             f"Non-unique frame names encountered for names: {duplicated}"
    #         )

    #     el: PoseBearing
    #     pose_bearing: List[PoseBearing] = [
    #         links,
    #         joints,
    #         [x for x in include if x.pose is not None],
    #         models,
    #         frames,
    #     ]
    #     for el in chain(*pose_bearing):
    #         relative_to = el.pose.relative_to
    #         if relative_to is None:
    #             el.pose.relative_to = "__model__"
    #         elif relative_to in implicit_frames:
    #             el.pose.relative_to += "::__model__"

    #     for frame in self.frames:
    #         if frame.attached_to is None:
    #             frame.attached_to = "__model__"
    #         elif frame.attached_to in implicit_frames:
    #             frame.attached_to = frame.attached_to + "::__model__"


"""<!-- Model -->
<element name="model" required="*">
  <description>The model element defines a complete robot or any other physical object.</description>

  <attribute name="name" type="string" default="__default__" required="1">
    <description>
      The name of the model and its implicit frame. This name must be unique
      among all elements defining frames within the same scope, i.e., it must
      not match another //model, //frame, //joint, or //link within the same
      scope.
    </description>
  </attribute>

  <attribute name="canonical_link" type="string" default="" required="*">
    <description>
      The name of the model's canonical link, to which the model's implicit
      coordinate frame is attached. If unset or set to an empty string,
      the first link element listed as a child of this model is chosen
      as the canonical link.
    </description>
  </attribute>
  <attribute name="placement_frame" type="string" default="" required="0">
    <description>The frame inside this model whose pose will be set by the pose element of the model. i.e, the pose element specifies the pose of this frame instead of the model frame.</description>
  </attribute>

  <element name="static" type="bool" default="false" required="0">
    <description>If set to true, the model is immovable. Otherwise the model is simulated in the dynamics engine.</description>
  </element>

  <element name="self_collide" type="bool" default="false" required="0">
    <description>If set to true, all links in the model will collide with each other (except those connected by a joint). Can be overridden by the link or collision element self_collide property. Two links within a model will collide if link1.self_collide OR link2.self_collide. Links connected by a joint will never collide.</description>
  </element>

  <element name="allow_auto_disable" type="bool" default="true" required="0">
    <description>Allows a model to auto-disable, which is means the physics engine can skip updating the model when the model is at rest. This parameter is only used by models with no joints.</description>
  </element>

  <include filename="frame.sdf" required="*"/>
  <include filename="pose.sdf" required="0"/>
  <include filename="link.sdf" required="*"/>
  <include filename="joint.sdf" required="*"/>
  <include filename="plugin.sdf" required="*"/>
  <include filename="gripper.sdf" required="*"/>

  <element name="include" required="*">
    <description>
      Include resources from a URI. This can be used to nest models. Included resources can only contain one 'model', 'light' or 'actor' element. The URI can point to a directory or a file. If the URI is a directory, it must conform to the model database structure (see /tutorials?tut=composition&amp;cat=specification&amp;#defining-models-in-separate-files).
    </description>
    <element name="uri" type="string" default="__default__" required="1">
      <description>URI to a resource, such as a model</description>
    </element>

    <include filename="pose.sdf" required="0"/>
    <include filename="plugin.sdf" required="*"/>

    <element name="name" type="string" default="" required="0">
      <description>Override the name of the included model.</description>
    </element>

    <element name="static" type="bool" default="false" required="0">
      <description>Override the static value of the included model.</description>
    </element>

    <element name="placement_frame" type="string" default="" required="0">
      <description>The frame inside the included model whose pose will be set by the specified pose element. If this element is specified, the pose must be specified.</description>
    </element>
  </element>

  <element name="model" ref="model" required="*">
    <description>A nested model element</description>
    <attribute name="name" type="string" default="__default__" required="1">
      <description>A unique name for the model. This name must not match another nested model in the same level as this model.</description>
    </attribute>
  </element>

  <element name="enable_wind" type="bool" default="false" required="0">
    <description>If set to true, all links in the model will be affected by the wind. Can be overriden by the link wind property.</description>
  </element>

</element> <!-- End Model -->
"""