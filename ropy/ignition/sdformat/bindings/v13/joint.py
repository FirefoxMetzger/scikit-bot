from dataclasses import dataclass, field
from typing import Optional

__NAMESPACE__ = "sdformat/v1.3/joint.xsd"


@dataclass
class Joint:
    """
    A joint connections two links with kinematic and dynamic properties.

    Parameters
    ----------
    parent: Name of the parent link
    child: Name of the child link
    pose: offset from child link origin in child link frame.
    thread_pitch:
    axis: The joint axis specified in the model frame. This is the axis
        of rotation for revolute joints, the axis of translation for
        prismatic joints. The axis is currently specified in the model
        frame of reference, but this will be changed to the joint frame
        in future version of SDFormat (see gazebo issue #494).
    axis2: The second joint axis specified in the model frame. This is
        the second axis of rotation for revolute2 joints and universal
        joints. The axis is currently specified in the model frame of
        reference, but this will be changed to the joint frame in future
        version of SDFormat (see gazebo issue #494).
    physics: Parameters that are specific to a certain physics engine.
    name: A unique name for the joint within the scope of the model.
    type: The type of joint, which must be one of the following:
        (revolute) a hinge joint that rotates on a single axis with
        either a fixed or continuous range of motion, (revolute2) same
        as two revolute joints connected in series, (prismatic) a
        sliding joint that slides along an axis with a limited range
        specified by upper and lower limits, (ball) a ball and socket
        joint, (universal), like a ball joint, but constrains one degree
        of freedom, (piston) similar to a Slider joint except that
        rotation around the translation axis is possible.
    """

    class Meta:
        name = "joint"

    parent: str = field(
        default="__default__",
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    child: str = field(
        default="__default__",
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
    thread_pitch: float = field(
        default=1.0,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    axis: Optional["Joint.Axis"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
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
        """The joint axis specified in the model frame.

        This is the axis of rotation for revolute joints, the axis of
        translation for prismatic joints. The axis is currently
        specified in the model frame of reference, but this will be
        changed to the joint frame in future version of SDFormat (see
        gazebo issue #494).

        Parameters
        ----------
        xyz: Represents the x,y,z components of a vector. The vector
            should be normalized.
        dynamics: An element specifying physical properties of the
            joint. These values are used to specify modeling properties
            of the joint, particularly useful for simulation.
        limit: specifies the limits of this joint
        """

        xyz: str = field(
            default="0 0 1",
            metadata={
                "type": "Element",
                "namespace": "",
                "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
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
        class Dynamics:
            """An element specifying physical properties of the joint.

            These values are used to specify modeling properties of the
            joint, particularly useful for simulation.

            Parameters
            ----------
            damping: The physical velocity dependent viscous damping
                coefficient of the joint.
            friction: The physical static friction value of the joint.
            """

            damping: float = field(
                default=0.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            friction: float = field(
                default=0.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

        @dataclass
        class Limit:
            """
            specifies the limits of this joint.

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
            """

            lower: float = field(
                default=-1e16,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            upper: float = field(
                default=1e16,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            effort: float = field(
                default=-1.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            velocity: float = field(
                default=-1.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

    @dataclass
    class Axis2:
        """The second joint axis specified in the model frame.

        This is the second axis of rotation for revolute2 joints and
        universal joints. The axis is currently specified in the model
        frame of reference, but this will be changed to the joint frame
        in future version of SDFormat (see gazebo issue #494).

        Parameters
        ----------
        xyz: Represents the x,y,z components of a vector. The vector
            should be normalized.
        dynamics: An element specifying physical properties of the
            joint. These values are used to specify modeling properties
            of the joint, particularly useful for simulation.
        limit:
        """

        xyz: str = field(
            default="0 0 1",
            metadata={
                "type": "Element",
                "namespace": "",
                "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
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
            """

            damping: float = field(
                default=0.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            friction: float = field(
                default=0.0,
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
            """

            lower: float = field(
                default=-1e16,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            upper: float = field(
                default=1e16,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            effort: float = field(
                default=-1.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            velocity: float = field(
                default=-1.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

    @dataclass
    class Physics:
        """
        Parameters that are specific to a certain physics engine.

        Parameters
        ----------
        ode: ODE specific parameters
        """

        ode: Optional["Joint.Physics.Ode"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

        @dataclass
        class Ode:
            """
            ODE specific parameters.

            Parameters
            ----------
            provide_feedback: If provide feedback is set to true, ODE
                will compute the constraint forces at this joint.
            cfm_damping: If cfm damping is set to true, ODE will use CFM
                to simulate damping, allows for infinite damping, and
                one additional constraint row (previously used for joint
                limit) is always active.
            fudge_factor: Scale the excess for in a joint motor at joint
                limits. Should be between zero and one.
            cfm: Constraint force mixing used when not at a stop
            bounce: Bounciness of the limits
            max_force: Maximum force or torque used to reach the desired
                velocity.
            velocity: The desired velocity of the joint. Should only be
                set if you want the joint to move on load.
            limit:
            suspension:
            """

            provide_feedback: bool = field(
                default=False,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            cfm_damping: bool = field(
                default=False,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            fudge_factor: float = field(
                default=0.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            cfm: float = field(
                default=0.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            bounce: float = field(
                default=0.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            max_force: float = field(
                default=0.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            velocity: float = field(
                default=0.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
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
                    },
                )
                erp: float = field(
                    default=0.2,
                    metadata={
                        "type": "Element",
                        "namespace": "",
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
                    },
                )
                erp: float = field(
                    default=0.2,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    },
                )
