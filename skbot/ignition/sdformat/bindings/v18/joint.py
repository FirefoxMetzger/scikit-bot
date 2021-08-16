from dataclasses import dataclass, field
from typing import List, Optional
from .sensor import Sensor

__NAMESPACE__ = "sdformat/v1.8/joint.xsd"


@dataclass
class Joint:
    """A joint connects two links with kinematic and dynamic properties.

    By default, the pose of a joint is expressed in the child link
    frame.

    Parameters
    ----------
    parent: Name of the parent frame or "world".
    child: Name of the child frame. The value "world" may not be
        specified.
    gearbox_ratio: Parameter for gearbox joints.  Given theta_1 and
        theta_2 defined in description for gearbox_reference_body,
        theta_2 = -gearbox_ratio * theta_1.
    gearbox_reference_body: Parameter for gearbox joints.  Gearbox ratio
        is enforced over two joint angles.  First joint angle (theta_1)
        is the angle from the gearbox_reference_body to the parent link
        in the direction of the axis element and the second joint angle
        (theta_2) is the angle from the gearbox_reference_body to the
        child link in the direction of the axis2 element.
    thread_pitch: Parameter for screw joints.
    axis: Parameters related to the axis of rotation for revolute
        joints,       the axis of translation for prismatic joints.
    axis2: Parameters related to the second axis of rotation for
        revolute2 joints and universal joints.
    physics: Parameters that are specific to a certain physics engine.
    pose: A position(x,y,z) and orientation(roll, pitch yaw) with
        respect to the frame named in the relative_to attribute.
    sensor: The sensor tag describes the type and properties of a
        sensor.
    name: A unique name for the joint within the scope of the model.
    type: The type of joint, which must be one of the following:
        (continuous) a hinge joint that rotates on a single axis with a
        continuous range of motion,       (revolute) a hinge joint that
        rotates on a single axis with a fixed range of motion,
        (gearbox) geared revolute joints,       (revolute2) same as two
        revolute joints connected in series,       (prismatic) a sliding
        joint that slides along an axis with a limited range specified
        by upper and lower limits,       (ball) a ball and socket joint,
        (screw) a single degree of freedom joint with coupled sliding
        and rotational motion,       (universal) like a ball joint, but
        constrains one degree of freedom,       (fixed) a joint with
        zero degrees of freedom that rigidly connects two links.
    """

    class Meta:
        name = "joint"

    parent: str = field(
        default="__default__",
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    child: str = field(
        default="__default__",
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    gearbox_ratio: float = field(
        default=1.0,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    gearbox_reference_body: str = field(
        default="__default__",
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    thread_pitch: float = field(
        default=1.0,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    axis: Optional["Joint.Axis"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    axis2: Optional["Joint.Axis2"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    physics: Optional["Joint.Physics"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    pose: Optional["Joint.Pose"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    sensor: List[Sensor] = field(
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
    type: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )

    @dataclass
    class Axis:
        """
        Parameters related to the axis of rotation for revolute joints,
        the axis of translation for prismatic joints.

        Parameters
        ----------
        xyz: Represents the x,y,z components of the axis unit vector.
            The axis is         expressed in the joint frame unless a
            different frame is expressed in         the expressed_in
            attribute. The vector should be normalized.
        dynamics: An element specifying physical properties of the
            joint. These values are used to specify modeling properties
            of the joint, particularly useful for simulation.
        limit: specifies the limits of this joint
        """

        xyz: Optional["Joint.Axis.Xyz"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        dynamics: Optional["Joint.Axis.Dynamics"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        limit: Optional["Joint.Axis.Limit"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )

        @dataclass
        class Xyz:
            """
            Parameters
            ----------
            value:
            expressed_in: Name of frame in whose coordinates the xyz
                unit vector is expressed.
            """

            value: str = field(
                default="0 0 1",
                metadata={
                    "required": True,
                    "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
                },
            )
            expressed_in: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                },
            )

        @dataclass
        class Dynamics:
            """An element specifying physical properties of the joint.

            These values are used to specify modeling properties of the
            joint, particularly useful for simulation.

            Parameters
            ----------
            damping: The physical velocity dependent viscous damping
                coefficient of the joint.
            friction: The physical static friction value of the joint.
            spring_reference: The spring reference position for this
                joint axis.
            spring_stiffness: The spring stiffness for this joint axis.
            """

            damping: float = field(
                default=0.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            friction: float = field(
                default=0.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            spring_reference: float = field(
                default=0.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            spring_stiffness: float = field(
                default=0.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )

        @dataclass
        class Limit:
            """
            specifies the limits of this joint.

            Parameters
            ----------
            lower: Specifies the lower joint limit (radians for revolute
                joints, meters for prismatic joints). Omit if joint is
                continuous.
            upper: Specifies the upper joint limit (radians for revolute
                joints, meters for prismatic joints). Omit if joint is
                continuous.
            effort: A value for enforcing the maximum joint effort
                applied. Limit is not enforced if value is negative.
            velocity: A value for enforcing the maximum joint velocity.
            stiffness: Joint stop stiffness.
            dissipation: Joint stop dissipation.
            """

            lower: float = field(
                default=-1e16,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            upper: float = field(
                default=1e16,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            effort: float = field(
                default=-1.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            velocity: float = field(
                default=-1.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            stiffness: float = field(
                default=100000000.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            dissipation: float = field(
                default=1.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )

    @dataclass
    class Axis2:
        """
        Parameters related to the second axis of rotation for revolute2 joints
        and universal joints.

        Parameters
        ----------
        xyz: Represents the x,y,z components of the axis unit vector.
            The axis is         expressed in the joint frame unless a
            different frame is expressed in         the expressed_in
            attribute. The vector should be normalized.
        dynamics: An element specifying physical properties of the
            joint. These values are used to specify modeling properties
            of the joint, particularly useful for simulation.
        limit:
        """

        xyz: Optional["Joint.Axis2.Xyz"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        dynamics: Optional["Joint.Axis2.Dynamics"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        limit: Optional["Joint.Axis2.Limit"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )

        @dataclass
        class Xyz:
            """
            Parameters
            ----------
            value:
            expressed_in: Name of frame in whose coordinates the xyz
                unit vector is expressed.
            """

            value: str = field(
                default="0 0 1",
                metadata={
                    "required": True,
                    "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
                },
            )
            expressed_in: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                },
            )

        @dataclass
        class Dynamics:
            """An element specifying physical properties of the joint.

            These values are used to specify modeling properties of the
            joint, particularly useful for simulation.

            Parameters
            ----------
            damping: The physical velocity dependent viscous damping
                coefficient of the joint.  EXPERIMENTAL: if damping
                coefficient is negative and implicit_spring_damper is
                true, adaptive damping is used.
            friction: The physical static friction value of the joint.
            spring_reference: The spring reference position for this
                joint axis.
            spring_stiffness: The spring stiffness for this joint axis.
            """

            damping: float = field(
                default=0.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            friction: float = field(
                default=0.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            spring_reference: float = field(
                default=0.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            spring_stiffness: float = field(
                default=0.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )

        @dataclass
        class Limit:
            """
            Parameters
            ----------
            lower: An attribute specifying the lower joint limit
                (radians for revolute joints, meters for prismatic
                joints). Omit if joint is continuous.
            upper: An attribute specifying the upper joint limit
                (radians for revolute joints, meters for prismatic
                joints). Omit if joint is continuous.
            effort: An attribute for enforcing the maximum joint effort
                applied by Joint::SetForce.  Limit is not enforced if
                value is negative.
            velocity: (not implemented) An attribute for enforcing the
                maximum joint velocity.
            stiffness: Joint stop stiffness. Supported physics engines:
                SimBody.
            dissipation: Joint stop dissipation. Supported physics
                engines: SimBody.
            """

            lower: float = field(
                default=-1e16,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            upper: float = field(
                default=1e16,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            effort: float = field(
                default=-1.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            velocity: float = field(
                default=-1.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            stiffness: float = field(
                default=100000000.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            dissipation: float = field(
                default=1.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )

    @dataclass
    class Physics:
        """
        Parameters that are specific to a certain physics engine.

        Parameters
        ----------
        simbody: Simbody specific parameters
        ode: ODE specific parameters
        provide_feedback: If provide feedback is set to true, physics
            engine will compute the constraint forces at this joint.
        """

        simbody: Optional["Joint.Physics.Simbody"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        ode: Optional["Joint.Physics.Ode"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        provide_feedback: bool = field(
            default=False,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )

        @dataclass
        class Simbody:
            """
            Simbody specific parameters.

            Parameters
            ----------
            must_be_loop_joint: Force cut in the multibody graph at this
                joint.
            """

            must_be_loop_joint: bool = field(
                default=False,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )

        @dataclass
        class Ode:
            """
            ODE specific parameters.

            Parameters
            ----------
            cfm_damping: If cfm damping is set to true, ODE will use CFM
                to simulate damping, allows for infinite damping, and
                one additional constraint row (previously used for joint
                limit) is always active.
            implicit_spring_damper: If implicit_spring_damper is set to
                true, ODE will use CFM, ERP to simulate stiffness and
                damping, allows for infinite damping, and one additional
                constraint row (previously used for joint limit) is
                always active.  This replaces cfm_damping parameter in
                SDFormat 1.4.
            fudge_factor: Scale the excess for in a joint motor at joint
                limits. Should be between zero and one.
            cfm: Constraint force mixing for constrained directions
            erp: Error reduction parameter for constrained directions
            bounce: Bounciness of the limits
            max_force: Maximum force or torque used to reach the desired
                velocity.
            velocity: The desired velocity of the joint. Should only be
                set if you want the joint to move on load.
            limit:
            suspension:
            """

            cfm_damping: bool = field(
                default=False,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            implicit_spring_damper: bool = field(
                default=False,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            fudge_factor: float = field(
                default=0.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            cfm: float = field(
                default=0.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            erp: float = field(
                default=0.2,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            bounce: float = field(
                default=0.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            max_force: float = field(
                default=0.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            velocity: float = field(
                default=0.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            limit: Optional["Joint.Physics.Ode.Limit"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            suspension: Optional["Joint.Physics.Ode.Suspension"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Limit:
                """
                Parameters
                ----------
                cfm: Constraint force mixing parameter used by the joint
                    stop
                erp: Error reduction parameter used by the joint stop
                """

                cfm: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                erp: float = field(
                    default=0.2,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )

            @dataclass
            class Suspension:
                """
                Parameters
                ----------
                cfm: Suspension constraint force mixing parameter
                erp: Suspension error reduction parameter
                """

                cfm: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                erp: float = field(
                    default=0.2,
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
