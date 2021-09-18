""" Generic (oppinionated) Bindings for SDFormat

The classes below are a poor man's version of the data bindings in
sdformat.bindings. They only implement a subset of the full SDFormat spec
relevant to frame graphs, but are independent of any specific version.

The idea is that a converter for a specific SDF version takes SDF objects of that
version and converts them into the generic representation below. The generic
objects are then used to construct the actual frame graph.
"""


from typing import List, Tuple, Union, Any
import numpy as np
from itertools import chain
from ..exceptions import ParseError
import warnings


def vector3(value: str):
    return np.fromstring(value, dtype=float, count=3, sep=" ")


class Version:
    def __init__(self, *, sdf_version: str):
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

    @classmethod
    def from_specific(cls, light:Any, *, version:str) -> "Light":
        raise NotImplementedError()


class Include(Version):
    # world defines its first include internally in v 1.4
    # world modifies its include in v1.5
    def __init__(
        self,
        *,
        uri: str,
        name: str = None,
        static: bool = None,
        pose: Pose = None,
        plugin: List["Plugin"] = None,
        placement_frame: str = None,
        sdf_version: str,
    ) -> None:
        super().__init__(sdf_version=sdf_version)
        self.uri = uri
        self.name = name
        self.static = static
        self.pose = pose
        self.plugin = [] if plugin is None else plugin
        self.placement_frame = placement_frame

        if self.placement_frame is not None:
            if self.pose is None:
                raise ParseError(
                    "`Include`s that specify `Include.placement_frame`"
                    " must also specify `Include.pose`."
                )

    def resolve(self) -> Union["Model", "Light", "Actor"]:
        pass


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

    @classmethod
    def from_specific(cls, model:Any, *, version:str) -> "Model":
        raise NotImplementedError()


class Actor(NamedPoseBearing):
    @classmethod
    def from_specific(cls, actor:Any, *, version:str) -> "Actor":
        raise NotImplementedError()


class Scene:
    pass


class Physics:
    pass


class Plugin:
    pass


class State:
    pass

class World(Version):
    """A simulation world

    The world element is a container for all information related to a single
    simulation.

    Parameters
    ----------
    name : str
        .. versionadded:: SDFormat v1.2

        The name of the world. It must be unique among all worlds in the same
        :class:`Sdf` container.
    audio: World.Audio
        .. versionadded:: SDFormat v1.4

        The simulations global audio properties.
    wind : World.Wind
        .. versionadded:: SDFormat v1.6

        The direction and strength of the wind. Currently only constant wind
        is supported.

    includes : "World.Include"
        .. versionadded:: SDFormat v1.4

        References to other SDF files that contain world fragments
        (:class:`Model`s, :class:`Light`s, :class:`Actor`s) to include in the
        simulation.

    gravity : str
        .. versionadded:: SDFormat v1.6

        The gravity in m/s^2, expressed in a coordinate frame defined by the
        spherical_coordinates attribute. The default is "0 0 -9.8".

    magnetic_field : str
        .. versionadded:: SDFormat v1.6

        The magnetic field vector in Tesla, expressed in a coordinate frame
        defined by the spherical_coordinates attribute. The default is
        "5.5645e-6 22.8758e-6 -42.3884e-6".
    atmosphere : World.Atmosphere
        .. versionadded:: SDFormat v1.6

        The atmosphere model to use.
    gui : World.Gui
        Layout of the Ignition Gazebo GUI. (Applications other than Gazebo will
        likely not need this.)
    physics_engine : Physics
        .. depreciated:: SDFormat v1.6
            Use `physics_engines` instead.

        Configuration parameters of the dynamics engine.
    physics_engines : List[Physics]
        .. versionadded:: SDFormat v1.6

        Configuration parameters of the dynamics engine.
    scene : Scene
        Ambience configuration of the world (skybox, ambient light, etc.)
    lights : List[Light]
        A list of light sources of the world.
    frames : List[Frame]
        .. versionadded:: SDFormat v1.7

        A list of reference frames used to ease the positioning of objects.
    models : List[Model]
        A list of models used in this simulation.
    actors : List[Actor]
        A list of actors used in this simulation.
    plugins : List[Plugin]
        A list of plugins used to customize the runtime behavior of the
        simulation.
    joints : List[Joint]
        .. depreciated:: SDFormat v1.7
            To attach models to the world, use the canonical_link kwarg
            instead. All other usage of `joints` has no replacement.

        A list of connections between two :class:`Link`s that constrains
        their relative movement.
    road : List[World.Road]
        A list of roads used in this simulation.
    spherical_coordinates : World.SphericalCoordinates
        .. versionadded:: SDFormat v1.4

        Simulator root frame location.

    state : List[State]
        The current state of this simulation.
    population : List["Population"]
        .. versionadded:: SDFormat v1.5

        A group of models that is procedually inserted into the simulation.
    sdf_version : str
        The SDFormat version to use when construction this element.

    Attributes
    ----------
    name : str
        The name of the world.
    audio: World.Audio
        The simulations global audio properties.
    wind : World.Wind
        The direction and strength of the wind.
    gravity : np.ndarray
        The gravity in m/s^2, expressed in a coordinate frame defined by the
        spherical_coordinates attribute.
    magnetic_field : np.ndarray
        The magnetic field vector in Tesla, expressed in a coordinate frame
        defined by the spherical_coordinates attribute.
    atmosphere : World.Atmosphere
        The atmosphere model to use.
    gui : World.Gui
        Layout of the Ignition Gazebo GUI.
    physics_engines : List[Physics]
        Configuration parameters of the dynamics engine(s).
    scene : Scene
        Ambience configuration of the world (skybox, ambient light, etc.)
    lights : List[Light]
        A list of light sources of the world.
    frames : List[Frame]
        A list of reference frames used to ease the positioning of objects.
    models : List[Model]
        A list of models used in this simulation.
    actors : List[Actor]
        A list of actors used in this simulation.
    plugins : List[Plugin]
        A list of plugins used to customize the runtime behavior of the
        simulation.
    road : List[World.Road]
        A list of roads used in this simulation.
    spherical_coordinates : World.SphericalCoordinates
        Simulator root frame location.
    state : List[State]
        The current state of this simulation.

    physics_engine : Physics
        .. depreciated:: SDFormat v1.6
            Use `physics_engines` instead.
    joints : List[Joint]
        .. depreciated:: SDFormat v1.7
            To attach models to the world, use the canonical_link kwarg
            instead. All other usage of `joints` has no replacement.

    Notes
    -----
    The `includes` kwarg is resolved upon construction and the included fragmens
    are appended to `World.models`, `Worlds.actors`, or `Worlds.lights`
    respectively.

    The `populations` kwarg is resolved upon construction and generated models
    are appended to the list of `Worlds.models`.

    Implicit frames defined by `Worlds.models` and `Models.joints` are appended
    to the list of `World.frames`.

    """

    def __init__(
        self,
        *,
        name: str = None,
        audio: "World.Audio" = None,
        wind: "World.Wind" = None,
        includes: List["World.WorldInclude"],
        gravity: str = "0 0 -9.8",
        magnetic_field: str = "5.5645e-6 22.8758e-6 -42.3884e-6",
        atmosphere: "World.Atmosphere",
        gui: "World.Gui" = None,
        physics_engine: Physics = None,
        physics_engines: List[Physics] = None,
        scene: Scene,
        lights: List[Light],
        frames: List[Frame],
        models: List[Model],
        actors: List[Actor],
        plugins: List[Plugin],
        joints: List[Joint] = None,
        road: List["World.Road"],
        spherical_coordinates: "World.SphericalCoordinates" = None,
        state: List[State],
        population: List["World.Population"],
        sdf_version: str = "1.8",
    ) -> None:
        super().__init__(sdf_version=sdf_version)
        self.name = "" if name is None else name
        self.audio = World.Audio() if audio is None else audio
        self.wind = World.Wind() if wind is None else wind
        self.gravity = vector3(gravity)
        self.magnetic_field = vector3(magnetic_field)
        self.atmosphere = atmosphere
        self.gui = World.Gui() if gui is None else gui
        if sdf_version in ["1.0", "1.2", "1.3", "1.4", "1.5"]:
            if physics_engines is not None:
                raise ValueError(
                    "`World.physics_engines` requires an SDF version newer than 1.5."
                )
            self.physics_engines = [] if physics_engine is None else [physics_engine]
        else:
            if physics_engine is not None:
                raise ValueError(
                    "`World.physics_engine` is depreciated. Use `physics_engines` instead."
                )
            self.physics_engines = [] if physics_engines is None else physics_engines
        self.scene = scene
        self.lights = lights
        self.frames = frames
        self.models = models
        self.actors = actors
        self.plugins = plugins
        if sdf_version in ["1.0", "1.2", "1.3", "1.4", "1.5", "1.6"]:
            self.joints = [] if joints is None else joints
        elif self.joints is not None:
            raise ValueError(
                "`World.joints` is depreciated."
                "To connect a model to the world use `Model.canonical_link` instead."
            )
        self.road = road
        self.spherical_coordinates = (
            World.SphericalCoordinates()
            if spherical_coordinates is None
            else spherical_coordinates
        )
        self.state = state

        includes: List["World.WorldInclude"]
        population: List["World.Population"]

        for model in self.models:
            self.frames.append(
                Frame(
                    name=model.name,
                    pose=model.pose,
                    attached_to=f"{model.name}::{model.canonical_link}",
                )
            )

        for frame in self.frames:
            if frame.attached_to is None:
                frame.attached_to = "world"
            elif frame.attached_to == "":
                frame.attached_to = "world"

        frame_names = [el.name for el in self.frames]
        unique_names = set(frame_names)

        if len(frame_names) != len(unique_names):
            duplicated = [name for x in unique_names if frame_names.count(x) > 1]
            raise ParseError(
                f"Non-unique frame names encountered for names: {duplicated}"
            )

        el: PoseBearing
        pose_bearing: List[PoseBearing] = [
            lights,
            frames,
            models,
        ]
        for el in chain(*pose_bearing):
            if el.pose.relative_to is None:
                el.pose.relative_to = "world"

    class Audio:
        """Global audio properties.

        Parameters
        ----------
        uri : str
            Device to use for audio playback. If None it will be set to
            "default".

        Attributes
        ----------
        uri : str
            The audio device to use.

        """

        def __init__(self, *, uri: str = None) -> None:
            if uri is None:
                self.uri = "default"
            else:
                self.uri = uri

    class Wind:
        """The type and properties of the wind in the world.

        Parameters
        ----------
        linear_velocity : str
            The direction and strength of the wind. Default is "0 0 0", meaning
            no wind.

        Attributes
        ----------
        linear_velocity : np.ndarray
            The direction and strength of the wind's velocity.

        """

        def __init__(self, *, linear_velocity: str = "0 0 0") -> None:
            self.linear_velocity = vector3(linear_velocity)

    class WorldInclude(Include):
        pass

    class Atmosphere:
        def __init__(self) -> None:
            warnings.warn("The `atmosphere` element has not been implemented yet.")

    class Gui:
        def __init__(self) -> None:
            warnings.warn("The `gui` element has not been implemented yet.")

    class Road:
        def __init__(self) -> None:
            warnings.warn("The `Road` element has not been implemented yet.")

    class SphericalCoordinates:
        """Simulator root frame location.

        SphericalCoordnates are used to specify the location of the simulation's
        root frame on Earth using a chosen surface model.

        Parameters
        ----------
        surface_model : str
            Name of planetary surface model, used to determine the surface
            altitude at a given latitude and longitude. The default is an
            ellipsoid model of the earth based on the WGS-84 standard. It is
            used in Gazebo's GPS sensor implementation.
        world_frame_orientation : str
            This field identifies how Gazebo world frame is aligned in
            Geographical sense.  The final Gazebo world frame orientation is
            obtained by rotating a frame aligned with following notation by the
            field heading_deg (Note that heading_deg corresponds to positive yaw
            rotation in the NED frame, so it's inverse specifies positive
            Z-rotation in ENU or NWU). Options are:
                - ENU (East-North-Up; default)
                - NED (North-East-Down)
                - NWU (North-West-Up)
            For example, world frame specified by setting
            world_orientation="ENU" and heading_deg=-90° is effectively
            equivalent to NWU with heading of 0°.
        latitude_deg : float
            Geodetic latitude at origin of gazebo reference frame, specified in
            units of degrees. The default is 0.0.
        longitude_deg : float
            Longitude at origin of gazebo reference frame, specified in units of
            degrees. The default is 0.0.
        elevation : float
            Elevation of origin of gazebo reference frame, specified in meters.
            The default is 0.0.
        heading_deg : float
            Heading offset of gazebo reference frame, measured as angle between
            East and gazebo x axis, or equivalently, the angle between North and
            gazebo y axis. The angle is specified in degrees. The default is
            0.0.

        Attributes
        ----------
        surface_model : str
            The name of planetary surface model.
        world_frame_orientation : str
            Reference orientation for frame alignment.
        latitude_deg : float
            Geodetic latitude at origin of the root frame.
        longitude_deg : float
            Longitude at origin of the root frame.
        elevation : float
            Elevation of origin of the root frame.
        heading_deg : float
            Angle (in degrees) between the root's y-axis and magnetic north.
        """

        def __init__(
            self,
            *,
            surface_model: str = "EARTH_WGS84",
            world_frame_orientation: str = "ENU",
            latitude_deg: float = 0.0,
            longitude_deg: float = 0.0,
            elevation: float = 0.0,
            heading_deg: float = 0.0,
        ) -> None:
            self.surface_model = surface_model
            self.world_frame_orientation = world_frame_orientation
            self.latitude_deg = latitude_deg
            self.longitude_deg = longitude_deg
            self.elevation = elevation
            self.heading_deg = heading_deg

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

    @classmethod
    def from_specific(cls, world: Any, *, version: str) -> "World":
        raise NotImplementedError()


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

    @classmethod
    def from_specific(cls, sdf: Any, *, version: str) -> "Sdf":
        """Create a generic Sdf object from a specific one.

        Parameters
        ----------
        sdf : Any
            The SDF object that should be turned into a generic object. It
            can come from any version of the specific SDFormat bindings
            provided by scikit-bot.
        version : str
            The version of the given SDF element.

        Returns
        -------
        generic_sdf : Sdf
            The generic equivalent of the provided specific Sdf object.
        """

        if version == "1.8":
            payload: Union[List[World], Model, Light, Actor]
            if sdf.world is not None and len(sdf.world) > 0:
                payload = [World.from_specific(x, version=version) for x in sdf.world]
            elif sdf.actor is not None:
                payload = Actor.from_specific(sdf.actor, version=version)
            elif sdf.model is not None:
                payload = Model.from_specific(sdf.model, version=version)
            elif sdf.light is not None:
                payload = Light.from_specific(sdf.light, version=version)
            else:
                raise ParseError("Can not convert `sdf` element without payload.")

            return Sdf(payload=payload, version=version)
        else:
            return Sdf(
                worlds=[World.from_specific(x, version=version) for x in sdf.world],
                actors=[Actor.from_specific(x, version=version) for x in sdf.actor],
                models=[Model.from_specific(x, version=version) for x in sdf.model],
                lights=[Light.from_specific(x, version=version) for x in sdf.light],
                version=version,
            )
