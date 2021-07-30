from dataclasses import dataclass, field
from typing import List, Optional
from .noise_type import NoiseType

__NAMESPACE__ = "sdformat/imu"


@dataclass
class ImuType:
    """
    Parameters
    ----------
    orientation_reference_frame:
    angular_velocity: These elements are specific to body-frame angular
        velocity, which is expressed in radians per second
    linear_acceleration: These elements are specific to body-frame
        linear acceleration, which is expressed in meters per second
        squared
    """
    class Meta:
        name = "imuType"

    orientation_reference_frame: List["ImuType.OrientationReferenceFrame"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    angular_velocity: List["ImuType.AngularVelocity"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    linear_acceleration: List["ImuType.LinearAcceleration"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )

    @dataclass
    class OrientationReferenceFrame:
        """
        Parameters
        ----------
        localization: This string represents special hardcoded use cases
            that are commonly seen with typical robot IMU's: - CUSTOM:
            use Euler angle custom_rpy orientation specification. The
            orientation of the IMU's reference frame is defined by
            adding the custom_rpy rotation to the parent_frame. - NED:
            The IMU XYZ aligns with NED, where NED orientation relative
            to Gazebo world is defined by the SphericalCoordinates
            class. - ENU: The IMU XYZ aligns with ENU, where ENU
            orientation relative to Gazebo world is defined by the
            SphericalCoordinates class. - NWU: The IMU XYZ aligns with
            NWU, where NWU orientation relative to Gazebo world is
            defined by the SphericalCoordinates class. - GRAV_UP: where
            direction of gravity maps to IMU reference frame Z-axis with
            Z-axis pointing in the opposite direction of gravity. IMU
            reference frame X-axis direction is defined by grav_dir_x.
            Note if grav_dir_x is parallel to gravity direction, this
            configuration fails. Otherwise, IMU reference frame X-axis
            is defined by projection of grav_dir_x onto a plane normal
            to the gravity vector. IMU reference frame Y-axis is a
            vector orthogonal to both X and Z axis following the right
            hand rule. - GRAV_DOWN: where direction of gravity maps to
            IMU reference frame Z-axis with Z-axis pointing in the
            direction of gravity. IMU reference frame X-axis direction
            is defined by grav_dir_x. Note if grav_dir_x is parallel to
            gravity direction, this configuration fails. Otherwise, IMU
            reference frame X-axis is defined by projection of
            grav_dir_x onto a plane normal to the gravity vector. IMU
            reference frame Y-axis is a vector orthogonal to both X and
            Z axis following the right hand rule.
        custom_rpy: This field and parent_frame are used when
            localization is set to CUSTOM. Orientation (fixed axis roll,
            pitch yaw) transform from parent_frame to this IMU's
            reference frame. Some common examples are: - IMU reports in
            its local frame on boot. IMU sensor frame is the reference
            frame. Example: parent_frame="", custom_rpy="0 0 0" - IMU
            reports in Gazebo world frame. Example sdf:
            parent_frame="world", custom_rpy="0 0 0" - IMU reports in
            NWU frame. Uses SphericalCoordinates class to determine
            world frame in relation to magnetic north and gravity; i.e.
            rotation between North-West-Up and world (+X,+Y,+Z) frame is
            defined by SphericalCoordinates class. Example sdf given
            world is NWU: parent_frame="world", custom_rpy="0 0 0" - IMU
            reports in NED frame. Uses SphericalCoordinates class to
            determine world frame in relation to magnetic north and
            gravity; i.e. rotation between North-East-Down and world
            (+X,+Y,+Z) frame is defined by SphericalCoordinates class.
            Example sdf given world is NWU: parent_frame="world",
            custom_rpy="M_PI 0 0" - IMU reports in ENU frame. Uses
            SphericalCoordinates class to determine world frame in
            relation to magnetic north and gravity; i.e. rotation
            between East-North-Up and world (+X,+Y,+Z) frame is defined
            by SphericalCoordinates class. Example sdf given world is
            NWU: parent_frame="world", custom_rpy="0 0 -0.5*M_PI" - IMU
            reports in ROS optical frame as described in
            http://www.ros.org/reps/rep-0103.html#suffix-frames, which
            is (z-forward, x-left to right when facing +z, y-top to
            bottom when facing +z). (default gazebo camera is +x:view
            direction, +y:left, +z:up). Example sdf:
            parent_frame="local", custom_rpy="-0.5*M_PI 0 -0.5*M_PI"
        grav_dir_x: Used when localization is set to GRAV_UP or
            GRAV_DOWN, a projection of this vector into a plane that is
            orthogonal to the gravity vector defines the direction of
            the IMU reference frame's X-axis. grav_dir_x is  defined in
            the coordinate frame as defined by the parent_frame element.
        """
        localization: List[str] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        custom_rpy: List["ImuType.OrientationReferenceFrame.CustomRpy"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        grav_dir_x: List["ImuType.OrientationReferenceFrame.GravDirX"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )

        @dataclass
        class CustomRpy:
            """
            Parameters
            ----------
            value:
            parent_frame: Name of parent frame which the custom_rpy
                transform is defined relative to. It can be any valid
                fully scoped Gazebo Link name or the special reserved
                "world" frame. If left empty, use the sensor's own local
                frame.
            """
            value: Optional[str] = field(
                default=None,
                metadata={
                    "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
                }
            )
            parent_frame: str = field(
                default="",
                metadata={
                    "type": "Attribute",
                }
            )

        @dataclass
        class GravDirX:
            """
            Parameters
            ----------
            value:
            parent_frame: Name of parent frame in which the grav_dir_x
                vector is defined. It can be any valid fully scoped
                Gazebo Link name or the special reserved "world" frame.
                If left empty, use the sensor's own local frame.
            """
            value: Optional[str] = field(
                default=None,
                metadata={
                    "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
                }
            )
            parent_frame: str = field(
                default="",
                metadata={
                    "type": "Attribute",
                }
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
            }
        )
        y: List["ImuType.AngularVelocity.Y"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        z: List["ImuType.AngularVelocity.Z"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
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
                }
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
                }
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
                }
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
            }
        )
        y: List["ImuType.LinearAcceleration.Y"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        z: List["ImuType.LinearAcceleration.Z"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
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
                }
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
                }
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
                }
            )
