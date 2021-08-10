from dataclasses import dataclass, field
from typing import List, Optional

__NAMESPACE__ = "sdformat/v1.2/sensor.xsd"


@dataclass
class Sensor:
    """
    The sensor tag describes the type and properties of a sensor.

    Parameters
    ----------
    always_on: If true the sensor will always be updated according to
        the update rate.
    update_rate: The frequency at which the sensor data is generated. If
        left unspecified, the sensor will generate data every cycle.
    visualize: If true, the sensor is visualized in the GUI
    pose: This is the pose of the sensor, relative to the parent link
        reference frame.
    topic: Name of the topic on which data is published. This is
        necessary for visualization
    plugin: A plugin is a dynamically loaded chunk of code. It can exist
        as a child of world, model, and sensor.
    camera: These elements are specific to camera sensors.
    ray: These elements are specific to the ray (laser) sensor.
    contact: These elements are specific to the contact sensor.
    rfidtag:
    rfid:
    name: A unique name for the sensor. This name must not match another
        model in the model.
    type: The type name of the sensor. By default, gazebo supports types
        camera, depth, stereocamera, contact, imu, ir and ray.
    """

    class Meta:
        name = "sensor"

    always_on: bool = field(
        default=False,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    update_rate: float = field(
        default=0.0,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    visualize: bool = field(
        default=False,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    pose: str = field(
        default="0 0 0 0 0 0",
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
            "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){5}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
        },
    )
    topic: str = field(
        default="__default",
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    plugin: List["Sensor.Plugin"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    camera: Optional["Sensor.Camera"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    ray: Optional["Sensor.Ray"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    contact: Optional["Sensor.Contact"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    rfidtag: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    rfid: Optional[str] = field(
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
    type: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
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
    class Camera:
        """
        These elements are specific to camera sensors.

        Parameters
        ----------
        horizontal_fov: Horizontal field of view
        image: The image size in pixels and format.
        clip: The near and far clip planes. Objects closer or farther
            than these planes are not rendered.
        save: Enable or disable saving of camera frames.
        depth_camera: Depth camera parameters
        """

        horizontal_fov: float = field(
            default=1.047,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        image: Optional["Sensor.Camera.Image"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        clip: Optional["Sensor.Camera.Clip"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        save: Optional["Sensor.Camera.Save"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        depth_camera: Optional["Sensor.Camera.DepthCamera"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

        @dataclass
        class Image:
            """
            The image size in pixels and format.

            Parameters
            ----------
            width: Width in pixels
            height: Height in pixels
            format:
                (L8|R8G8B8|B8G8R8|BAYER_RGGB8|BAYER_BGGR8|BAYER_GBRG8|BAYER_GRBG8)
            """

            width: int = field(
                default=320,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            height: int = field(
                default=240,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            format: str = field(
                default="R8G8B8",
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )

        @dataclass
        class Clip:
            """The near and far clip planes.

            Objects closer or farther than these planes are not
            rendered.

            Parameters
            ----------
            near: Near clipping plane
            far: Far clipping plane
            """

            near: float = field(
                default=0.1,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            far: float = field(
                default=100.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )

        @dataclass
        class Save:
            """
            Enable or disable saving of camera frames.

            Parameters
            ----------
            path: The path name which will hold the frame data. If path
                name is relative, then directory is relative to current
                working directory.
            enabled: True = saving enabled
            """

            path: str = field(
                default="__default__",
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            enabled: Optional[bool] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                    "required": True,
                },
            )

        @dataclass
        class DepthCamera:
            """
            Depth camera parameters.

            Parameters
            ----------
            output: Type of output
            """

            output: str = field(
                default="depths",
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )

    @dataclass
    class Ray:
        """
        These elements are specific to the ray (laser) sensor.

        Parameters
        ----------
        scan:
        range: specifies range properties of each simulated ray
        """

        scan: Optional["Sensor.Ray.Scan"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        range: Optional["Sensor.Ray.Range"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )

        @dataclass
        class Scan:
            horizontal: Optional["Sensor.Ray.Scan.Horizontal"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            vertical: Optional["Sensor.Ray.Scan.Vertical"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Horizontal:
                """
                Parameters
                ----------
                samples: The number of simulated rays to generate per
                    complete laser sweep cycle.
                resolution: This number is multiplied by samples to
                    determine the number of range data points returned.
                    If resolution is less than one, range data is
                    interpolated. If resolution is greater than one,
                    range data is averaged.
                min_angle:
                max_angle: Must be greater or equal to min_angle
                """

                samples: int = field(
                    default=640,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                resolution: float = field(
                    default=1.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                min_angle: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                max_angle: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )

            @dataclass
            class Vertical:
                """
                Parameters
                ----------
                samples: The number of simulated rays to generate per
                    complete laser sweep cycle.
                resolution: This number is multiplied by samples to
                    determine the number of range data points returned.
                    If resolution is less than one, range data is
                    interpolated. If resolution is greater than one,
                    range data is averaged.
                min_angle:
                max_angle: Must be greater or equal to min_angle
                """

                samples: int = field(
                    default=1,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                resolution: float = field(
                    default=1.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                min_angle: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                max_angle: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )

        @dataclass
        class Range:
            """
            specifies range properties of each simulated ray.

            Parameters
            ----------
            min: The minimum distance for each ray.
            max: The maximum distance for each ray.
            resolution: Linear resolution of each ray.
            """

            min: float = field(
                default=0.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            max: float = field(
                default=0.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            resolution: float = field(
                default=0.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )

    @dataclass
    class Contact:
        """
        These elements are specific to the contact sensor.

        Parameters
        ----------
        collision: name of the collision element within a link that acts
            as the contact sensor.
        topic: Topic on which contact data is published.
        """

        collision: str = field(
            default="__default__",
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        topic: str = field(
            default="__default_topic__",
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
