import warnings
from itertools import chain
from typing import List, Any, Dict, Tuple


from .base import BoolElement, ElementBase, Pose
from .light import Light
from .frame import Frame
from .sensor import Sensor
from .origin import Origin
from .inertial import Inertial
from .collision import Collision
from .visual import Visual
from .sensor import Sensor
from .projector import Projector
from .audio_sink import AudioSink
from .audio_source import AudioSource
from .battery import Battery
from .particle_emitter import ParticleEmitter
from .... import transform as tf


class Link(ElementBase):
    """A rigid body.

    Parameters
    ----------
    name : str
        The name of the link. It must be unique within its scope (the containing
        model).
    gravity : bool
        If true (default), the link is affected by gravity.
    enable_wind : bool
        If true, the link is affected by the wind. Default: ``False``.

        .. versionadded:: SDFormat v1.6
    self_collide : bool
        If true, the link can collide with other links in the model. Any other
        link within a model will collide with this link if either
        ``self.self_collide == True`` or ``other.self_collide == True``.
        Further, links connected by a joint will never collide. Default:
        ``False``.
    kinematic : bool
        If True, the link is kinematic only. Default: `` False``
    pose : Pose
        The links's initial position (x,y,z) and orientation (roll, pitch, yaw).

        .. versionadded:: SDFormat 1.2
    must_be_base_link : bool
        If true, the link will have 6DOF and be a direct child of world.

        .. versionadded:: SDFormat 1.4
    velocity_decay : Link.VelocityDecay
        Exponential damping of the link's velocity.

        .. versionadded:: SDFormat 1.2
    inertial : Inertial
        The inertial properties of the link.
    collisions : List[Collision]
        The list of collision properties of a link. Note that this can be
        different from the visual properties of a link, for example, simpler
        collision models are often used to reduce computation time.
    visuals : List[Visual]
        A list of visual properties of the link. This element specifies the
        shape of the object (box, cylinder, etc.) for visualization purposes.
    sensors : List[Sensor]
        A list of sensors attached to this link.
    projectors : List[Projector]
        A list of projectors attached to this link.
    audio_sinks : List[AudioSink]
        A list of audio sinks attached to this link.

        .. versionadded:: SDFormat v1.4
    audio_sources : List[AudioSource]
        A list of audio sources attached to this link.

        .. versionadded:: SDFormat v1.4
    batteries : List[Battery]
        A list of batteries attached to this link.

        .. versionadded:: SDFormat v1.5
    lights : List[Light]
        A list of light sources attached to this link.

        .. versionadded:: SDFormat v1.6
    particle_emitters : List[ParticleEmitter]
        A list of particle emitters attached to this link. A particle emitter
        that can be used to describe fog, smoke, and dust.

        .. versionadded:: SDFormat v1.6
    sdf_version : str
        The SDFormat version to use when constructing this element.
    origin : Origin
        The link's origin.

        .. deprecated:: SDFormat v1.2
            Use `Link.pose` instead.
    damping : Link.Damping
        Exponential damping of the link's velocity.

        .. deprecated:: SDFormat 1.2
            Use `Link.velocity_decay` instead.
    frames : List["Frame"]
        A list of frames of reference in which poses may be expressed.

        .. deprecated:: SDFormat v1.7
            Use :attr:`Model.frame` instead.
        .. versionadded:: SDFormat v1.5


    Attributes
    ----------
    name : str
        See ``Parameters`` section.
    gravity : bool
        See ``Parameters`` section.
    enable_wind : bool
        See ``Parameters`` section.
    self_collide : bool
        See ``Parameters`` section.
    kinematic : bool
        See ``Parameters`` section.
    pose : Pose
        See ``Parameters`` section.
    must_be_base_link : bool
        See ``Parameters`` section.
    velocity_decay : Link.VelocityDecay
        See ``Parameters`` section.
    inertial : Inertial
        See ``Parameters`` section.
    collisions : List[Collision]
        See ``Parameters`` section.
    visuals : List[Visual]
        See ``Parameters`` section.
    sensors : List[Sensor]
        See ``Parameters`` section.
    projectors : List[Projector]
        See ``Parameters`` section.
    audio_sinks : List[AudioSink]
        See ``Parameters`` section.
    audio_sources : List[AudioSource]
        See ``Parameters`` section.
    batteries : List[Battery]
        See ``Parameters`` section.
    lights : List[Light]
        See ``Parameters`` section.
    particle_emitters : List[ParticleEmitter]
        See ``Parameters`` section.

    """

    def __init__(
        self,
        *,
        name: str,
        gravity: bool = True,
        enable_wind: bool = False,
        self_collide: bool = False,
        kinematic: bool = False,
        origin: Origin = None,
        pose: Pose = None,
        must_be_base_link: bool = False,
        damping: "Link.Damping" = None,
        velocity_decay: "Link.VelocityDecay" = None,
        frames: List["Frame"] = None,
        inertial: Inertial = None,
        collisions: List[Collision] = None,
        visuals: List[Visual] = None,
        sensors: List[Sensor] = None,
        projector: Projector = None,
        audio_sinks: List[AudioSink] = None,
        audio_sources: List[AudioSource] = None,
        batteries: List[Battery] = None,
        lights: List["Light"] = None,
        particle_emitters: List[ParticleEmitter] = None,
        sdf_version: str,
    ) -> None:
        super().__init__(sdf_version=sdf_version)
        self.name = name
        self.gravity = gravity
        self.enable_wind = enable_wind
        self.self_collide = self_collide
        self.kinematic = kinematic
        if origin is None:
            self._origin = Origin(sdf_version=sdf_version)
        elif sdf_version == "1.0":
            self._origin = origin
        else:
            warnings.warn("`origin` is deprecated. Use `pose` instead.")
            self._origin = origin
        if sdf_version == "1.0":
            self.pose = self._origin.pose
        elif pose is None:
            self.pose = Pose(sdf_version=sdf_version)
        else:
            self.pose = pose
        self.must_be_base_link = must_be_base_link
        if damping is None:
            self._damping = Link.Damping(sdf_version=sdf_version)
        elif sdf_version == "1.0":
            self._damping = damping
        else:
            warnings.warn("`damping` is deprecated. Use `velocity_decay` instead.")
            self._damping = damping
        if sdf_version == "1.0":
            self.velocity_decay = self._damping
        elif velocity_decay is None:
            self.velocity_decay = Link.VelocityDecay(sdf_version=sdf_version)
        else:
            self.velocity_decay = velocity_decay
        self._frames = [] if frames is None else frames
        self.inertial = inertial
        self.collisions = [] if collisions is None else collisions
        self.visuals = [] if visuals is None else visuals
        self.sensors = [] if sensors is None else sensors
        self.projector = projector
        # projector is buggy
        # self.projectors = [] if projectors is None else projectors
        self.audio_sinks = [] if audio_sinks is None else audio_sinks
        self.audio_sources = [] if audio_sources is None else audio_sources
        self.batteries = [] if batteries is None else batteries
        self.lights = [] if lights is None else lights
        self.particle_emitters = [] if particle_emitters is None else particle_emitters

        self._origin.pose = self.pose

        # if projector is not None:
        #     if projector.pose.relative_to is None:
        #         projector.pose.relative_to = name

        # inertial frame is _forced_ to be relative to link
        # if self.inertial is not None:
        #     self.inertial.pose.relative_to = name

        for frame in self._frames:
            if frame.attached_to is None:
                frame.attached_to = self.name
            if frame.pose.relative_to is None:
                frame.pose.relative_to = self.name

        for sensor in sensors:
            if sensor.pose.relative_to is None:
                sensor.pose.relative_to = self.name

            if sensor.camera.pose.relative_to is None:
                sensor.camera.pose.relative_to = f"{self.name}::{sensor.name}"

            for frame in sensor.camera._frames:
                if frame.pose.relative_to is None:
                    frame.pose.relative_to = (
                        f"{self.name}::{sensor.name}::{sensor.camera.name}"
                    )
                if frame.attached_to is None:
                    frame.attached_to = f"{self.name}::{sensor.name}"

            for frame in sensor._frames:
                if frame.pose.relative_to is None:
                    frame.pose.relative_to = f"{self.name}::{sensor.name}"

                if frame.attached_to is None:
                    frame.attached_to = f"{self.name}::{sensor.name}"

    @property
    def origin(self):
        warnings.warn(
            "`Link.origin` is deprecated since SDF v1.7. Use `Link.pose` instead.",
            DeprecationWarning,
        )
        return self._origin

    @property
    def damping(self):
        warnings.warn(
            "`Link.daming` is deprecated since SDF v1.7."
            " Use `Link.velocity_decay` instead.",
            DeprecationWarning,
        )
        return self._damping

    @property
    def frames(self):
        warnings.warn(
            "`Link.frames` is deprecated since SDF v1.7."
            " Use `Model.frames` instead and set `Frame.attached_to` to the name of this link.",
            DeprecationWarning,
        )
        return self._frames

    @classmethod
    def from_specific(cls, specific: Any, *, version: str) -> "Link":
        link_args = {
            "name": specific.name,
            "inertial": specific.inertial,
        }
        args_with_default = {
            "gravity": BoolElement,
            "enable_wind": BoolElement,
            "self_collide": BoolElement,
            "kinematic": BoolElement,
            "origin": Origin,
            "pose": Pose,
            "must_be_base_link": BoolElement,
            "damping": Link.Damping,
            "velocity_decay": Link.VelocityDecay,
            # projector is buggy
            "projector": Projector,
        }
        list_args = {
            "frame": ("frames", Frame),
            "collision": ("collisions", Collision),
            "visual": ("visuals", Visual),
            "sensor": ("sensors", Sensor),
            "audio_sink": ("audio_sinks", AudioSink),
            "audio_source": ("audio_sources", AudioSource),
            "batterie": ("batteries", Battery),
            "light": ("lights", Light),
            "particle_emitter": ("particle_emitters", ParticleEmitter),
        }

        standard_args = cls._prepare_standard_args(
            specific, args_with_default, list_args, version=version
        )
        link_args.update(standard_args)

        return Link(**link_args, sdf_version=version)

    def declared_frames(self) -> Dict[str, tf.Frame]:
        declared_frames = {self.name: tf.Frame(3, name=self.name)}

        for el in chain(self._frames):
            declared_frames.update(el.declared_frames())

        for sensor in self.sensors:
            for name, frame in sensor.declared_frames().items():
                declared_frames[f"{self.name}::{name}"] = frame

        return declared_frames

    def to_static_graph(
        self,
        declared_frames: Dict[str, tf.Frame],
        *,
        seed: int = None,
        shape: Tuple,
        axis: int = -1,
    ) -> tf.Frame:
        parent_name = self.pose.relative_to
        child_name = self.name

        parent = declared_frames[parent_name]
        child = declared_frames[child_name]

        link = self.pose.to_tf_link()
        link(child, parent)

        for frame in self._frames:
            frame.to_static_graph(declared_frames, seed=seed, shape=shape, axis=axis)

        for sensor in self.sensors:
            sensor.to_static_graph(
                declared_frames,
                f"{self.name}::{sensor.name}",
                seed=seed,
                shape=shape,
                axis=axis,
            )

        return declared_frames[self.name]

    def to_dynamic_graph(
        self,
        declared_frames: Dict[str, tf.Frame],
        *,
        seed: int = None,
        shape: Tuple,
        axis: int = -1,
        apply_state: bool = True,
        _scaffolding: Dict[str, tf.Frame],
    ) -> tf.Frame:
        if self.must_be_base_link:
            parent_name = "world"
            child_name = self.name

            parent = declared_frames[parent_name]
            child = declared_frames[child_name]

            parent_static = _scaffolding[parent_name]
            child_static = _scaffolding[child_name]

            link = tf.CompundLink(parent_static.links_between(child_static))
            link(parent, child)

        for frame in self._frames:
            frame.to_dynamic_graph(
                declared_frames,
                seed=seed,
                shape=shape,
                axis=axis,
                apply_state=apply_state,
                _scaffolding=_scaffolding,
            )

        for sensor in self.sensors:
            parent_name = self.name
            child_name = f"{self.name}::{sensor.name}"

            parent = declared_frames[parent_name]
            child = declared_frames[child_name]

            parent_static = _scaffolding[parent_name]
            child_static = _scaffolding[child_name]

            link = tf.CompundLink(parent_static.links_between(child_static))
            link(parent, child)

            sensor.to_dynamic_graph(
                declared_frames,
                f"{self.name}::{sensor.name}",
                seed=seed,
                shape=shape,
                axis=axis,
                apply_state=apply_state,
                _scaffolding=_scaffolding,
            )

        return declared_frames[self.name]

    class Damping(ElementBase):
        def __init__(
            self, *, linear: float = 0.0, angular: float = 0.0, sdf_version: str
        ) -> None:
            warnings.warn("`Link.Damping` has not been implemented yet.")
            super().__init__(sdf_version=sdf_version)

    class VelocityDecay(ElementBase):
        def __init__(
            self, *, linear: float = 0.0, angular: float = 0.0, sdf_version: str
        ) -> None:
            warnings.warn("`Link.VelocityDecay` has not been implemented yet.")
            super().__init__(sdf_version=sdf_version)
