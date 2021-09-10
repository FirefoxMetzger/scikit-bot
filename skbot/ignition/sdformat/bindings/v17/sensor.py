from dataclasses import dataclass, field
from typing import List, Optional

__NAMESPACE__ = "sdformat/v1.7/sensor.xsd"


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
    topic: Name of the topic on which data is published. This is
        necessary for visualization
    enable_metrics: If true, the sensor will publish performance metrics
    pose: A position(x,y,z) and orientation(roll, pitch yaw) with
        respect to the frame named in the relative_to attribute.
    plugin: A plugin is a dynamically loaded chunk of code. It can exist
        as a child of world, model, and sensor.
    air_pressure: These elements are specific to an air pressure sensor.
    altimeter: These elements are specific to an altimeter sensor.
    camera: These elements are specific to camera sensors.
    contact: These elements are specific to the contact sensor.
    force_torque: These elements are specific to the force torque
        sensor.
    gps: These elements are specific to the GPS sensor.
    imu: These elements are specific to the IMU sensor.
    lidar: These elements are specific to the lidar sensor.
    logical_camera: These elements are specific to logical camera
        sensors. A logical camera reports objects that fall within a
        frustum. Computation should be performed on the CPU.
    magnetometer: These elements are specific to a Magnetometer sensor.
    navsat: These elements are specific to the NAVSAT sensor.
    ray: These elements are specific to the ray (laser) sensor.
    rfidtag:
    rfid:
    sonar: These elements are specific to the sonar sensor.
    transceiver: These elements are specific to a wireless transceiver.
    name: A unique name for the sensor. This name must not match another
        model in the model.
    type: The type name of the sensor. By default, SDFormat supports
        types                   air_pressure,
        altimeter,                   camera,                   contact,
        depth_camera, depth,                   force_torque,
        gps,                   gpu_lidar,                   gpu_ray,
        imu,                   lidar,                   logical_camera,
        magnetometer,                   multicamera,
        navsat,                   ray,                   rfid,
        rfidtag,                   rgbd_camera, rgbd,
        sonar,                   thermal_camera, thermal,
        wireless_receiver, and                   wireless_transmitter.
        The "ray", "gpu_ray", and "gps" types are equivalent to "lidar",
        "gpu_lidar", and "navsat", respectively. It is preferred to use
        "lidar", "gpu_lidar", and "navsat" since "ray", "gpu_ray", and
        "gps" will be deprecated. The "ray", "gpu_ray", and "gps" types
        are maintained for legacy support.
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
    topic: str = field(
        default="__default__",
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    enable_metrics: bool = field(
        default=False,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    pose: Optional["Sensor.Pose"] = field(
        default=None,
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
    air_pressure: Optional["Sensor.AirPressure"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    altimeter: Optional["Sensor.Altimeter"] = field(
        default=None,
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
    lidar: Optional["Sensor.Lidar"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    logical_camera: Optional["Sensor.LogicalCamera"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    magnetometer: Optional["Sensor.Magnetometer"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    navsat: Optional["Sensor.Navsat"] = field(
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
    class AirPressure:
        """
        These elements are specific to an air pressure sensor.

        Parameters
        ----------
        reference_altitude: The initial altitude in meters. This value
            can be used by a sensor implementation to augment the
            altitude of the sensor. For example, if you are using
            simulation instead of creating a 1000 m mountain model on
            which to place your sensor, you could instead set this value
            to 1000 and place your model on a ground plane with a Z
            height of zero.
        pressure: Noise parameters for the pressure data.
        """

        reference_altitude: float = field(
            default=0.0,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        pressure: Optional["Sensor.AirPressure.Pressure"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

        @dataclass
        class Pressure:
            """
            Noise parameters for the pressure data.

            Parameters
            ----------
            noise: The properties of a sensor noise model.
            """

            noise: Optional["Sensor.AirPressure.Pressure.Noise"] = field(
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
                    distribution from which       noise values are
                    drawn.
                stddev: For type "gaussian*", the standard deviation of
                    the Gaussian distribution from which noise values
                    are drawn.
                bias_mean: For type "gaussian*", the mean of the
                    Gaussian distribution from which bias values are
                    drawn.
                bias_stddev: For type "gaussian*", the standard
                    deviation of the Gaussian distribution from which
                    bias values are drawn.
                dynamic_bias_stddev: For type "gaussian*", the standard
                    deviation of the noise used to drive a process to
                    model slow variations in a sensor bias.
                dynamic_bias_correlation_time: For type "gaussian*", the
                    correlation time in seconds of the noise used to
                    drive a process to model slow variations in a sensor
                    bias. A typical value, when used, would be on the
                    order of 3600 seconds (1 hour).
                precision: For type "gaussian_quantized", the precision
                    of output signals. A value       of zero implies
                    infinite precision / no quantization.
                type: The type of noise. Currently supported types are:
                    "none" (no noise).       "gaussian" (draw noise
                    values independently for each measurement from a
                    Gaussian distribution).       "gaussian_quantized"
                    ("gaussian" plus quantization of outputs (ie.
                    rounding))
                """

                mean: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                stddev: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                bias_mean: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                bias_stddev: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                dynamic_bias_stddev: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                dynamic_bias_correlation_time: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                precision: float = field(
                    default=0.0,
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
    class Altimeter:
        """
        These elements are specific to an altimeter sensor.

        Parameters
        ----------
        vertical_position: Noise parameters for vertical position
        vertical_velocity: Noise parameters for vertical velocity
        """

        vertical_position: Optional["Sensor.Altimeter.VerticalPosition"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        vertical_velocity: Optional["Sensor.Altimeter.VerticalVelocity"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

        @dataclass
        class VerticalPosition:
            """
            Noise parameters for vertical position.

            Parameters
            ----------
            noise: The properties of a sensor noise model.
            """

            noise: Optional["Sensor.Altimeter.VerticalPosition.Noise"] = field(
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
                    distribution from which       noise values are
                    drawn.
                stddev: For type "gaussian*", the standard deviation of
                    the Gaussian distribution from which noise values
                    are drawn.
                bias_mean: For type "gaussian*", the mean of the
                    Gaussian distribution from which bias values are
                    drawn.
                bias_stddev: For type "gaussian*", the standard
                    deviation of the Gaussian distribution from which
                    bias values are drawn.
                dynamic_bias_stddev: For type "gaussian*", the standard
                    deviation of the noise used to drive a process to
                    model slow variations in a sensor bias.
                dynamic_bias_correlation_time: For type "gaussian*", the
                    correlation time in seconds of the noise used to
                    drive a process to model slow variations in a sensor
                    bias. A typical value, when used, would be on the
                    order of 3600 seconds (1 hour).
                precision: For type "gaussian_quantized", the precision
                    of output signals. A value       of zero implies
                    infinite precision / no quantization.
                type: The type of noise. Currently supported types are:
                    "none" (no noise).       "gaussian" (draw noise
                    values independently for each measurement from a
                    Gaussian distribution).       "gaussian_quantized"
                    ("gaussian" plus quantization of outputs (ie.
                    rounding))
                """

                mean: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                stddev: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                bias_mean: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                bias_stddev: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                dynamic_bias_stddev: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                dynamic_bias_correlation_time: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                precision: float = field(
                    default=0.0,
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
        class VerticalVelocity:
            """
            Noise parameters for vertical velocity.

            Parameters
            ----------
            noise: The properties of a sensor noise model.
            """

            noise: Optional["Sensor.Altimeter.VerticalVelocity.Noise"] = field(
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
                    distribution from which       noise values are
                    drawn.
                stddev: For type "gaussian*", the standard deviation of
                    the Gaussian distribution from which noise values
                    are drawn.
                bias_mean: For type "gaussian*", the mean of the
                    Gaussian distribution from which bias values are
                    drawn.
                bias_stddev: For type "gaussian*", the standard
                    deviation of the Gaussian distribution from which
                    bias values are drawn.
                dynamic_bias_stddev: For type "gaussian*", the standard
                    deviation of the noise used to drive a process to
                    model slow variations in a sensor bias.
                dynamic_bias_correlation_time: For type "gaussian*", the
                    correlation time in seconds of the noise used to
                    drive a process to model slow variations in a sensor
                    bias. A typical value, when used, would be on the
                    order of 3600 seconds (1 hour).
                precision: For type "gaussian_quantized", the precision
                    of output signals. A value       of zero implies
                    infinite precision / no quantization.
                type: The type of noise. Currently supported types are:
                    "none" (no noise).       "gaussian" (draw noise
                    values independently for each measurement from a
                    Gaussian distribution).       "gaussian_quantized"
                    ("gaussian" plus quantization of outputs (ie.
                    rounding))
                """

                mean: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                stddev: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                bias_mean: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                bias_stddev: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                dynamic_bias_stddev: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                dynamic_bias_correlation_time: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                precision: float = field(
                    default=0.0,
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
        noise: The properties of the noise model that should be applied
            to generated images
        distortion: Lens distortion to be applied to camera images. See
            http://en.wikipedia.org/wiki/Distortion_(optics)#Software_correction
        lens: Lens projection description
        visibility_mask: Visibility mask of a camera. When (camera's
            visibility_mask &amp; visual's visibility_flags) evaluates
            to non-zero, the visual will be visible to the camera.
        pose: A position(x,y,z) and orientation(roll, pitch yaw) with
            respect to the frame named in the relative_to attribute.
        name: An optional name for the camera.
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
        noise: Optional["Sensor.Camera.Noise"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        distortion: Optional["Sensor.Camera.Distortion"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        lens: Optional["Sensor.Camera.Lens"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        visibility_mask: int = field(
            default=4294967295,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        pose: Optional["Sensor.Camera.Pose"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
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
                (L8|L16|R_FLOAT16|R_FLOAT32|R8G8B8|B8G8R8|BAYER_RGGB8|BAYER_BGGR8|BAYER_GBRG8|BAYER_GRBG8)
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
            clip: The near and far clip planes. Objects closer or
                farther than these planes are not detected by the depth
                camera.
            """

            output: str = field(
                default="depths",
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            clip: Optional["Sensor.Camera.DepthCamera.Clip"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Clip:
                """The near and far clip planes.

                Objects closer or farther than these planes are not
                detected by the depth camera.

                Parameters
                ----------
                near: Near clipping plane for depth camera
                far: Far clipping plane for depth camera
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
                    default=10.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
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
                    "required": True,
                },
            )
            mean: float = field(
                default=0.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            stddev: float = field(
                default=0.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )

        @dataclass
        class Distortion:
            """Lens distortion to be applied to camera images.

            See http://en.wikipedia.org/wiki/Distortion_(optics)#Software_correction

            Parameters
            ----------
            k1: The radial distortion coefficient k1
            k2: The radial distortion coefficient k2
            k3: The radial distortion coefficient k3
            p1: The tangential distortion coefficient p1
            p2: The tangential distortion coefficient p2
            center: The distortion center or principal point
            """

            k1: float = field(
                default=0.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            k2: float = field(
                default=0.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            k3: float = field(
                default=0.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            p1: float = field(
                default=0.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            p2: float = field(
                default=0.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            center: str = field(
                default="0.5 0.5",
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                    "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+)((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
                },
            )

        @dataclass
        class Lens:
            """
            Lens projection description.

            Parameters
            ----------
            type: Type of the lens mapping. Supported values are
                gnomonical, stereographic, equidistant, equisolid_angle,
                orthographic, custom. For gnomonical (perspective)
                projection, it is recommended to specify a
                horizontal_fov of less than or equal to 90°
            scale_to_hfov: If true the image will be scaled to fit
                horizontal FOV, otherwise it will be shown according to
                projection type parameters
            custom_function: Definition of custom mapping function in a
                form of r=c1*f*fun(theta/c2 + c3). See
                https://en.wikipedia.org/wiki/Fisheye_lens#Mapping_function
            cutoff_angle: Everything outside of the specified angle will
                be hidden, 90° by default
            env_texture_size: Resolution of the environment cube map
                used to draw the world
            intrinsics: Camera intrinsic parameters for setting a custom
                perspective projection matrix (cannot be used with
                WideAngleCamera since this class uses image stitching
                from 6 different cameras for achieving a wide field of
                view). The focal lengths can be computed using
                focal_length_in_pixels = (image_width_in_pixels * 0.5) /
                tan(field_of_view_in_degrees * 0.5 * PI/180)
            """

            type: str = field(
                default="stereographic",
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            scale_to_hfov: bool = field(
                default=True,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            custom_function: Optional["Sensor.Camera.Lens.CustomFunction"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            cutoff_angle: float = field(
                default=1.5707,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            env_texture_size: int = field(
                default=256,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            intrinsics: Optional["Sensor.Camera.Lens.Intrinsics"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class CustomFunction:
                """Definition of custom mapping function in a form of
                r=c1*f*fun(theta/c2 + c3).

                See https://en.wikipedia.org/wiki/Fisheye_lens#Mapping_function

                Parameters
                ----------
                c1: Linear scaling constant
                c2: Angle scaling constant
                c3: Angle offset constant
                f: Focal length of the optical system. Note: It's not a
                    focal length of the lens in a common sense! This
                    value is ignored if 'scale_to_fov' is set to true
                fun: Possible values are 'sin', 'tan' and 'id'
                """

                c1: float = field(
                    default=1.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                c2: float = field(
                    default=1.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                c3: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                f: float = field(
                    default=1.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                fun: str = field(
                    default="tan",
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )

            @dataclass
            class Intrinsics:
                """Camera intrinsic parameters for setting a custom perspective
                projection matrix (cannot be used with WideAngleCamera since
                this class uses image stitching from 6 different cameras for
                achieving a wide field of view).

                The focal lengths can be computed using focal_length_in_pixels = (image_width_in_pixels * 0.5) / tan(field_of_view_in_degrees * 0.5 * PI/180)

                Parameters
                ----------
                fx: X focal length (in pixels, overrides horizontal_fov)
                fy: Y focal length (in pixels, overrides horizontal_fov)
                cx: X principal point (in pixels)
                cy: Y principal point (in pixels)
                s: XY axis skew
                """

                fx: float = field(
                    default=277.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                fy: float = field(
                    default=277.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                cx: float = field(
                    default=160.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                cy: float = field(
                    default=120.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                s: float = field(
                    default=0.0,
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

    @dataclass
    class ForceTorque:
        """
        These elements are specific to the force torque sensor.

        Parameters
        ----------
        frame: Frame in which to report the wrench values. Currently
            supported frames are:         "parent" report the wrench
            expressed in the orientation of the parent link frame,
            "child" report the wrench expressed in the orientation of
            the child link frame,         "sensor" report the wrench
            expressed in the orientation of the joint sensor frame.
            Note that for each option the point with respect to which
            the       torque component of the wrench is expressed is the
            joint origin.
        measure_direction: Direction of the wrench measured by the
            sensor. The supported options are:         "parent_to_child"
            if the measured wrench is the one applied by the parent link
            on the child link,         "child_to_parent" if the measured
            wrench is the one applied by the child link on the parent
            link.
        """

        frame: str = field(
            default="child",
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        measure_direction: str = field(
            default="child_to_parent",
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
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
                        distribution from which       noise values are
                        drawn.
                    stddev: For type "gaussian*", the standard deviation
                        of the Gaussian distribution from which noise
                        values are drawn.
                    bias_mean: For type "gaussian*", the mean of the
                        Gaussian distribution from which bias values are
                        drawn.
                    bias_stddev: For type "gaussian*", the standard
                        deviation of the Gaussian distribution from
                        which bias values are drawn.
                    dynamic_bias_stddev: For type "gaussian*", the
                        standard deviation of the noise used to drive a
                        process to model slow variations in a sensor
                        bias.
                    dynamic_bias_correlation_time: For type "gaussian*",
                        the correlation time in seconds of the noise
                        used to drive a process to model slow variations
                        in a sensor bias. A typical value, when used,
                        would be on the order of 3600 seconds (1 hour).
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
                            "required": True,
                        },
                    )
                    stddev: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    bias_mean: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    bias_stddev: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    dynamic_bias_stddev: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    dynamic_bias_correlation_time: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    precision: float = field(
                        default=0.0,
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
                        distribution from which       noise values are
                        drawn.
                    stddev: For type "gaussian*", the standard deviation
                        of the Gaussian distribution from which noise
                        values are drawn.
                    bias_mean: For type "gaussian*", the mean of the
                        Gaussian distribution from which bias values are
                        drawn.
                    bias_stddev: For type "gaussian*", the standard
                        deviation of the Gaussian distribution from
                        which bias values are drawn.
                    dynamic_bias_stddev: For type "gaussian*", the
                        standard deviation of the noise used to drive a
                        process to model slow variations in a sensor
                        bias.
                    dynamic_bias_correlation_time: For type "gaussian*",
                        the correlation time in seconds of the noise
                        used to drive a process to model slow variations
                        in a sensor bias. A typical value, when used,
                        would be on the order of 3600 seconds (1 hour).
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
                            "required": True,
                        },
                    )
                    stddev: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    bias_mean: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    bias_stddev: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    dynamic_bias_stddev: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    dynamic_bias_correlation_time: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    precision: float = field(
                        default=0.0,
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
                        distribution from which       noise values are
                        drawn.
                    stddev: For type "gaussian*", the standard deviation
                        of the Gaussian distribution from which noise
                        values are drawn.
                    bias_mean: For type "gaussian*", the mean of the
                        Gaussian distribution from which bias values are
                        drawn.
                    bias_stddev: For type "gaussian*", the standard
                        deviation of the Gaussian distribution from
                        which bias values are drawn.
                    dynamic_bias_stddev: For type "gaussian*", the
                        standard deviation of the noise used to drive a
                        process to model slow variations in a sensor
                        bias.
                    dynamic_bias_correlation_time: For type "gaussian*",
                        the correlation time in seconds of the noise
                        used to drive a process to model slow variations
                        in a sensor bias. A typical value, when used,
                        would be on the order of 3600 seconds (1 hour).
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
                            "required": True,
                        },
                    )
                    stddev: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    bias_mean: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    bias_stddev: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    dynamic_bias_stddev: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    dynamic_bias_correlation_time: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    precision: float = field(
                        default=0.0,
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
                        distribution from which       noise values are
                        drawn.
                    stddev: For type "gaussian*", the standard deviation
                        of the Gaussian distribution from which noise
                        values are drawn.
                    bias_mean: For type "gaussian*", the mean of the
                        Gaussian distribution from which bias values are
                        drawn.
                    bias_stddev: For type "gaussian*", the standard
                        deviation of the Gaussian distribution from
                        which bias values are drawn.
                    dynamic_bias_stddev: For type "gaussian*", the
                        standard deviation of the noise used to drive a
                        process to model slow variations in a sensor
                        bias.
                    dynamic_bias_correlation_time: For type "gaussian*",
                        the correlation time in seconds of the noise
                        used to drive a process to model slow variations
                        in a sensor bias. A typical value, when used,
                        would be on the order of 3600 seconds (1 hour).
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
                            "required": True,
                        },
                    )
                    stddev: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    bias_mean: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    bias_stddev: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    dynamic_bias_stddev: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    dynamic_bias_correlation_time: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    precision: float = field(
                        default=0.0,
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
    class Imu:
        """
        These elements are specific to the IMU sensor.

        Parameters
        ----------
        orientation_reference_frame:
        angular_velocity: These elements are specific to body-frame
            angular velocity,     which is expressed in radians per
            second
        linear_acceleration: These elements are specific to body-frame
            linear acceleration,     which is expressed in meters per
            second squared
        enable_orientation: Some IMU sensors rely on external filters to
            produce orientation estimates. True to generate and output
            orientation data, false to disable orientation data
            generation.
        """

        orientation_reference_frame: Optional[
            "Sensor.Imu.OrientationReferenceFrame"
        ] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        angular_velocity: Optional["Sensor.Imu.AngularVelocity"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        linear_acceleration: Optional["Sensor.Imu.LinearAcceleration"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        enable_orientation: bool = field(
            default=True,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )

        @dataclass
        class OrientationReferenceFrame:
            """
            Parameters
            ----------
            localization: This string represents special hardcoded use
                cases that are commonly seen with typical robot IMU's:
                - CUSTOM: use Euler angle custom_rpy orientation
                specification.                  The orientation of the
                IMU's reference frame is defined by adding the
                custom_rpy rotation                  to the
                parent_frame.           - NED: The IMU XYZ aligns with
                NED, where NED orientation relative to Gazebo world
                is defined by the SphericalCoordinates class.
                - ENU: The IMU XYZ aligns with ENU, where ENU
                orientation relative to Gazebo world                  is
                defined by the SphericalCoordinates class.           -
                NWU: The IMU XYZ aligns with NWU, where NWU orientation
                relative to Gazebo world                  is defined by
                the SphericalCoordinates class.           - GRAV_UP:
                where direction of gravity maps to IMU reference frame
                Z-axis with Z-axis pointing in                      the
                opposite direction of gravity. IMU reference frame
                X-axis direction is defined by grav_dir_x.
                Note if grav_dir_x is parallel to gravity direction,
                this configuration fails.
                Otherwise, IMU reference frame X-axis is defined by
                projection of grav_dir_x onto a plane
                normal to the gravity vector. IMU reference frame Y-axis
                is a vector orthogonal to both                      X
                and Z axis following the right hand rule.           -
                GRAV_DOWN: where direction of gravity maps to IMU
                reference frame Z-axis with Z-axis pointing in
                the direction of gravity. IMU reference frame X-axis
                direction is defined by grav_dir_x.
                Note if grav_dir_x is parallel to gravity direction,
                this configuration fails.
                Otherwise, IMU reference frame X-axis is defined by
                projection of grav_dir_x onto a plane
                normal to the gravity vector. IMU reference frame Y-axis
                is a vector orthogonal to both                        X
                and Z axis following the right hand rule.
            custom_rpy: This field and parent_frame are used when
                localization is set to CUSTOM.         Orientation
                (fixed axis roll, pitch yaw) transform from parent_frame
                to this IMU's reference frame.         Some common
                examples are:           - IMU reports in its local frame
                on boot. IMU sensor frame is the reference frame.
                Example: parent_frame="", custom_rpy="0 0 0"           -
                IMU reports in Gazebo world frame.              Example
                sdf: parent_frame="world", custom_rpy="0 0 0"
                - IMU reports in NWU frame.              Uses
                SphericalCoordinates class to determine world frame in
                relation to magnetic north and gravity;
                i.e. rotation between North-West-Up and world (+X,+Y,+Z)
                frame is defined by SphericalCoordinates class.
                Example sdf given world is NWU: parent_frame="world",
                custom_rpy="0 0 0"           - IMU reports in NED frame.
                Uses SphericalCoordinates class to determine world frame
                in relation to magnetic north and gravity;
                i.e. rotation between North-East-Down and world
                (+X,+Y,+Z) frame is defined by SphericalCoordinates
                class.              Example sdf given world is NWU:
                parent_frame="world", custom_rpy="M_PI 0 0"           -
                IMU reports in ENU frame.              Uses
                SphericalCoordinates class to determine world frame in
                relation to magnetic north and gravity;
                i.e. rotation between East-North-Up and world (+X,+Y,+Z)
                frame is defined by SphericalCoordinates class.
                Example sdf given world is NWU: parent_frame="world",
                custom_rpy="0 0 -0.5*M_PI"           - IMU reports in
                ROS optical frame as described in
                http://www.ros.org/reps/rep-0103.html#suffix-frames,
                which is              (z-forward, x-left to right when
                facing +z, y-top to bottom when facing +z).
                (default gazebo camera is +x:view direction, +y:left,
                +z:up).              Example sdf: parent_frame="local",
                custom_rpy="-0.5*M_PI 0 -0.5*M_PI"
            grav_dir_x: Used when localization is set to GRAV_UP or
                GRAV_DOWN, a projection of this vector         into a
                plane that is orthogonal to the gravity vector
                defines the direction of the IMU reference frame's
                X-axis.         grav_dir_x is  defined in the coordinate
                frame as defined by the parent_frame element.
            """

            localization: str = field(
                default="CUSTOM",
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            custom_rpy: Optional[
                "Sensor.Imu.OrientationReferenceFrame.CustomRpy"
            ] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            grav_dir_x: Optional[
                "Sensor.Imu.OrientationReferenceFrame.GravDirX"
            ] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )

            @dataclass
            class CustomRpy:
                """
                Parameters
                ----------
                value:
                parent_frame: Name of parent frame which the custom_rpy
                    transform is defined relative to.           It can
                    be any valid fully scoped Gazebo Link name or the
                    special reserved "world" frame.           If left
                    empty, use the sensor's own local frame.
                """

                value: str = field(
                    default="0 0 0",
                    metadata={
                        "required": True,
                        "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
                    },
                )
                parent_frame: Optional[str] = field(
                    default=None,
                    metadata={
                        "type": "Attribute",
                    },
                )

            @dataclass
            class GravDirX:
                """
                Parameters
                ----------
                value:
                parent_frame: Name of parent frame in which the
                    grav_dir_x vector is defined.           It can be
                    any valid fully scoped Gazebo Link name or the
                    special reserved "world" frame.           If left
                    empty, use the sensor's own local frame.
                """

                value: str = field(
                    default="1 0 0",
                    metadata={
                        "required": True,
                        "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
                    },
                )
                parent_frame: Optional[str] = field(
                    default=None,
                    metadata={
                        "type": "Attribute",
                    },
                )

        @dataclass
        class AngularVelocity:
            """
            These elements are specific to body-frame angular velocity,
            which is expressed in radians per second.

            Parameters
            ----------
            x: Angular velocity about the X axis
            y: Angular velocity about the Y axis
            z: Angular velocity about the Z axis
            """

            x: Optional["Sensor.Imu.AngularVelocity.X"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            y: Optional["Sensor.Imu.AngularVelocity.Y"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            z: Optional["Sensor.Imu.AngularVelocity.Z"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class X:
                """
                Angular velocity about the X axis.

                Parameters
                ----------
                noise: The properties of a sensor noise model.
                """

                noise: Optional["Sensor.Imu.AngularVelocity.X.Noise"] = field(
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
                        distribution from which       noise values are
                        drawn.
                    stddev: For type "gaussian*", the standard deviation
                        of the Gaussian distribution from which noise
                        values are drawn.
                    bias_mean: For type "gaussian*", the mean of the
                        Gaussian distribution from which bias values are
                        drawn.
                    bias_stddev: For type "gaussian*", the standard
                        deviation of the Gaussian distribution from
                        which bias values are drawn.
                    dynamic_bias_stddev: For type "gaussian*", the
                        standard deviation of the noise used to drive a
                        process to model slow variations in a sensor
                        bias.
                    dynamic_bias_correlation_time: For type "gaussian*",
                        the correlation time in seconds of the noise
                        used to drive a process to model slow variations
                        in a sensor bias. A typical value, when used,
                        would be on the order of 3600 seconds (1 hour).
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
                            "required": True,
                        },
                    )
                    stddev: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    bias_mean: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    bias_stddev: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    dynamic_bias_stddev: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    dynamic_bias_correlation_time: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    precision: float = field(
                        default=0.0,
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
            class Y:
                """
                Angular velocity about the Y axis.

                Parameters
                ----------
                noise: The properties of a sensor noise model.
                """

                noise: Optional["Sensor.Imu.AngularVelocity.Y.Noise"] = field(
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
                        distribution from which       noise values are
                        drawn.
                    stddev: For type "gaussian*", the standard deviation
                        of the Gaussian distribution from which noise
                        values are drawn.
                    bias_mean: For type "gaussian*", the mean of the
                        Gaussian distribution from which bias values are
                        drawn.
                    bias_stddev: For type "gaussian*", the standard
                        deviation of the Gaussian distribution from
                        which bias values are drawn.
                    dynamic_bias_stddev: For type "gaussian*", the
                        standard deviation of the noise used to drive a
                        process to model slow variations in a sensor
                        bias.
                    dynamic_bias_correlation_time: For type "gaussian*",
                        the correlation time in seconds of the noise
                        used to drive a process to model slow variations
                        in a sensor bias. A typical value, when used,
                        would be on the order of 3600 seconds (1 hour).
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
                            "required": True,
                        },
                    )
                    stddev: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    bias_mean: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    bias_stddev: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    dynamic_bias_stddev: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    dynamic_bias_correlation_time: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    precision: float = field(
                        default=0.0,
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
            class Z:
                """
                Angular velocity about the Z axis.

                Parameters
                ----------
                noise: The properties of a sensor noise model.
                """

                noise: Optional["Sensor.Imu.AngularVelocity.Z.Noise"] = field(
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
                        distribution from which       noise values are
                        drawn.
                    stddev: For type "gaussian*", the standard deviation
                        of the Gaussian distribution from which noise
                        values are drawn.
                    bias_mean: For type "gaussian*", the mean of the
                        Gaussian distribution from which bias values are
                        drawn.
                    bias_stddev: For type "gaussian*", the standard
                        deviation of the Gaussian distribution from
                        which bias values are drawn.
                    dynamic_bias_stddev: For type "gaussian*", the
                        standard deviation of the noise used to drive a
                        process to model slow variations in a sensor
                        bias.
                    dynamic_bias_correlation_time: For type "gaussian*",
                        the correlation time in seconds of the noise
                        used to drive a process to model slow variations
                        in a sensor bias. A typical value, when used,
                        would be on the order of 3600 seconds (1 hour).
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
                            "required": True,
                        },
                    )
                    stddev: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    bias_mean: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    bias_stddev: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    dynamic_bias_stddev: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    dynamic_bias_correlation_time: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    precision: float = field(
                        default=0.0,
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
        class LinearAcceleration:
            """
            These elements are specific to body-frame linear acceleration,
            which is expressed in meters per second squared.

            Parameters
            ----------
            x: Linear acceleration about the X axis
            y: Linear acceleration about the Y axis
            z: Linear acceleration about the Z axis
            """

            x: Optional["Sensor.Imu.LinearAcceleration.X"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            y: Optional["Sensor.Imu.LinearAcceleration.Y"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            z: Optional["Sensor.Imu.LinearAcceleration.Z"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class X:
                """
                Linear acceleration about the X axis.

                Parameters
                ----------
                noise: The properties of a sensor noise model.
                """

                noise: Optional["Sensor.Imu.LinearAcceleration.X.Noise"] = field(
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
                        distribution from which       noise values are
                        drawn.
                    stddev: For type "gaussian*", the standard deviation
                        of the Gaussian distribution from which noise
                        values are drawn.
                    bias_mean: For type "gaussian*", the mean of the
                        Gaussian distribution from which bias values are
                        drawn.
                    bias_stddev: For type "gaussian*", the standard
                        deviation of the Gaussian distribution from
                        which bias values are drawn.
                    dynamic_bias_stddev: For type "gaussian*", the
                        standard deviation of the noise used to drive a
                        process to model slow variations in a sensor
                        bias.
                    dynamic_bias_correlation_time: For type "gaussian*",
                        the correlation time in seconds of the noise
                        used to drive a process to model slow variations
                        in a sensor bias. A typical value, when used,
                        would be on the order of 3600 seconds (1 hour).
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
                            "required": True,
                        },
                    )
                    stddev: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    bias_mean: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    bias_stddev: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    dynamic_bias_stddev: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    dynamic_bias_correlation_time: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    precision: float = field(
                        default=0.0,
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
            class Y:
                """
                Linear acceleration about the Y axis.

                Parameters
                ----------
                noise: The properties of a sensor noise model.
                """

                noise: Optional["Sensor.Imu.LinearAcceleration.Y.Noise"] = field(
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
                        distribution from which       noise values are
                        drawn.
                    stddev: For type "gaussian*", the standard deviation
                        of the Gaussian distribution from which noise
                        values are drawn.
                    bias_mean: For type "gaussian*", the mean of the
                        Gaussian distribution from which bias values are
                        drawn.
                    bias_stddev: For type "gaussian*", the standard
                        deviation of the Gaussian distribution from
                        which bias values are drawn.
                    dynamic_bias_stddev: For type "gaussian*", the
                        standard deviation of the noise used to drive a
                        process to model slow variations in a sensor
                        bias.
                    dynamic_bias_correlation_time: For type "gaussian*",
                        the correlation time in seconds of the noise
                        used to drive a process to model slow variations
                        in a sensor bias. A typical value, when used,
                        would be on the order of 3600 seconds (1 hour).
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
                            "required": True,
                        },
                    )
                    stddev: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    bias_mean: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    bias_stddev: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    dynamic_bias_stddev: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    dynamic_bias_correlation_time: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    precision: float = field(
                        default=0.0,
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
            class Z:
                """
                Linear acceleration about the Z axis.

                Parameters
                ----------
                noise: The properties of a sensor noise model.
                """

                noise: Optional["Sensor.Imu.LinearAcceleration.Z.Noise"] = field(
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
                        distribution from which       noise values are
                        drawn.
                    stddev: For type "gaussian*", the standard deviation
                        of the Gaussian distribution from which noise
                        values are drawn.
                    bias_mean: For type "gaussian*", the mean of the
                        Gaussian distribution from which bias values are
                        drawn.
                    bias_stddev: For type "gaussian*", the standard
                        deviation of the Gaussian distribution from
                        which bias values are drawn.
                    dynamic_bias_stddev: For type "gaussian*", the
                        standard deviation of the noise used to drive a
                        process to model slow variations in a sensor
                        bias.
                    dynamic_bias_correlation_time: For type "gaussian*",
                        the correlation time in seconds of the noise
                        used to drive a process to model slow variations
                        in a sensor bias. A typical value, when used,
                        would be on the order of 3600 seconds (1 hour).
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
                            "required": True,
                        },
                    )
                    stddev: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    bias_mean: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    bias_stddev: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    dynamic_bias_stddev: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    dynamic_bias_correlation_time: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    precision: float = field(
                        default=0.0,
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
    class Lidar:
        """
        These elements are specific to the lidar sensor.

        Parameters
        ----------
        scan:
        range: specifies range properties of each simulated lidar
        noise: The properties of the noise model that should be applied
            to generated scans
        """

        scan: Optional["Sensor.Lidar.Scan"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        range: Optional["Sensor.Lidar.Range"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        noise: Optional["Sensor.Lidar.Noise"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

        @dataclass
        class Scan:
            horizontal: Optional["Sensor.Lidar.Scan.Horizontal"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            vertical: Optional["Sensor.Lidar.Scan.Vertical"] = field(
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
                samples: The number of simulated lidar rays to generate
                    per complete laser sweep cycle.
                resolution: This number is multiplied by samples to
                    determine the number of range data points returned.
                    If resolution is not equal to one, range data is
                    interpolated.
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
                samples: The number of simulated lidar rays to generate
                    per complete laser sweep cycle.
                resolution: This number is multiplied by samples to
                    determine the number of range data points returned.
                    If resolution is not equal to one, range data is
                    interpolated.
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
            specifies range properties of each simulated lidar.

            Parameters
            ----------
            min: The minimum distance for each lidar ray.
            max: The maximum distance for each lidar ray.
            resolution: Linear resolution of each lidar ray.
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
                    "required": True,
                },
            )
            mean: float = field(
                default=0.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            stddev: float = field(
                default=0.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )

    @dataclass
    class LogicalCamera:
        """These elements are specific to logical camera sensors.

        A logical camera reports objects that fall within a frustum.
        Computation should be performed on the CPU.

        Parameters
        ----------
        near: Near clipping distance of the view frustum
        far: Far clipping distance of the view frustum
        aspect_ratio: Aspect ratio of the near and far planes. This is
            the width divided by the height of the near or far planes.
        horizontal_fov: Horizontal field of view of the frustum, in
            radians. This is the angle between the frustum's vertex and
            the edges of the near or far plane.
        """

        near: float = field(
            default=0.0,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        far: float = field(
            default=1.0,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        aspect_ratio: float = field(
            default=1.0,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        horizontal_fov: float = field(
            default=1.0,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )

    @dataclass
    class Magnetometer:
        """
        These elements are specific to a Magnetometer sensor.

        Parameters
        ----------
        x: Parameters related to the body-frame X axis of the
            magnetometer
        y: Parameters related to the body-frame Y axis of the
            magnetometer
        z: Parameters related to the body-frame Z axis of the
            magnetometer
        """

        x: Optional["Sensor.Magnetometer.X"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        y: Optional["Sensor.Magnetometer.Y"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        z: Optional["Sensor.Magnetometer.Z"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

        @dataclass
        class X:
            """
            Parameters related to the body-frame X axis of the magnetometer.

            Parameters
            ----------
            noise: The properties of a sensor noise model.
            """

            noise: Optional["Sensor.Magnetometer.X.Noise"] = field(
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
                    distribution from which       noise values are
                    drawn.
                stddev: For type "gaussian*", the standard deviation of
                    the Gaussian distribution from which noise values
                    are drawn.
                bias_mean: For type "gaussian*", the mean of the
                    Gaussian distribution from which bias values are
                    drawn.
                bias_stddev: For type "gaussian*", the standard
                    deviation of the Gaussian distribution from which
                    bias values are drawn.
                dynamic_bias_stddev: For type "gaussian*", the standard
                    deviation of the noise used to drive a process to
                    model slow variations in a sensor bias.
                dynamic_bias_correlation_time: For type "gaussian*", the
                    correlation time in seconds of the noise used to
                    drive a process to model slow variations in a sensor
                    bias. A typical value, when used, would be on the
                    order of 3600 seconds (1 hour).
                precision: For type "gaussian_quantized", the precision
                    of output signals. A value       of zero implies
                    infinite precision / no quantization.
                type: The type of noise. Currently supported types are:
                    "none" (no noise).       "gaussian" (draw noise
                    values independently for each measurement from a
                    Gaussian distribution).       "gaussian_quantized"
                    ("gaussian" plus quantization of outputs (ie.
                    rounding))
                """

                mean: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                stddev: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                bias_mean: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                bias_stddev: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                dynamic_bias_stddev: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                dynamic_bias_correlation_time: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                precision: float = field(
                    default=0.0,
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
        class Y:
            """
            Parameters related to the body-frame Y axis of the magnetometer.

            Parameters
            ----------
            noise: The properties of a sensor noise model.
            """

            noise: Optional["Sensor.Magnetometer.Y.Noise"] = field(
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
                    distribution from which       noise values are
                    drawn.
                stddev: For type "gaussian*", the standard deviation of
                    the Gaussian distribution from which noise values
                    are drawn.
                bias_mean: For type "gaussian*", the mean of the
                    Gaussian distribution from which bias values are
                    drawn.
                bias_stddev: For type "gaussian*", the standard
                    deviation of the Gaussian distribution from which
                    bias values are drawn.
                dynamic_bias_stddev: For type "gaussian*", the standard
                    deviation of the noise used to drive a process to
                    model slow variations in a sensor bias.
                dynamic_bias_correlation_time: For type "gaussian*", the
                    correlation time in seconds of the noise used to
                    drive a process to model slow variations in a sensor
                    bias. A typical value, when used, would be on the
                    order of 3600 seconds (1 hour).
                precision: For type "gaussian_quantized", the precision
                    of output signals. A value       of zero implies
                    infinite precision / no quantization.
                type: The type of noise. Currently supported types are:
                    "none" (no noise).       "gaussian" (draw noise
                    values independently for each measurement from a
                    Gaussian distribution).       "gaussian_quantized"
                    ("gaussian" plus quantization of outputs (ie.
                    rounding))
                """

                mean: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                stddev: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                bias_mean: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                bias_stddev: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                dynamic_bias_stddev: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                dynamic_bias_correlation_time: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                precision: float = field(
                    default=0.0,
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
        class Z:
            """
            Parameters related to the body-frame Z axis of the magnetometer.

            Parameters
            ----------
            noise: The properties of a sensor noise model.
            """

            noise: Optional["Sensor.Magnetometer.Z.Noise"] = field(
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
                    distribution from which       noise values are
                    drawn.
                stddev: For type "gaussian*", the standard deviation of
                    the Gaussian distribution from which noise values
                    are drawn.
                bias_mean: For type "gaussian*", the mean of the
                    Gaussian distribution from which bias values are
                    drawn.
                bias_stddev: For type "gaussian*", the standard
                    deviation of the Gaussian distribution from which
                    bias values are drawn.
                dynamic_bias_stddev: For type "gaussian*", the standard
                    deviation of the noise used to drive a process to
                    model slow variations in a sensor bias.
                dynamic_bias_correlation_time: For type "gaussian*", the
                    correlation time in seconds of the noise used to
                    drive a process to model slow variations in a sensor
                    bias. A typical value, when used, would be on the
                    order of 3600 seconds (1 hour).
                precision: For type "gaussian_quantized", the precision
                    of output signals. A value       of zero implies
                    infinite precision / no quantization.
                type: The type of noise. Currently supported types are:
                    "none" (no noise).       "gaussian" (draw noise
                    values independently for each measurement from a
                    Gaussian distribution).       "gaussian_quantized"
                    ("gaussian" plus quantization of outputs (ie.
                    rounding))
                """

                mean: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                stddev: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                bias_mean: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                bias_stddev: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                dynamic_bias_stddev: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                dynamic_bias_correlation_time: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                precision: float = field(
                    default=0.0,
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
    class Navsat:
        """
        These elements are specific to the NAVSAT sensor.

        Parameters
        ----------
        position_sensing: Parameters related to NAVSAT position
            measurement.
        velocity_sensing: Parameters related to NAVSAT position
            measurement.
        """

        position_sensing: Optional["Sensor.Navsat.PositionSensing"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        velocity_sensing: Optional["Sensor.Navsat.VelocitySensing"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

        @dataclass
        class PositionSensing:
            """
            Parameters related to NAVSAT position measurement.

            Parameters
            ----------
            horizontal: Noise parameters for horizontal position
                measurement, in units of meters.
            vertical: Noise parameters for vertical position
                measurement, in units of meters.
            """

            horizontal: Optional["Sensor.Navsat.PositionSensing.Horizontal"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            vertical: Optional["Sensor.Navsat.PositionSensing.Vertical"] = field(
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

                noise: Optional[
                    "Sensor.Navsat.PositionSensing.Horizontal.Noise"
                ] = field(
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
                        distribution from which       noise values are
                        drawn.
                    stddev: For type "gaussian*", the standard deviation
                        of the Gaussian distribution from which noise
                        values are drawn.
                    bias_mean: For type "gaussian*", the mean of the
                        Gaussian distribution from which bias values are
                        drawn.
                    bias_stddev: For type "gaussian*", the standard
                        deviation of the Gaussian distribution from
                        which bias values are drawn.
                    dynamic_bias_stddev: For type "gaussian*", the
                        standard deviation of the noise used to drive a
                        process to model slow variations in a sensor
                        bias.
                    dynamic_bias_correlation_time: For type "gaussian*",
                        the correlation time in seconds of the noise
                        used to drive a process to model slow variations
                        in a sensor bias. A typical value, when used,
                        would be on the order of 3600 seconds (1 hour).
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
                            "required": True,
                        },
                    )
                    stddev: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    bias_mean: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    bias_stddev: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    dynamic_bias_stddev: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    dynamic_bias_correlation_time: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    precision: float = field(
                        default=0.0,
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
            class Vertical:
                """
                Noise parameters for vertical position measurement, in units of
                meters.

                Parameters
                ----------
                noise: The properties of a sensor noise model.
                """

                noise: Optional["Sensor.Navsat.PositionSensing.Vertical.Noise"] = field(
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
                        distribution from which       noise values are
                        drawn.
                    stddev: For type "gaussian*", the standard deviation
                        of the Gaussian distribution from which noise
                        values are drawn.
                    bias_mean: For type "gaussian*", the mean of the
                        Gaussian distribution from which bias values are
                        drawn.
                    bias_stddev: For type "gaussian*", the standard
                        deviation of the Gaussian distribution from
                        which bias values are drawn.
                    dynamic_bias_stddev: For type "gaussian*", the
                        standard deviation of the noise used to drive a
                        process to model slow variations in a sensor
                        bias.
                    dynamic_bias_correlation_time: For type "gaussian*",
                        the correlation time in seconds of the noise
                        used to drive a process to model slow variations
                        in a sensor bias. A typical value, when used,
                        would be on the order of 3600 seconds (1 hour).
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
                            "required": True,
                        },
                    )
                    stddev: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    bias_mean: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    bias_stddev: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    dynamic_bias_stddev: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    dynamic_bias_correlation_time: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    precision: float = field(
                        default=0.0,
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
        class VelocitySensing:
            """
            Parameters related to NAVSAT position measurement.

            Parameters
            ----------
            horizontal: Noise parameters for horizontal velocity
                measurement, in units of meters/second.
            vertical: Noise parameters for vertical velocity
                measurement, in units of meters/second.
            """

            horizontal: Optional["Sensor.Navsat.VelocitySensing.Horizontal"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            vertical: Optional["Sensor.Navsat.VelocitySensing.Vertical"] = field(
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

                noise: Optional[
                    "Sensor.Navsat.VelocitySensing.Horizontal.Noise"
                ] = field(
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
                        distribution from which       noise values are
                        drawn.
                    stddev: For type "gaussian*", the standard deviation
                        of the Gaussian distribution from which noise
                        values are drawn.
                    bias_mean: For type "gaussian*", the mean of the
                        Gaussian distribution from which bias values are
                        drawn.
                    bias_stddev: For type "gaussian*", the standard
                        deviation of the Gaussian distribution from
                        which bias values are drawn.
                    dynamic_bias_stddev: For type "gaussian*", the
                        standard deviation of the noise used to drive a
                        process to model slow variations in a sensor
                        bias.
                    dynamic_bias_correlation_time: For type "gaussian*",
                        the correlation time in seconds of the noise
                        used to drive a process to model slow variations
                        in a sensor bias. A typical value, when used,
                        would be on the order of 3600 seconds (1 hour).
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
                            "required": True,
                        },
                    )
                    stddev: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    bias_mean: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    bias_stddev: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    dynamic_bias_stddev: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    dynamic_bias_correlation_time: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    precision: float = field(
                        default=0.0,
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
            class Vertical:
                """
                Noise parameters for vertical velocity measurement, in units of
                meters/second.

                Parameters
                ----------
                noise: The properties of a sensor noise model.
                """

                noise: Optional["Sensor.Navsat.VelocitySensing.Vertical.Noise"] = field(
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
                        distribution from which       noise values are
                        drawn.
                    stddev: For type "gaussian*", the standard deviation
                        of the Gaussian distribution from which noise
                        values are drawn.
                    bias_mean: For type "gaussian*", the mean of the
                        Gaussian distribution from which bias values are
                        drawn.
                    bias_stddev: For type "gaussian*", the standard
                        deviation of the Gaussian distribution from
                        which bias values are drawn.
                    dynamic_bias_stddev: For type "gaussian*", the
                        standard deviation of the noise used to drive a
                        process to model slow variations in a sensor
                        bias.
                    dynamic_bias_correlation_time: For type "gaussian*",
                        the correlation time in seconds of the noise
                        used to drive a process to model slow variations
                        in a sensor bias. A typical value, when used,
                        would be on the order of 3600 seconds (1 hour).
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
                            "required": True,
                        },
                    )
                    stddev: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    bias_mean: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    bias_stddev: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    dynamic_bias_stddev: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    dynamic_bias_correlation_time: float = field(
                        default=0.0,
                        metadata={
                            "type": "Element",
                            "namespace": "",
                            "required": True,
                        },
                    )
                    precision: float = field(
                        default=0.0,
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
                    "required": True,
                },
            )
            mean: float = field(
                default=0.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            stddev: float = field(
                default=0.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )

    @dataclass
    class Sonar:
        """
        These elements are specific to the sonar sensor.

        Parameters
        ----------
        geometry: The sonar collision shape. Currently supported
            geometries are: "cone" and "sphere".
        min: Minimum range
        max: Max range
        radius: Radius of the sonar cone at max range. This parameter is
            only used if geometry is "cone".
        """

        geometry: str = field(
            default="cone",
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        min: float = field(
            default=0.0,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        max: float = field(
            default=1.0,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        radius: float = field(
            default=0.5,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
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
                "required": True,
            },
        )
        frequency: float = field(
            default=2442.0,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        min_frequency: float = field(
            default=2412.0,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        max_frequency: float = field(
            default=2484.0,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        gain: float = field(
            default=2.5,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        power: float = field(
            default=14.5,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        sensitivity: float = field(
            default=-90.0,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
