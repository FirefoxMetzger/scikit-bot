from dataclasses import dataclass, field
from typing import List

__NAMESPACE__ = "sdformat/lidar"


@dataclass
class LidarType:
    """
    Parameters
    ----------
    scan:
    range: specifies range properties of each simulated lidar
    noise: The properties of the noise model that should be applied to
        generated scans
    """
    class Meta:
        name = "lidarType"

    scan: List["LidarType.Scan"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    range: List["LidarType.Range"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    noise: List["LidarType.Noise"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )

    @dataclass
    class Scan:
        horizontal: List["LidarType.Scan.Horizontal"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        vertical: List["LidarType.Scan.Vertical"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )

        @dataclass
        class Horizontal:
            """
            Parameters
            ----------
            samples: The number of simulated lidar rays to generate per
                complete laser sweep cycle.
            resolution: This number is multiplied by samples to
                determine the number of range data points returned. If
                resolution is not equal to one, range data is
                interpolated.
            min_angle:
            max_angle: Must be greater or equal to min_angle
            """
            samples: List[int] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            resolution: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            min_angle: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            max_angle: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )

        @dataclass
        class Vertical:
            """
            Parameters
            ----------
            samples: The number of simulated lidar rays to generate per
                complete laser sweep cycle.
            resolution: This number is multiplied by samples to
                determine the number of range data points returned. If
                resolution is not equal to one, range data is
                interpolated.
            min_angle:
            max_angle: Must be greater or equal to min_angle
            """
            samples: List[int] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            resolution: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            min_angle: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            max_angle: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )

    @dataclass
    class Range:
        """
        Parameters
        ----------
        min: The minimum distance for each lidar ray.
        max: The maximum distance for each lidar ray.
        resolution: Linear resolution of each lidar ray.
        """
        min: List[float] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        max: List[float] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        resolution: List[float] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )

    @dataclass
    class Noise:
        """
        Parameters
        ----------
        type: The type of noise.  Currently supported types are:
            "gaussian" (draw noise values independently for each beam
            from a Gaussian distribution).
        mean: For type "gaussian," the mean of the Gaussian distribution
            from which noise values are drawn.
        stddev: For type "gaussian," the standard deviation of the
            Gaussian distribution from which noise values are drawn.
        """
        type: List[str] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        mean: List[float] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        stddev: List[float] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
