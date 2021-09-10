from dataclasses import dataclass, field
from typing import List, Optional
from .actor import Actor
from .light import Light
from .material import Material
from .model import Model
from .physics import Physics
from .scene import Scene
from .state import State

__NAMESPACE__ = "sdformat/v1.8/world.xsd"


@dataclass
class World:
    """
    The world element encapsulates an entire world description including:
    models, scene, physics, and plugins.

    Parameters
    ----------
    audio: Global audio properties.
    wind: The wind tag specifies the type and properties of the wind.
    include: Include resources from a URI. Included resources can only
        contain one 'model', 'light' or 'actor' element. The URI can
        point to a directory or a file. If the URI is a directory, it
        must conform to the model database structure (see
        /tutorials?tut=composition&amp;cat=specification&amp;#defining-
        models-in-separate-files).
    gravity: The gravity vector in m/s^2, expressed in a coordinate
        frame defined by the spherical_coordinates tag.
    magnetic_field: The magnetic vector in Tesla, expressed in a
        coordinate frame defined by the spherical_coordinates tag.
    atmosphere: The atmosphere tag specifies the type and properties of
        the atmosphere model.
    gui:
    physics: The physics tag specifies the type and properties of the
        dynamics engine.
    scene: Specifies the look of the environment.
    light: The light element describes a light source.
    frame: A frame of reference to which a pose is relative.
    model: The model element defines a complete robot or any other
        physical object.
    actor: A special kind of model which can have a scripted motion.
        This includes both global waypoint type animations and skeleton
        animations.
    plugin: A plugin is a dynamically loaded chunk of code. It can exist
        as a child of world, model, and sensor.
    road:
    spherical_coordinates:
    state:
    population: The population element defines how and where a set of
        models will     be automatically populated in Gazebo.
    name: Unique name of the world
    """

    class Meta:
        name = "world"

    audio: Optional["World.Audio"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    wind: Optional["World.Wind"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    include: List["World.Include"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    gravity: str = field(
        default="0 0 -9.8",
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
            "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
        },
    )
    magnetic_field: str = field(
        default="5.5645e-6 22.8758e-6 -42.3884e-6",
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
            "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
        },
    )
    atmosphere: Optional["World.Atmosphere"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    gui: Optional["World.Gui"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    physics: List[Physics] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
            "min_occurs": 1,
        },
    )
    scene: Optional[Scene] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    light: List[Light] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    frame: List["World.Frame"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    model: List[Model] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    actor: List[Actor] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    plugin: List["World.Plugin"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    road: List["World.Road"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    spherical_coordinates: Optional["World.SphericalCoordinates"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    state: List[State] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    population: List["World.Population"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )

    @dataclass
    class Audio:
        """
        Global audio properties.

        Parameters
        ----------
        device: Device to use for audio playback. A value of "default"
            will use the system's default audio device. Otherwise,
            specify a an audio device file"
        """

        device: str = field(
            default="default",
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )

    @dataclass
    class Wind:
        """
        The wind tag specifies the type and properties of the wind.

        Parameters
        ----------
        linear_velocity: Linear velocity of the wind.
        """

        linear_velocity: str = field(
            default="0 0 0",
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
                "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
            },
        )

    @dataclass
    class Include:
        """Include resources from a URI.

        Included resources can only contain one 'model', 'light' or 'actor' element. The URI can point to a directory or a file. If the URI is a directory, it must conform to the model database structure (see /tutorials?tut=composition&amp;cat=specification&amp;#defining-models-in-separate-files).

        Parameters
        ----------
        uri: URI to a resource, such as a model
        name: Override the name of the included entity.
        static: Override the static value of the included entity.
        placement_frame: The frame inside the included entity whose pose
            will be set by the specified pose element. If this element
            is specified, the pose must be specified.
        pose: A position(x,y,z) and orientation(roll, pitch yaw) with
            respect to the frame named in the relative_to attribute.
        plugin: A plugin is a dynamically loaded chunk of code. It can
            exist as a child of world, model, and sensor.
        """

        uri: str = field(
            default="__default__",
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        name: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        static: bool = field(
            default=False,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        placement_frame: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        pose: Optional["World.Include.Pose"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        plugin: List["World.Include.Plugin"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

        @dataclass
        class Pose:
            """
            Parameters
            ----------
            value:
            relative_to: Name of frame relative to which the pose is
                applied.
            """

            value: str = field(
                default="0 0 0 0 0 0",
                metadata={
                    "required": True,
                    "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){5}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
                },
            )
            relative_to: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                },
            )

        @dataclass
        class Plugin:
            """A plugin is a dynamically loaded chunk of code.

            It can exist as a child of world, model, and sensor.

            Parameters
            ----------
            any_element: This is a special element that should not be
                specified in an SDFormat file. It automatically copies
                child elements into the SDFormat element so that a
                plugin can access the data.
            name: A unique name for the plugin, scoped to its parent.
            filename: Name of the shared library to load. If the
                filename is not a full path name, the file will be
                searched for in the configuration paths.
            """

            any_element: List[object] = field(
                default_factory=list,
                metadata={
                    "type": "Wildcard",
                    "namespace": "##any",
                },
            )
            name: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                    "required": True,
                },
            )
            filename: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                    "required": True,
                },
            )

    @dataclass
    class Atmosphere:
        """
        The atmosphere tag specifies the type and properties of the atmosphere
        model.

        Parameters
        ----------
        temperature: Temperature at sea level in kelvins.
        pressure: Pressure at sea level in pascals.
        temperature_gradient: Temperature gradient with respect to
            increasing altitude at sea level in units of K/m.
        type: The type of the atmosphere engine. Current options are
            adiabatic.  Defaults to adiabatic if left unspecified.
        """

        temperature: float = field(
            default=288.15,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        pressure: float = field(
            default=101325.0,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        temperature_gradient: float = field(
            default=-0.0065,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        type: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
            },
        )

    @dataclass
    class Gui:
        """
        Parameters
        ----------
        camera:
        plugin: A plugin is a dynamically loaded chunk of code. It can
            exist as a child of world, model, and sensor.
        fullscreen:
        """

        camera: Optional["World.Gui.Camera"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        plugin: List["World.Gui.Plugin"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        fullscreen: bool = field(
            default=False,
            metadata={
                "type": "Attribute",
            },
        )

        @dataclass
        class Camera:
            """
            Parameters
            ----------
            view_controller:
            projection_type: Set the type of projection for the camera.
                Valid values are "perspective" and "orthographic".
            track_visual:
            pose: A position(x,y,z) and orientation(roll, pitch yaw)
                with respect to the frame named in the relative_to
                attribute.
            name:
            """

            view_controller: str = field(
                default="orbit",
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            projection_type: str = field(
                default="perspective",
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            track_visual: Optional["World.Gui.Camera.TrackVisual"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            pose: Optional["World.Gui.Camera.Pose"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            name: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                    "required": True,
                },
            )

            @dataclass
            class TrackVisual:
                """
                Parameters
                ----------
                name: Name of the tracked visual. If no name is
                    provided, the remaining settings will be applied
                    whenever tracking is triggered in the GUI.
                min_dist: Minimum distance between the camera and the
                    tracked visual. This parameter is only used if
                    static is set to false.
                max_dist: Maximum distance between the camera and the
                    tracked visual. This parameter is only used if
                    static is set to false.
                static: If set to true, the position of the camera is
                    fixed relatively to the model or to the world,
                    depending on the value of the use_model_frame
                    element. Otherwise, the position of the camera may
                    vary but the distance between the camera and the
                    model will depend on the value of the min_dist and
                    max_dist elements. In any case, the camera will
                    always follow the model by changing its orientation.
                use_model_frame: If set to true, the position of the
                    camera is relative to the model reference frame,
                    which means that its position relative to the model
                    will not change. Otherwise, the position of the
                    camera is relative to the world reference frame,
                    which means that its position relative to the world
                    will not change. This parameter is only used if
                    static is set to true.
                xyz: The position of the camera's reference frame. This
                    parameter is only used if static is set to true. If
                    use_model_frame is set to true, the position is
                    relative to the model reference frame, otherwise it
                    represents world coordinates.
                inherit_yaw: If set to true, the camera will inherit the
                    yaw rotation of the tracked model. This parameter is
                    only used if static and use_model_frame are set to
                    true.
                """

                name: str = field(
                    default="__default__",
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                min_dist: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                max_dist: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                static: bool = field(
                    default=False,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                use_model_frame: bool = field(
                    default=True,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                xyz: str = field(
                    default="-5.0 0.0 3.0",
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                        "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
                    },
                )
                inherit_yaw: bool = field(
                    default=False,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )

            @dataclass
            class Pose:
                """
                Parameters
                ----------
                value:
                relative_to: Name of frame relative to which the pose is
                    applied.
                """

                value: str = field(
                    default="0 0 0 0 0 0",
                    metadata={
                        "required": True,
                        "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){5}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
                    },
                )
                relative_to: Optional[str] = field(
                    default=None,
                    metadata={
                        "type": "Attribute",
                    },
                )

        @dataclass
        class Plugin:
            """A plugin is a dynamically loaded chunk of code.

            It can exist as a child of world, model, and sensor.

            Parameters
            ----------
            any_element: This is a special element that should not be
                specified in an SDFormat file. It automatically copies
                child elements into the SDFormat element so that a
                plugin can access the data.
            name: A unique name for the plugin, scoped to its parent.
            filename: Name of the shared library to load. If the
                filename is not a full path name, the file will be
                searched for in the configuration paths.
            """

            any_element: List[object] = field(
                default_factory=list,
                metadata={
                    "type": "Wildcard",
                    "namespace": "##any",
                },
            )
            name: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                    "required": True,
                },
            )
            filename: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                    "required": True,
                },
            )

    @dataclass
    class Frame:
        """
        A frame of reference to which a pose is relative.

        Parameters
        ----------
        pose: A position(x,y,z) and orientation(roll, pitch yaw) with
            respect to the frame named in the relative_to attribute.
        name: Name of the frame. This name must not match another frame
            defined inside the parent that this frame is attached to.
        attached_to: Name of the link or frame to which this frame is
            attached.       If a frame is specified, recursively
            following the attached_to attributes       of the specified
            frames must lead to the name of a link, a model, or the
            world frame.
        """

        pose: Optional["World.Frame.Pose"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        name: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
            },
        )
        attached_to: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

        @dataclass
        class Pose:
            """
            Parameters
            ----------
            value:
            relative_to: Name of frame relative to which the pose is
                applied.
            """

            value: str = field(
                default="0 0 0 0 0 0",
                metadata={
                    "required": True,
                    "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){5}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
                },
            )
            relative_to: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                },
            )

    @dataclass
    class Plugin:
        """A plugin is a dynamically loaded chunk of code.

        It can exist as a child of world, model, and sensor.

        Parameters
        ----------
        any_element: This is a special element that should not be
            specified in an SDFormat file. It automatically copies child
            elements into the SDFormat element so that a plugin can
            access the data.
        name: A unique name for the plugin, scoped to its parent.
        filename: Name of the shared library to load. If the filename is
            not a full path name, the file will be searched for in the
            configuration paths.
        """

        any_element: List[object] = field(
            default_factory=list,
            metadata={
                "type": "Wildcard",
                "namespace": "##any",
            },
        )
        name: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
            },
        )
        filename: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
            },
        )

    @dataclass
    class Road:
        """
        Parameters
        ----------
        width: Width of the road
        point: A series of points that define the path of the road.
        material: The material of the visual element.
        name: Name of the road
        """

        width: float = field(
            default=1.0,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        point: List[str] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
                "min_occurs": 1,
                "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
            },
        )
        material: Optional[Material] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        name: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
            },
        )

    @dataclass
    class SphericalCoordinates:
        """
        Parameters
        ----------
        surface_model: Name of planetary surface model, used to
            determine the surface altitude       at a given latitude and
            longitude. The default is an ellipsoid model of       the
            earth based on the WGS-84 standard. It is used in Gazebo's
            GPS sensor       implementation.
        world_frame_orientation: This field identifies how Gazebo world
            frame is aligned in Geographical       sense.  The final
            Gazebo world frame orientation is obtained by rotating
            a frame aligned with following notation by the field
            heading_deg (Note       that heading_deg corresponds to
            positive yaw rotation in the NED frame,       so it's
            inverse specifies positive Z-rotation in ENU or NWU).
            Options are:         - ENU (East-North-Up)         - NED
            (North-East-Down)         - NWU (North-West-Up)       For
            example, world frame specified by setting
            world_orientation="ENU"       and heading_deg=-90° is
            effectively equivalent to NWU with heading of 0°.
        latitude_deg: Geodetic latitude at origin of gazebo reference
            frame, specified       in units of degrees.
        longitude_deg: Longitude at origin of gazebo reference frame,
            specified in units       of degrees.
        elevation: Elevation of origin of gazebo reference frame,
            specified in meters.
        heading_deg: Heading offset of gazebo reference frame, measured
            as angle between       Gazebo world frame and the
            world_frame_orientation type (ENU/NED/NWU).       Rotations
            about the downward-vector (e.g. North to East) are positive.
            The direction of rotation is chosen to be consistent with
            compass       heading convention (e.g. 0 degrees points
            North and 90 degrees       points East, positive rotation
            indicates counterclockwise rotation       when viewed from
            top-down direction).       The angle is specified in
            degrees.
        """

        surface_model: str = field(
            default="EARTH_WGS84",
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        world_frame_orientation: str = field(
            default="ENU",
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        latitude_deg: float = field(
            default=0.0,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        longitude_deg: float = field(
            default=0.0,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        elevation: float = field(
            default=0.0,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        heading_deg: float = field(
            default=0.0,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )

    @dataclass
    class Population:
        """
        The population element defines how and where a set of models will
        be automatically populated in Gazebo.

        Parameters
        ----------
        model_count: The number of models to place.
        distribution: Specifies the type of object distribution and its
            optional parameters.
        box: Box shape
        cylinder: Cylinder shape
        pose: A position(x,y,z) and orientation(roll, pitch yaw) with
            respect to the frame named in the relative_to attribute.
        model: The model element defines a complete robot or any other
            physical object.
        name: A unique name for the population. This name must not match
            another population in the world.
        """

        model_count: int = field(
            default=1,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        distribution: Optional["World.Population.Distribution"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        box: Optional["World.Population.Box"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        cylinder: Optional["World.Population.Cylinder"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        pose: Optional["World.Population.Pose"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        model: Optional[Model] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        name: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
            },
        )

        @dataclass
        class Distribution:
            """
            Specifies the type of object distribution and its optional
            parameters.

            Parameters
            ----------
            type: Define how the objects will be placed in the specified
                region.         - random: Models placed at random.
                - uniform: Models approximately placed in a 2D grid
                pattern with control             over the number of
                objects.         - grid: Models evenly placed in a 2D
                grid pattern. The number of objects             is not
                explicitly specified, it is based on the number of rows
                and             columns of the grid.         - linear-x:
                Models evently placed in a row along the global x-axis.
                - linear-y: Models evently placed in a row along the
                global y-axis.         - linear-z: Models evently placed
                in a row along the global z-axis.
            rows: Number of rows in the grid.
            cols: Number of columns in the grid.
            step: Distance between elements of the grid.
            """

            type: str = field(
                default="random",
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            rows: int = field(
                default=1,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            cols: int = field(
                default=1,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            step: str = field(
                default="0.5 0.5 0",
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                    "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
                },
            )

        @dataclass
        class Box:
            """
            Box shape.

            Parameters
            ----------
            size: The three side lengths of the box. The origin of the
                box is in its geometric center (inside the center of the
                box).
            """

            size: str = field(
                default="1 1 1",
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                    "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
                },
            )

        @dataclass
        class Cylinder:
            """
            Cylinder shape.

            Parameters
            ----------
            radius: Radius of the cylinder
            length: Length of the cylinder along the z axis
            """

            radius: float = field(
                default=1.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            length: float = field(
                default=1.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )

        @dataclass
        class Pose:
            """
            Parameters
            ----------
            value:
            relative_to: Name of frame relative to which the pose is
                applied.
            """

            value: str = field(
                default="0 0 0 0 0 0",
                metadata={
                    "required": True,
                    "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){5}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
                },
            )
            relative_to: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                },
            )
