from dataclasses import dataclass, field
from typing import List

__NAMESPACE__ = "sdformat/spherical_coordinates"


@dataclass
class SphericalCoordinatesType:
    """
    Parameters
    ----------
    surface_model: Name of planetary surface model, used to determine
        the surface altitude at a given latitude and longitude. The
        default is an ellipsoid model of the earth based on the WGS-84
        standard. It is used in Gazebo's GPS sensor implementation.
    latitude_deg: Geodetic latitude at origin of gazebo reference frame,
        specified in units of degrees.
    longitude_deg: Longitude at origin of gazebo reference frame,
        specified in units of degrees.
    elevation: Elevation of origin of gazebo reference frame, specified
        in meters.
    heading_deg: Heading offset of gazebo reference frame, measured as
        angle between East and gazebo x axis, or equivalently, the angle
        between North and gazebo y axis. The angle is specified in
        degrees.
    """
    class Meta:
        name = "spherical_coordinatesType"

    surface_model: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    latitude_deg: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    longitude_deg: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    elevation: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    heading_deg: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
