from ..exceptions import ParseError
from typing import Dict, List, Any, Tuple
from itertools import chain
import warnings

from .base import (
    ElementBase,
    NamedPoseBearing,
    Pose,
    vector3,
    PoseBearing,
    StringElement,
    FloatElement,
)
from .model import Model
from .physics import Physics
from .light import Light
from .frame import Frame
from .scene import Scene
from .actor import Actor
from .joint import Joint
from .plugin import Plugin
from .state import State
from .include import Include
from .population import Population
from .atmosphere import Atmosphere
from .gui import Gui
from .... import transform as tf


class World(ElementBase):
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

        References to other SDF files that contain fragments
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
        .. deprecated:: SDFormat v1.6
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
        .. deprecated:: SDFormat v1.7
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
        The SDFormat version to use when constructing this element.

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
        .. deprecated:: SDFormat v1.6
            Use `physics_engines` instead.
    joints : List[Joint]
        .. deprecated:: SDFormat v1.7
            Use `Model.joints` instead and set `Model.joints.parent` to
            `world`.

    Notes
    -----
    The `includes` kwarg is resolved upon construction and the included fragmens
    are appended to `World.models`, `Worlds.actors`, or `Worlds.lights`
    respectively.

    The `populations` kwarg is resolved upon construction and generated models
    are appended to the list of `Worlds.models`.

    """

    def __init__(
        self,
        *,
        name: str = "",
        audio: "World.Audio" = None,
        wind: "World.Wind" = None,
        includes: List[Include],
        gravity: str = "0 0 -9.8",
        magnetic_field: str = "5.5645e-6 22.8758e-6 -42.3884e-6",
        atmosphere: "Atmosphere" = None,
        gui: "Gui" = None,
        physics_engine: Physics = None,
        physics_engines: List[Physics] = None,
        scene: Scene,
        lights: List[Light],
        frames: List[Frame],
        models: List[Model],
        actors: List[Actor],
        plugins: List[Plugin],
        joints: List[Joint] = None,
        roads: List["World.Road"],
        spherical_coordinates: "World.SphericalCoordinates" = None,
        states: List[State],
        populations: List["World.WorldPopulation"],
        sdf_version: str = "1.8",
    ) -> None:
        super().__init__(sdf_version=sdf_version)
        self.name = name
        self.audio = World.Audio(sdf_version=sdf_version) if audio is None else audio
        self.wind = World.Wind(sdf_version=sdf_version) if wind is None else wind
        self.gravity = vector3(gravity)
        self.magnetic_field = vector3(magnetic_field)
        self.atmosphere = (
            Atmosphere(sdf_version=sdf_version) if atmosphere is None else atmosphere
        )
        self.gui = Gui(sdf_version=sdf_version) if gui is None else gui
        if sdf_version in ["1.0", "1.2", "1.3", "1.4", "1.5"]:
            if physics_engines is not None:
                raise ValueError(
                    "`World.physics_engines` requires an SDF version newer than 1.5."
                )
            self.physics_engines = [] if physics_engine is None else [physics_engine]
        else:
            if physics_engine is not None:
                raise ValueError(
                    "`World.physics_engine` is deprecated. Use `physics_engines` instead."
                )
            self.physics_engines = [] if physics_engines is None else physics_engines
        self.scene = scene
        self.lights = lights
        self.frames = frames
        self.models = models
        self.actors = actors
        self.plugins = plugins
        self.populations = populations
        if sdf_version in ["1.0", "1.2", "1.3", "1.4", "1.5", "1.6"]:
            self._joints = [] if joints is None else joints
        elif joints is not None:
            raise ValueError(
                "`World.joints` is deprecated."
                "To connect a model to the world use `Model.canonical_link` instead."
            )
        else:
            self._joints = list()
        self.road = roads
        self.spherical_coordinates = (
            World.SphericalCoordinates()
            if spherical_coordinates is None
            else spherical_coordinates
        )
        self.state = states

        for include in includes:
            fragment = include.resolve()
            if isinstance(fragment, Model):
                self.models.append(fragment)
            elif isinstance(fragment, Actor):
                self.actors.append(fragment)
            else:
                self.lights.append(fragment)

        for frame in self.frames:
            if frame.attached_to is None:
                frame.attached_to = "world"

        el: PoseBearing
        pose_bearing: List[PoseBearing] = [
            # lights,
            self.frames,
            self.models,
            self._joints,
        ]
        for el in chain(*pose_bearing):
            if el.pose.relative_to is None:
                el.pose.relative_to = "world"

    @property
    def joints(self):
        warnings.warn(
            "`World.joints` has been deprecated. Use `Model.joints` with"
            " `Model.joints.parent = 'world'` instead.",
            DeprecationWarning,
        )
        return self._joints

    @classmethod
    def from_specific(cls, specific: Any, *, version: str) -> "World":
        world_args = {
            "includes": [
                Include.from_specific(x, version=version) for x in specific.include
            ],
            "scene": Scene.from_specific(specific.scene, version=version),
        }

        elements_with_default: Dict[str, ElementBase] = {
            "name": StringElement,
            "gravity": StringElement,
            "magnetic_field": StringElement,
            "audio": World.Audio,
            "wind": World.Wind,
            "atmosphere": Atmosphere,
            "gui": Gui,
            "spherical_coordinates": World.SphericalCoordinates,
        }
        list_elements: Dict[str, Tuple[str, ElementBase]] = {
            "include": ("includes", Include),
            "light": ("lights", Light),
            "frame": ("frames", Frame),
            "model": ("models", Model),
            "actor": ("actors", Actor),
            "plugin": ("plugins", Plugin),
            "road": ("roads", World.Road),
            "state": ("states", State),
            "population": ("populations", World.WorldPopulation),
        }

        args = cls._prepare_standard_args(
            specific, elements_with_default, list_elements, version=version
        )
        world_args.update(args)

        if version in ["1.0", "1.1", "1.2", "1.3", "1.4", "1.5"]:
            world_args["physics_engine"] = Physics.from_specific(
                specific.physics, version=version
            )
        else:
            world_args["physics_engines"] = [
                Physics.from_specific(x, version=version) for x in specific.physics
            ]

        if version in ["1.0", "1.1", "1.2", "1.3", "1.4", "1.5", "1.6"]:
            world_args["joints"] = [
                Joint.from_specific(x, version=version) for x in specific.joint
            ]

        return World(**world_args, sdf_version=version)

    def declared_frames(self) -> Dict[str, tf.Frame]:
        world_frame = tf.Frame(3, name=self.name)
        declared_frames = {"world": world_frame}

        for el in self.models:
            model_frames = el.declared_frames()
            declared_frames[el.name] = model_frames["__model__"]
            for name, frame in model_frames.items():
                declared_frames[f"{el.name}::{name}"] = frame

        for el in chain(self.frames, self._joints):
            declared_frames.update(el.declared_frames())

        return declared_frames

    def to_static_graph(
        self,
        declared_frames: Dict[str, tf.Frame],
        *,
        seed: int = None,
        shape: Tuple[int] = ...,
        axis: int = -1,
    ) -> tf.Frame:
        for model in self.models:
            scope = {
                name.split("::", 1)[1]: frame
                for name, frame in declared_frames.items()
                if name.startswith(f"{model.name}::")
            }
            scope["world"] = declared_frames["world"]
            model.to_static_graph(scope, seed=seed, shape=shape, axis=axis)

        for model in self.models:
            link = model.pose.to_tf_link()
            parent_name = model.pose.relative_to
            child_name = f"{model.name}::{model.placement_frame}"

            parent = declared_frames[parent_name]
            child = declared_frames[child_name]
            link(child, parent)

        for el in chain(self.frames, self._joints):
            link: tf.Link = el.pose.to_tf_link()
            parent_name = el.pose.relative_to
            child_name = el.name

            parent = declared_frames[parent_name]
            child = declared_frames[child_name]
            link(child, parent)

            el.to_static_graph(declared_frames, seed=seed, shape=shape, axis=axis)

        return declared_frames["world"]

    def to_dynamic_graph(
        self,
        declared_frames: Dict[str, tf.Frame],
        *,
        seed: int = None,
        shape: Tuple[int] = (3,),
        axis: int = -1,
        apply_state: bool = True,
        _scaffolding: Dict[str, tf.Frame] = None,
    ) -> tf.Frame:
        if _scaffolding is None:
            _scaffolding = self.declared_frames()
            self.to_static_graph(_scaffolding, seed=seed, shape=shape, axis=axis)

        for model in self.models:
            scaffold_scope = {
                name.split("::", 1)[1]: frame
                for name, frame in _scaffolding.items()
                if name.startswith(f"{model.name}::")
            }
            scaffold_scope["world"] = _scaffolding["world"]

            scope = {
                name.split("::", 1)[1]: frame
                for name, frame in declared_frames.items()
                if name.startswith(f"{model.name}::")
            }
            scope["world"] = declared_frames["world"]
            model.to_dynamic_graph(
                scope,
                seed=seed,
                shape=shape,
                axis=axis,
                apply_state=apply_state,
                _scaffolding=scaffold_scope,
            )

        for el in chain(self.frames, self._joints):
            el.to_dynamic_graph(
                declared_frames,
                seed=seed,
                shape=shape,
                axis=axis,
                apply_state=apply_state,
                _scaffolding=_scaffolding,
            )

        return declared_frames["world"]

    class Audio(ElementBase):
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

        def __init__(self, *, device: str = "default", sdf_version: str) -> None:
            super().__init__(sdf_version=sdf_version)
            self.uri = device

        @classmethod
        def from_specific(cls, specific: Any, *, version: str) -> "ElementBase":
            if specific is None:
                return World.Audio(sdf_version=version)
            return World.Audio(device=specific.device, sdf_version=version)

    class Wind(ElementBase):
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

        def __init__(self, *, linear_velocity: str = "0 0 0", sdf_version: str) -> None:
            self.linear_velocity = vector3(linear_velocity)

        @classmethod
        def from_specific(cls, specific: Any, *, version: str) -> "ElementBase":
            if specific is None:
                return World.Wind(sdf_version=version)
            return World.Wind(
                linear_velocity=specific.linear_velocity, sdf_version=version
            )

    class Road(ElementBase):
        def __init__(self, *, sdf_version: str) -> None:
            warnings.warn("`Road` has not been implemented yet.")
            super().__init__(sdf_version=sdf_version)

    class SphericalCoordinates(ElementBase):
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
            sdf_version: str,
        ) -> None:
            super().__init__(sdf_version=sdf_version)
            self.surface_model = surface_model
            self.world_frame_orientation = world_frame_orientation
            self.latitude_deg = latitude_deg
            self.longitude_deg = longitude_deg
            self.elevation = elevation
            self.heading_deg = heading_deg

        @classmethod
        def from_specific(cls, specific: Any, *, version: str) -> "World":
            elements_with_default: Dict[str, ElementBase] = {
                "surface_model": StringElement,
                "world_frame_orientation": StringElement,
                "latitude_deg": FloatElement,
                "longitude_deg": FloatElement,
                "elevation": FloatElement,
                "heading_deg": FloatElement,
            }
            generic_args = cls._prepare_standard_args(
                specific, elements_with_default, version=version
            )

            return cls(**generic_args, sdf_version=version)

    class WorldPopulation(Population):
        # def __init__(
        #     self,
        #     *,
        #     name: str,
        #     pose: Pose = None,
        #     model_count: int = 1,
        #     distribution: "Distribution",
        #     box: "Box" = None,
        #     cylinder: "Cylinder" = None,
        #     model: Model,
        #     frames: List[Frame] = None,
        # ) -> None:
        #     super().__init__(name=name, pose=pose)
        #     self.name=name
        #     self.model_count = model_count
        #     self.distribution = distribution
        #     self.box = box
        #     self.cylinder = cylinder
        #     self.model = model
        #     self.frames = frames

        #     if frames is None:
        #         self.frames = list()

        class Distribution(ElementBase):
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

        class Box(ElementBase):
            def __init__(self, *, size: Tuple[float] = (1, 1, 1)) -> None:
                self.size = size

        class Cylinder(ElementBase):
            def __init__(self, *, radius: float = 1, length: float = 1) -> None:
                self.radius = radius
                self.length = length
