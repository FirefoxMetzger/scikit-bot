""" Generic (oppinionated) Bindings for SDFormat

The classes below are a poor man's version of the data bindings in
sdformat.bindings. They only implement a subset of the full SDFormat spec
relevant to frame graphs, but are independent of any specific version.

The idea is that a converter for a specific SDF version takes SDF objects of that
version and converts them into the generic representation below. The generic
objects are then used to construct the actual frame graph.
"""


from typing import List, Tuple, Union
import numpy as np
from itertools import chain
from ..exceptions import ParseError
import warnings


class Version:
    def __init__(self, *, sdf_version: str = "1.8"):
        self.sdf_version = sdf_version


class Pose:
    def __init__(self, *, value: str = "0 0 0 0 0 0", relative_to: str = None) -> None:
        self.value = value
        self.relative_to = relative_to

        if self.relative_to == "":
            self.relative_to = None


class PoseBearing:
    def __init__(self, *, pose: Pose = None) -> None:
        self.pose = pose
        if self.pose is None:
            self.pose = Pose()


class NamedPoseBearing(PoseBearing):
    def __init__(self, *, name: str, pose: Pose = None) -> None:
        super().__init__(pose=pose)
        self.name = name


class Frame(NamedPoseBearing):
    def __init__(
        self, *, name: str, pose: Pose = None, attached_to: str = None
    ) -> None:
        super().__init__(name=name, pose=pose)
        self.attached_to = attached_to

        if self.attached_to == "":
            self.attached_to = None


class Sensor(NamedPoseBearing):
    def __init__(
        self,
        *,
        name: str,
        type: str,
        pose: Pose = None,
        camera: "Camera" = None,
        frames: List["Frame"] = None,
    ) -> None:
        super().__init__(name=name, pose=pose)
        self.type = type
        self.camera = camera
        self.frames = frames

        if frames is None:
            self.frames = list()

    class Camera(NamedPoseBearing):
        def __init__(
            self,
            *,
            name: str,
            pose: Pose = None,
            horizontal_fov: float = 1.047,
            image: "Image" = None,
            frames: "Frame" = None,
        ) -> None:
            super().__init__(name=name, pose=pose)
            self.horizontal_fov = horizontal_fov
            self.image = image
            self.frames = frames

            if self.frames is None:
                self.frames = list()

            if self.image is None:
                self.image = Sensor.Camera.Image()

        class Image:
            def __init__(
                self, *, width: int = 320, height: int = 240, format: str = "R8G8B8"
            ) -> None:
                self.width = width
                self.height = height
                self.format = format


class Joint(NamedPoseBearing):
    def __init__(
        self,
        *,
        name: str,
        kind: str,
        parent: str,
        child: str,
        axis: "Axis" = None,
        pose: Pose = None,
        sensor: List[Sensor] = None,
        frames: List["Frame"] = None,
    ) -> None:
        super().__init__(name=name, pose=pose)
        self.type = kind
        self.parent = parent
        self.child = child
        self.axis = axis
        self.sensor = sensor
        self.frames = frames

        if axis is None:
            self.axis = Joint.Axis()

        if self.axis.xyz.expressed_in is None:
            self.axis.xyz.expressed_in = self.child

        if frames is None:
            self.frames = list()

    class Axis:
        def __init__(self) -> None:
            self.xyz = Joint.Axis.Xyz()
            self.limit = Joint.Axis.Limit()

        class Xyz:
            def __init__(self, *, value: str = "0 0 1", expressed_in=None) -> None:
                self.value = value
                self.expressed_in = expressed_in

        class Limit:
            def __init__(
                self,
                *,
                lower: float = -1e17,
                upper: float = 1e17,
                effort: float = -1,
                velocity: float = -1,
                stiffness: float = 1e9,
                dissipation: float = 1,
            ) -> None:
                self.lower = lower
                self.upper = upper
                self.effort = effort
                self.velocity = velocity
                self.stiffness = stiffness
                self.dissipation = dissipation


class Link(NamedPoseBearing):
    def __init__(
        self,
        *,
        name: str,
        pose: Pose = None,
        must_be_base_link: bool = False,
        inertial: "Link.Inertial" = None,
        collisions: List[NamedPoseBearing],
        visuals: List[NamedPoseBearing],
        projector: NamedPoseBearing = None,
        audio_source_poses: List[Pose],
        sensors: List[Sensor],
        lights: List["Light"] = None,
        frames: List["Frame"] = None,
    ) -> None:
        super().__init__(name=name, pose=pose)
        self.must_be_base_link = must_be_base_link
        self.inertial = inertial
        self.projector = projector
        self.collision = collisions
        self.visual = visuals
        self.sensors = sensors
        self.lights = lights
        self.audio_sources = [PoseBearing(pose=p) for p in audio_source_poses]
        self.frames = frames

        if frames is None:
            self.frames = list()

        if lights is None:
            self.lights = list()

        for el in chain(
            visuals, collisions, self.audio_sources, sensors, self.lights, self.frames
        ):
            if el.pose.relative_to is None:
                el.pose.relative_to = name

        if projector is not None:
            if projector.pose.relative_to is None:
                projector.pose.relative_to = name

        # inertial frame is _forced_ to be relative to link
        if self.inertial is not None:
            self.inertial.pose.relative_to = name

    class Inertial(PoseBearing):
        def __init__(self, *, pose: Pose = None, frames: List["Frame"] = None) -> None:
            super().__init__(pose=pose)
            self.frames = frames

            if self.frames is None:
                self.frames = list()


class Light(NamedPoseBearing):
    def __init__(
        self,
        *,
        name: str,
        pose: Pose = None,
        frames: List["Frame"] = None,
    ) -> None:
        super().__init__(name=name, pose=pose)

        self.frames = frames

        if frames is None:
            self.frames = list()


class Include(NamedPoseBearing):
    def __init__(
        self,
        *,
        name: str,
        pose: Pose = None,
        placement_frame: str = None,
        uri: str,
    ) -> None:
        super().__init__(name=name, pose=pose)
        self.placement_frame = placement_frame
        self.uri = uri
        if pose is None:
            # here pose is None means no overwrite
            self.pose = None


class Model(NamedPoseBearing):
    def __init__(
        self,
        *,
        name: str,
        pose: Pose = None,
        placement_frame: str = None,
        canonical_link: str = None,
        links: List[Link],
        include: List[Include],
        models: List["Model"],
        frames: List[Frame],
        joints: List[Joint],
    ) -> None:
        super().__init__(name=name, pose=pose)
        self.placement_frame = placement_frame
        self.canonical_link = canonical_link
        self.links = links
        self.include = include
        self.models = models
        self.frames = frames
        self.joints = joints

        if self.canonical_link is None:
            if len(links) > 0:
                self.canonical_link = links[0].name
            elif len(include) > 0:
                self.canonical_link = include[0].name
            elif len(models) > 0:
                self.canonical_link = f"{models[0].name}::{models[0].canonical_link}"
            else:
                raise ParseError(f"Can not determine canonical link of `{name}`.")

        if self.placement_frame is None:
            self.placement_frame = "__model__"

        implicit_frames = [el.name for el in chain(models, include)]
        all_frames = [el.name for el in chain(links, include, models, frames, joints)]
        unique_frames = set(all_frames)

        if len(all_frames) != len(unique_frames):
            duplicated = [name for x in unique_frames if all_frames.count(x) > 1]
            raise ParseError(
                f"Non-unique frame names encountered for names: {duplicated}"
            )

        el: PoseBearing
        pose_bearing: List[PoseBearing] = [
            links,
            joints,
            [x for x in include if x.pose is not None],
            models,
            frames,
        ]
        for el in chain(*pose_bearing):
            relative_to = el.pose.relative_to
            if relative_to is None:
                el.pose.relative_to = "__model__"
            elif relative_to in implicit_frames:
                el.pose.relative_to += "::__model__"

        for frame in self.frames:
            if frame.attached_to is None:
                frame.attached_to = "__model__"
            elif frame.attached_to in implicit_frames:
                frame.attached_to = frame.attached_to + "::__model__"


class Actor(NamedPoseBearing):
    pass


class World:
    """ A simulation World
    
    
    """

    def __init__(
        self,
        *,
        name: str,
        includes: List[Include],
        lights: List[Light],
        frames: List[Frame],
        models: List[Model],
        population: List["Population"],
    ) -> None:
        self.name = name
        self.includes = includes
        self.lights = lights
        self.frames = frames
        self.models = models
        self.population = population

        implicit_frames = [el.name for el in chain(models, includes)]
        all_frames = [el.name for el in chain(models, frames, population)]
        unique_frames = set(all_frames)

        if len(all_frames) != len(unique_frames):
            duplicated = [name for x in unique_frames if all_frames.count(x) > 1]
            raise ParseError(
                f"Non-unique frame names encountered for names: {duplicated}"
            )

        el: PoseBearing
        pose_bearing: List[PoseBearing] = [
            [x for x in includes if x.pose is not None],
            lights,
            frames,
            models,
            population,
        ]
        for el in chain(*pose_bearing):
            if el.pose.relative_to is None:
                el.pose.relative_to = "world"
            elif el.pose.relative_to in implicit_frames:
                el.pose.relative_to = el.pose.relative_to + "::__model__"

        for frame in self.frames:
            if frame.attached_to is None:
                frame.attached_to = "world"
            elif frame.attached_to in implicit_frames:
                frame.attached_to = frame.attached_to + "::__model__"

    class Population(NamedPoseBearing):
        def __init__(
            self,
            *,
            name: str,
            pose: Pose = None,
            model_count: int = 1,
            distribution: "Distribution",
            box: "Box" = None,
            cylinder: "Cylinder" = None,
            model: Model,
            frames: List[Frame] = None,
        ) -> None:
            super().__init__(name=name, pose=pose)
            self.model_count = model_count
            self.distribution = distribution
            self.box = box
            self.cylinder = cylinder
            self.model = model
            self.frames = frames

            if frames is None:
                self.frames = list()

        class Distribution:
            def __init__(
                self,
                *,
                kind: str = "random",
                rows: int = 1,
                cols: int = 1,
                step: Tuple[float] = (0.5, 0.5, 0),
            ):
                self.type = kind
                self.rows = rows
                self.cols = cols
                self.step = step

        class Box:
            def __init__(self, *, size: Tuple[float] = (1, 1, 1)) -> None:
                self.size = size

        class Cylinder:
            def __init__(self, *, radius: float = 1, length: float = 1) -> None:
                self.radius = radius
                self.length = length


class Sdf(Version):
    """SDFormat Base Element

    This element is a container for multiple simulation worlds (can be one) or
    for a single fragment of a world (Model, Actor, Light).

    Parameters
    ----------
    payload : Union[List[World], Model, Light, Actor]
        The element contained in this SDF. This can be one :class:`Model`, one :class`Actor`, one
        :class:`Light`, or a list of :class`Worlds`.
    version : str
        The SDFormat version.
    worlds : List[World]
        .. depreciated:: SDFormat v1.8
            Worlds, models, lights, and/or actors can no longer be combined. Use
            `payload` instead.
        The worlds contained in this SDF.
    models : List[Model]
        .. depreciated:: SDFormat v1.8
            Starting with SDFormat v1.8 only a single model is supported. Use the
            `model` kwarg instead.

        The models contained in this SDF.
    lights : List[Light]
        .. depreciated:: SDFormat v1.8
            Starting with SDFormat v1.8 only a single light is supported. Use the
            `light` kwarg instead.

        The lights contained in this SDF.
    actors : List[Actor]
        .. depreciated:: SDFormat v1.8
            Starting with SDFormat v1.8 only a single actor is supported. Use the
            `actor` kwarg instead.

        The actors contained in this SDF.

    Attributes
    ----------
    worlds : List[World]
        The worlds contained in the SDF file.
    model: Model
        The model contained in the SDF file.
    light: Light
        The light contained in the SDF file.
    actor: Actor
        The actor contained in the SDF file.
    version : str
        The SDFormat version.
    models : List[Model]
        .. depreciated:: SDFormat v1.8
            Use the `Sdf.model` instead.
    lights : List[Light]
        .. depreciated:: SDFormat v1.8
            Use the `Sdf.light` instead.
    actors : List[Actor]
        .. depreciated:: SDFormat v1.8
            Use the `Sdf.actor` instead.

    """

    def __init__(
        self,
        *,
        payload: Union[List[World], Model, Light, Actor] = None,
        version: str = "1.8",
        worlds: List[World] = None,
        models: List[Model] = None,
        lights: List[Light] = None,
        actors: List[Actor] = None,
    ) -> None:
        super().__init__(sdf_version=version)
        self.version = version
        self._worlds = []
        self._actors = []
        self._models = []
        self._lights = []

        if self.sdf_version == "1.8":
            if worlds is not None:
                raise ValueError(
                    "`Sdf` does not support the `worlds` kwarg for SDFormat v1.8. Use `payload` instead."
                )
            if actors is not None:
                raise ParseError("`Sdf` only supports a single actor in SDFormat v1.8.")
            if models is not None:
                raise ParseError("`Sdf` only supports a single model in SDFormat v1.8.")
            if lights is not None:
                raise ParseError("`Sdf` only supports a single light in SDFormat v1.8.")

            if isinstance(payload, list) and all(
                [isinstance(x, World) for x in payload]
            ):
                self._worlds = payload
            elif isinstance(payload, Actor):
                self._actors.append(payload)
            elif isinstance(payload, Model):
                self._models.append(payload)
            elif isinstance(payload, Light):
                self._lights.append(payload)
            else:
                raise ParseError("Invalid `Sdf` element.")
        elif version in ["1.7", "1.6", "1.5", "1.4", "1.3"]:
            if payload is not None:
                raise ParseError(
                    "`Sdf` does not support `payload` prior to SDFormat v1.8."
                )
            if worlds is None:
                raise ValueError("`Sdf` must specify `worlds` prior to SDFormat v1.8.")
            if actors is None:
                raise ValueError("`Sdf` must specify `actors` prior to SDFormat v1.8.")
            if models is None:
                raise ValueError("`Sdf` must specify `models` prior to SDFormat v1.8.")
            if lights is None:
                raise ValueError("`Sdf` must specify `lights` prior to SDFormat v1.8.")

            self._worlds = worlds
            self._models = models
            self._lights = lights
            self._actors = actors
        else:
            raise ParseError("`Sdf` does not exist prior to SDFormat v1.3.")

    @property
    def worlds(self) -> List[World]:
        if len(self._worlds) == 0:
            raise AttributeError("`Sdf` does not contain any worlds.")

        return self._worlds

    @property
    def actor(self) -> Actor:
        try:
            return self._actors[0]
        except IndexError:
            raise AttributeError("`Sdf` does not contain an actor.") from None

    @property
    def model(self) -> Model:
        try:
            return self._models[0]
        except IndexError:
            raise AttributeError("`Sdf` does not contain a model.") from None

    @property
    def light(self) -> Light:
        try:
            return self._lights[0]
        except IndexError:
            raise AttributeError("`Sdf` does not contain a light.") from None

    # Depreciated properties
    @property
    def actors(self) -> List[Actor]:
        warnings.warn(
            "`sdf.actors` is depreciated since SDFormat v1.8. Use `sdf.actor` instead.",
            DeprecationWarning,
        )
        return self._actors

    @property
    def models(self) -> List[Model]:
        warnings.warn(
            "`sdf.models` is depreciated since SDFormat v1.8. Use `sdf.models` instead.",
            DeprecationWarning,
        )
        return self._models

    @property
    def lights(self) -> List[Light]:
        warnings.warn(
            "`sdf.lights` is depreciated since SDFormat v1.8. Use `sdf.lights` instead.",
            DeprecationWarning,
        )
        return self._lights
