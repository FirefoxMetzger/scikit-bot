from dataclasses import dataclass, field
from typing import List, Optional

__NAMESPACE__ = "sdformat/v1.4/sensor.xsd"


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
    contact: These elements are specific to the contact sensor.
    force_torque: These elements are specific to the force torque
        sensor.
    gps: These elements are specific to the GPS sensor.
    imu: These elements are specific to the IMU sensor.
    ray: These elements are specific to the ray (laser) sensor.
    rfidtag:
    rfid:
    sonar: These elements are specific to the sonar sensor.
    transceiver: These elements are specific to a wireless transceiver.
    name: A unique name for the sensor. This name must not match another
        model in the model.
    type: The type name of the sensor. By default, SDFormat supports
        types camera, depth, multicamera, contact, gps, imu, ir and ray.
    """

    class Meta:
        name = "sensor"

    always_on: bool = field(
        default=False,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    update_rate: float = field(
        default=0.0,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    visualize: bool = field(
        default=False,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    pose: str = field(
        default="0 0 0 0 0 0",
        metadata={
            "type": "Element",
            "namespace": "",
            "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){5}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
        },
    )
    topic: str = field(
        default="__default__",
        metadata={
            "type": "Element",
            "namespace": "",
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
    contact: Optional["Sensor.Contact"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    force_torque: Optional["Sensor.ForceTorque"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    gps: Optional["Sensor.Gps"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    imu: Optional["Sensor.Imu"] = field(
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
    sonar: Optional["Sensor.Sonar"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    transceiver: Optional["Sensor.Transceiver"] = field(
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
        pose: A position and orientation in the parent coordinate frame
            for the camera.
        horizontal_fov: Horizontal field of view
        image: The image size in pixels and format.
        clip: The near and far clip planes. Objects closer or farther
            than these planes are not rendered.
        save: Enable or disable saving of camera frames.
        depth_camera: Depth camera parameters
        noise: The properties of the noise model that should be applied
            to generated images
        name: An optional name for the camera.
        """

        pose: str = field(
            default="0 0 0 0 0 0",
            metadata={
                "type": "Element",
                "namespace": "",
                "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){5}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
            },
        )
        horizontal_fov: float = field(
            default=1.047,
            metadata={
                "type": "Element",
                "namespace": "",
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
        noise: Optional["Sensor.Camera.Noise"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        name: str = field(
            default="__default__",
            metadata={
                "type": "Attribute",
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
                },
            )
            height: int = field(
                default=240,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            format: str = field(
                default="R8G8B8",
                metadata={
                    "type": "Element",
                    "namespace": "",
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
                },
            )
            far: float = field(
                default=100.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
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
                },
            )

        @dataclass
        class Noise:
            """
            The properties of the noise model that should be applied to
            generated images.

            Parameters
            ----------
            type: The type of noise.  Currently supported types are:
                "gaussian" (draw additive noise values independently for
                each pixel from a Gaussian distribution).
            mean: For type "gaussian," the mean of the Gaussian
                distribution from which noise values are drawn.
            stddev: For type "gaussian," the standard deviation of the
                Gaussian distribution from which noise values are drawn.
            """

            type: str = field(
                default="gaussian",
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            mean: float = field(
                default=0.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            stddev: float = field(
                default=0.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
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
            },
        )
        topic: str = field(
            default="__default_topic__",
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

    @dataclass
    class ForceTorque:
        """
        These elements are specific to the force torque sensor.

        Parameters
        ----------
        frame: Frame in which to report the wrench values.
        """

        frame: str = field(
            default="parent",
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

    @dataclass
    class Gps:
        """
        These elements are specific to the GPS sensor.

        Parameters
        ----------
        position_sensing: Parameters related to GPS position
            measurement.
        velocity_sensing: Parameters related to GPS position
            measurement.
        """

        position_sensing: Optional["Sensor.Gps.PositionSensing"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        velocity_sensing: Optional["Sensor.Gps.VelocitySensing"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

        @dataclass
        class PositionSensing:
            """
            Parameters related to GPS position measurement.

            Parameters
            ----------
            horizontal: Noise parameters for horizontal position
                measurement, in units of meters.
            vertical: Noise parameters for vertical position
                measurement, in units of meters.
            """

            horizontal: Optional["Sensor.Gps.PositionSensing.Horizontal"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            vertical: Optional["Sensor.Gps.PositionSensing.Vertical"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Horizontal:
                """
                Noise parameters for horizontal position measurement, in units
                of meters.

                Parameters
                ----------
                noise: The properties of a sensor noise model.
                """

                noise: Optional["Sensor.Gps.PositionSensing.Horizontal.Noise"] = field(
                    default=None,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )

                @dataclass
                class Noise:
                    """
                    The properties of a sensor noise model.

                    Parameters
                    ----------
                    mean: For type "gaussian*", the mean of the Gaussian
                        distribution from which noise values are drawn.
                    stddev: For type "gaussian*", the standard deviation
                        of the Gaussian distribution from which noise
                        values are drawn.
                    bias_mean: For type "gaussian*", the mean of the
                        Gaussian distribution from which bias values are
                        drawn.
                    bias_stddev: For type "gaussian*", the standard
                        deviation of the Gaussian distribution from
                        which bias values are drawn.
                    precision: For type "gaussian_quantized", the
                        precision of output signals. A value       of
                        zero implies infinite precision / no
                        quantization.
                    type: The type of noise. Currently supported types
                        are:       "none" (no noise).       "gaussian"
                        (draw noise values independently for each
                        measurement from a Gaussian distribution).
                        "gaussian_quantized" ("gaussian" plus
                        quantization of outputs (ie. rounding))
                    """

                    mean: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                        },
                    )
                    stddev: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                        },
                    )
                    bias_mean: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                        },
                    )
                    bias_stddev: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                        },
                    )
                    precision: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
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
            class Vertical:
                """
                Noise parameters for vertical position measurement, in units of
                meters.

                Parameters
                ----------
                noise: The properties of a sensor noise model.
                """

                noise: Optional["Sensor.Gps.PositionSensing.Vertical.Noise"] = field(
                    default=None,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )

                @dataclass
                class Noise:
                    """
                    The properties of a sensor noise model.

                    Parameters
                    ----------
                    mean: For type "gaussian*", the mean of the Gaussian
                        distribution from which noise values are drawn.
                    stddev: For type "gaussian*", the standard deviation
                        of the Gaussian distribution from which noise
                        values are drawn.
                    bias_mean: For type "gaussian*", the mean of the
                        Gaussian distribution from which bias values are
                        drawn.
                    bias_stddev: For type "gaussian*", the standard
                        deviation of the Gaussian distribution from
                        which bias values are drawn.
                    precision: For type "gaussian_quantized", the
                        precision of output signals. A value       of
                        zero implies infinite precision / no
                        quantization.
                    type: The type of noise. Currently supported types
                        are:       "none" (no noise).       "gaussian"
                        (draw noise values independently for each
                        measurement from a Gaussian distribution).
                        "gaussian_quantized" ("gaussian" plus
                        quantization of outputs (ie. rounding))
                    """

                    mean: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                        },
                    )
                    stddev: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                        },
                    )
                    bias_mean: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                        },
                    )
                    bias_stddev: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                        },
                    )
                    precision: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
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
        class VelocitySensing:
            """
            Parameters related to GPS position measurement.

            Parameters
            ----------
            horizontal: Noise parameters for horizontal velocity
                measurement, in units of meters/second.
            vertical: Noise parameters for vertical velocity
                measurement, in units of meters/second.
            """

            horizontal: Optional["Sensor.Gps.VelocitySensing.Horizontal"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            vertical: Optional["Sensor.Gps.VelocitySensing.Vertical"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Horizontal:
                """
                Noise parameters for horizontal velocity measurement, in units
                of meters/second.

                Parameters
                ----------
                noise: The properties of a sensor noise model.
                """

                noise: Optional["Sensor.Gps.VelocitySensing.Horizontal.Noise"] = field(
                    default=None,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )

                @dataclass
                class Noise:
                    """
                    The properties of a sensor noise model.

                    Parameters
                    ----------
                    mean: For type "gaussian*", the mean of the Gaussian
                        distribution from which noise values are drawn.
                    stddev: For type "gaussian*", the standard deviation
                        of the Gaussian distribution from which noise
                        values are drawn.
                    bias_mean: For type "gaussian*", the mean of the
                        Gaussian distribution from which bias values are
                        drawn.
                    bias_stddev: For type "gaussian*", the standard
                        deviation of the Gaussian distribution from
                        which bias values are drawn.
                    precision: For type "gaussian_quantized", the
                        precision of output signals. A value       of
                        zero implies infinite precision / no
                        quantization.
                    type: The type of noise. Currently supported types
                        are:       "none" (no noise).       "gaussian"
                        (draw noise values independently for each
                        measurement from a Gaussian distribution).
                        "gaussian_quantized" ("gaussian" plus
                        quantization of outputs (ie. rounding))
                    """

                    mean: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                        },
                    )
                    stddev: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                        },
                    )
                    bias_mean: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                        },
                    )
                    bias_stddev: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                        },
                    )
                    precision: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
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
            class Vertical:
                """
                Noise parameters for vertical velocity measurement, in units of
                meters/second.

                Parameters
                ----------
                noise: The properties of a sensor noise model.
                """

                noise: Optional["Sensor.Gps.VelocitySensing.Vertical.Noise"] = field(
                    default=None,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )

                @dataclass
                class Noise:
                    """
                    The properties of a sensor noise model.

                    Parameters
                    ----------
                    mean: For type "gaussian*", the mean of the Gaussian
                        distribution from which noise values are drawn.
                    stddev: For type "gaussian*", the standard deviation
                        of the Gaussian distribution from which noise
                        values are drawn.
                    bias_mean: For type "gaussian*", the mean of the
                        Gaussian distribution from which bias values are
                        drawn.
                    bias_stddev: For type "gaussian*", the standard
                        deviation of the Gaussian distribution from
                        which bias values are drawn.
                    precision: For type "gaussian_quantized", the
                        precision of output signals. A value       of
                        zero implies infinite precision / no
                        quantization.
                    type: The type of noise. Currently supported types
                        are:       "none" (no noise).       "gaussian"
                        (draw noise values independently for each
                        measurement from a Gaussian distribution).
                        "gaussian_quantized" ("gaussian" plus
                        quantization of outputs (ie. rounding))
                    """

                    mean: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                        },
                    )
                    stddev: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                        },
                    )
                    bias_mean: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                        },
                    )
                    bias_stddev: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                        },
                    )
                    precision: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
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
    class Imu:
        """
        These elements are specific to the IMU sensor.

        Parameters
        ----------
        topic: Topic on which data is published.
        noise: The properties of the noise model that should be applied
            to generated data
        """

        topic: str = field(
            default="__default_topic__",
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        noise: Optional["Sensor.Imu.Noise"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

        @dataclass
        class Noise:
            """
            The properties of the noise model that should be applied to
            generated data.

            Parameters
            ----------
            type: The type of noise.  Currently supported types are:
                "gaussian" (draw noise values independently for each
                beam from a Gaussian distribution).
            rate: Noise parameters for angular rates.
            accel: Noise parameters for linear accelerations.
            """

            type: str = field(
                default="gaussian",
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            rate: Optional["Sensor.Imu.Noise.Rate"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            accel: Optional["Sensor.Imu.Noise.Accel"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )

            @dataclass
            class Rate:
                """
                Noise parameters for angular rates.

                Parameters
                ----------
                mean: For type "gaussian," the mean of the Gaussian
                    distribution from which noise values are drawn.
                stddev: For type "gaussian," the standard deviation of
                    the Gaussian distribution from which noise values
                    are drawn.
                bias_mean: For type "gaussian," the mean of the Gaussian
                    distribution from which bias values are drawn.
                bias_stddev: For type "gaussian," the standard deviation
                    of the Gaussian distribution from which bias values
                    are drawn.
                """

                mean: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    },
                )
                stddev: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    },
                )
                bias_mean: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    },
                )
                bias_stddev: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    },
                )

            @dataclass
            class Accel:
                """
                Noise parameters for linear accelerations.

                Parameters
                ----------
                mean: For type "gaussian," the mean of the Gaussian
                    distribution from which noise values are drawn.
                stddev: For type "gaussian," the standard deviation of
                    the Gaussian distribution from which noise values
                    are drawn.
                bias_mean: For type "gaussian," the mean of the Gaussian
                    distribution from which bias values are drawn.
                bias_stddev: For type "gaussian," the standard deviation
                    of the Gaussian distribution from which bias values
                    are drawn.
                """

                mean: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    },
                )
                stddev: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    },
                )
                bias_mean: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    },
                )
                bias_stddev: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
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
        noise: The properties of the noise model that should be applied
            to generated scans
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
        noise: Optional["Sensor.Ray.Noise"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
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
                    },
                )
                resolution: float = field(
                    default=1.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    },
                )
                min_angle: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    },
                )
                max_angle: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
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
                    },
                )
                resolution: float = field(
                    default=1.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    },
                )
                min_angle: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    },
                )
                max_angle: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
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
                },
            )
            max: float = field(
                default=0.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            resolution: float = field(
                default=0.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

        @dataclass
        class Noise:
            """
            The properties of the noise model that should be applied to
            generated scans.

            Parameters
            ----------
            type: The type of noise.  Currently supported types are:
                "gaussian" (draw noise values independently for each
                beam from a Gaussian distribution).
            mean: For type "gaussian," the mean of the Gaussian
                distribution from which noise values are drawn.
            stddev: For type "gaussian," the standard deviation of the
                Gaussian distribution from which noise values are drawn.
            """

            type: str = field(
                default="gaussian",
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            mean: float = field(
                default=0.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            stddev: float = field(
                default=0.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

    @dataclass
    class Sonar:
        """
        These elements are specific to the sonar sensor.

        Parameters
        ----------
        min: Minimum range
        max: Max range
        radius: Radius of the sonar cone at max range.
        """

        min: float = field(
            default=0.0,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        max: float = field(
            default=1.0,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        radius: float = field(
            default=0.5,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

    @dataclass
    class Transceiver:
        """
        These elements are specific to a wireless transceiver.

        Parameters
        ----------
        essid: Service set identifier (network name)
        frequency: Specifies the frequency of transmission in MHz
        min_frequency: Only a frequency range is filtered. Here we set
            the lower bound (MHz).
        max_frequency: Only a frequency range is filtered. Here we set
            the upper bound (MHz).
        gain: Specifies the antenna gain in dBi
        power: Specifies the transmission power in dBm
        sensitivity: Mininum received signal power in dBm
        """

        essid: str = field(
            default="wireless",
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        frequency: float = field(
            default=2442.0,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        min_frequency: float = field(
            default=2412.0,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        max_frequency: float = field(
            default=2484.0,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        gain: float = field(
            default=2.5,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        power: float = field(
            default=14.5,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        sensitivity: float = field(
            default=-90.0,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
