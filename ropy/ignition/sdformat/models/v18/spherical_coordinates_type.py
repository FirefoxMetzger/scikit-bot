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
    world_frame_orientation: This field identifies how Gazebo world
        frame is aligned in Geographical sense.  The final Gazebo world
        frame orientation is obtained by rotating a frame aligned with
        following notation by the field heading_deg (Note that
        heading_deg corresponds to positive yaw rotation in the NED
        frame, so it's inverse specifies positive Z-rotation in ENU or
        NWU). Options are: - ENU (East-North-Up) - NED (North-East-Down)
        - NWU (North-West-Up) For example, world frame specified by
        setting world_orientation="ENU" and heading_deg=-90° is
        effectively equivalent to NWU with heading of 0°.
    latitude_deg: Geodetic latitude at origin of gazebo reference frame,
        specified in units of degrees.
    longitude_deg: Longitude at origin of gazebo reference frame,
        specified in units of degrees.
    elevation: Elevation of origin of gazebo reference frame, specified
        in meters.
    heading_deg: Heading offset of gazebo reference frame, measured as
        angle between Gazebo world frame and the world_frame_orientation
        type (ENU/NED/NWU). Rotations about the downward-vector (e.g.
        North to East) are positive. The direction of rotation is chosen
        to be consistent with compass heading convention (e.g. 0 degrees
        points North and 90 degrees points East, positive rotation
        indicates counterclockwise rotation when viewed from top-down
        direction). The angle is specified in degrees.
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
    world_frame_orientation: List[str] = field(
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
