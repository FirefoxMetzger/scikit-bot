import warnings
from itertools import chain
from typing import List, Any


from .base import ElementBase, Pose, PoseBearing, NamedPoseBearing
from .light import Light
from .frame import Frame
from .sensor import Sensor

class Link(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        warnings.warn("`Link` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)


# class Link(NamedPoseBearing):
#     def __init__(
#         self,
#         *,
#         name: str,
#         pose: Pose = None,
#         must_be_base_link: bool = False,
#         inertial: "Link.Inertial" = None,
#         collisions: List[NamedPoseBearing],
#         visuals: List[NamedPoseBearing],
#         projector: NamedPoseBearing = None,
#         audio_source_poses: List[Pose],
#         sensors: List[Sensor],
#         lights: List["Light"] = None,
#         frames: List["Frame"] = None,
#     ) -> None:
#         super().__init__(name=name, pose=pose)
#         self.must_be_base_link = must_be_base_link
#         self.inertial = inertial
#         self.projector = projector
#         self.collision = collisions
#         self.visual = visuals
#         self.sensors = sensors
#         self.lights = lights
#         self.audio_sources = [PoseBearing(pose=p) for p in audio_source_poses]
#         self.frames = frames

#         if frames is None:
#             self.frames = list()

#         if lights is None:
#             self.lights = list()

#         for el in chain(
#             visuals, collisions, self.audio_sources, sensors, self.lights, self.frames
#         ):
#             if el.pose.relative_to is None:
#                 el.pose.relative_to = name

#         if projector is not None:
#             if projector.pose.relative_to is None:
#                 projector.pose.relative_to = name

#         # inertial frame is _forced_ to be relative to link
#         if self.inertial is not None:
#             self.inertial.pose.relative_to = name

#     class Inertial(PoseBearing):
#         def __init__(self, *, pose: Pose = None, frames: List["Frame"] = None) -> None:
#             super().__init__(pose=pose)
#             self.frames = frames

#             if self.frames is None:
#                 self.frames = list()


"""<!-- Link -->
<element name="link" required="*">
  <description>A physical link with inertia, collision, and visual properties. A link must be a child of a model, and any number of links may exist in a model.</description>

  <attribute name="name" type="string" default="__default__" required="1">
    <description>A unique name for the link within the scope of the model.</description>
  </attribute>

  <element name="gravity" type="bool" default="true" required="0">
    <description>If true, the link is affected by gravity.</description>
  </element>

  <element name="enable_wind" type="bool" default="false" required="0">
    <description>If true, the link is affected by the wind.</description>
  </element>

  <element name="self_collide" type="bool" default="false" required="0">
    <description>If true, the link can collide with other links in the model. Two links within a model will collide if link1.self_collide OR link2.self_collide. Links connected by a joint will never collide.</description>
  </element>

  <element name="kinematic" type="bool" default="false" required="0">
    <description>If true, the link is kinematic only</description>
  </element>

  <element name="must_be_base_link" type="bool" default="false" required="0">
    <description>If true, the link will have 6DOF and be a direct child of world.</description>
  </element>

  <element name="velocity_decay" required="0">
    <description>Exponential damping of the link's velocity.</description>
    <element name="linear" type="double" default="0.0" required="0">
      <description>Linear damping</description>
    </element>
    <element name="angular" type="double" default="0.0" required="0">
      <description>Angular damping</description>
    </element>
  </element> <!-- End velocity decay -->

  <include filename="pose.sdf" required="0"/>
  <include filename="inertial.sdf" required="0"/>
  <include filename="collision.sdf" required="*"/>
  <include filename="visual.sdf" required="*"/>
  <include filename="sensor.sdf" required="*"/>
  <include filename="projector.sdf" required="*"/>
  <include filename="audio_sink.sdf" required="*"/>
  <include filename="audio_source.sdf" required="*"/>
  <include filename="battery.sdf" required="*"/>
  <include filename="light.sdf" required="*"/>
  <include filename="particle_emitter.sdf" required="*"/>

</element> <!-- End Link -->
"""