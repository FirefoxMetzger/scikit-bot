from dataclasses import dataclass, field
from typing import List
from .noise_type import NoiseType

__NAMESPACE__ = "sdformat/imu"


@dataclass
class ImuType:
    """
    Parameters
    ----------
    topic: Topic on which data is published.
    angular_velocity: These elements are specific to body-frame angular
        velocity, which is expressed in radians per second
    linear_acceleration: These elements are specific to body-frame
        linear acceleration, which is expressed in meters per second
        squared
    noise: The properties of the noise model that should be applied to
        generated data
    """

    class Meta:
        name = "imuType"

    topic: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    angular_velocity: List["ImuType.AngularVelocity"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    linear_acceleration: List["ImuType.LinearAcceleration"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    noise: List["ImuType.Noise"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )

    @dataclass
    class AngularVelocity:
        """
        Parameters
        ----------
        x: Angular velocity about the X axis
        y: Angular velocity about the Y axis
        z: Angular velocity about the Z axis
        """

        x: List["ImuType.AngularVelocity.X"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        y: List["ImuType.AngularVelocity.Y"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        z: List["ImuType.AngularVelocity.Z"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

        @dataclass
        class X:
            """
            Parameters
            ----------
            noise: The properties of a sensor noise model.
            """

            noise: List[NoiseType] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

        @dataclass
        class Y:
            """
            Parameters
            ----------
            noise: The properties of a sensor noise model.
            """

            noise: List[NoiseType] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

        @dataclass
        class Z:
            """
            Parameters
            ----------
            noise: The properties of a sensor noise model.
            """

            noise: List[NoiseType] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

    @dataclass
    class LinearAcceleration:
        """
        Parameters
        ----------
        x: Linear acceleration about the X axis
        y: Linear acceleration about the Y axis
        z: Linear acceleration about the Z axis
        """

        x: List["ImuType.LinearAcceleration.X"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        y: List["ImuType.LinearAcceleration.Y"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        z: List["ImuType.LinearAcceleration.Z"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

        @dataclass
        class X:
            """
            Parameters
            ----------
            noise: The properties of a sensor noise model.
            """

            noise: List[NoiseType] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

        @dataclass
        class Y:
            """
            Parameters
            ----------
            noise: The properties of a sensor noise model.
            """

            noise: List[NoiseType] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

        @dataclass
        class Z:
            """
            Parameters
            ----------
            noise: The properties of a sensor noise model.
            """

            noise: List[NoiseType] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

    @dataclass
    class Noise:
        """
        Parameters
        ----------
        type: The type of noise.  Currently supported types are:
            "gaussian" (draw noise values independently for each beam
            from a Gaussian distribution).
        rate: Noise parameters for angular rates.
        accel: Noise parameters for linear accelerations.
        """

        type: List[str] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        rate: List["ImuType.Noise.Rate"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        accel: List["ImuType.Noise.Accel"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

        @dataclass
        class Rate:
            """
            Parameters
            ----------
            mean: For type "gaussian," the mean of the Gaussian
                distribution from which noise values are drawn.
            stddev: For type "gaussian," the standard deviation of the
                Gaussian distribution from which noise values are drawn.
            bias_mean: For type "gaussian," the mean of the Gaussian
                distribution from which bias values are drawn.
            bias_stddev: For type "gaussian," the standard deviation of
                the Gaussian distribution from which bias values are
                drawn.
            """

            mean: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            stddev: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            bias_mean: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            bias_stddev: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

        @dataclass
        class Accel:
            """
            Parameters
            ----------
            mean: For type "gaussian," the mean of the Gaussian
                distribution from which noise values are drawn.
            stddev: For type "gaussian," the standard deviation of the
                Gaussian distribution from which noise values are drawn.
            bias_mean: For type "gaussian," the mean of the Gaussian
                distribution from which bias values are drawn.
            bias_stddev: For type "gaussian," the standard deviation of
                the Gaussian distribution from which bias values are
                drawn.
            """

            mean: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            stddev: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            bias_mean: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            bias_stddev: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
