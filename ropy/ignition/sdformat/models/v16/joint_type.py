from dataclasses import dataclass, field
from typing import List, Optional
from .frame_type import FrameType
from .pose_type import PoseType
from .sensor_type import SensorType

__NAMESPACE__ = "sdformat/joint"


@dataclass
class JointType:
    """A joint connects two links with kinematic and dynamic properties.

    By default, the pose of a joint is expressed in the child link
    frame.

    Parameters
    ----------
    parent: Name of the parent link
    child: Name of the child link
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
        joints, the axis of translation for prismatic joints.
    axis2: Parameters related to the second axis of rotation for
        revolute2 joints and universal joints.
    physics: Parameters that are specific to a certain physics engine.
    frame: A frame of reference to which a pose is relative.
    pose: A position(x,y,z) and orientation(roll, pitch yaw) with
        respect to the specified frame.
    sensor: The sensor tag describes the type and properties of a
        sensor.
    name: A unique name for the joint within the scope of the model.
    type: The type of joint, which must be one of the following:
        (continuous) a hinge joint that rotates on a single axis with a
        continuous range of motion, (revolute) a hinge joint that
        rotates on a single axis with a fixed range of motion, (gearbox)
        geared revolute joints, (revolute2) same as two revolute joints
        connected in series, (prismatic) a sliding joint that slides
        along an axis with a limited range specified by upper and lower
        limits, (ball) a ball and socket joint, (screw) a single degree
        of freedom joint with coupled sliding and rotational motion,
        (universal) like a ball joint, but constrains one degree of
        freedom, (fixed) a joint with zero degrees of freedom that
        rigidly connects two links.
    """
    class Meta:
        name = "jointType"

    parent: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    child: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    gearbox_ratio: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    gearbox_reference_body: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    thread_pitch: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    axis: List["JointType.Axis"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    axis2: List["JointType.Axis2"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    physics: List["JointType.Physics"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    frame: List[FrameType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    pose: List[PoseType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    sensor: List[SensorType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    type: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )

    @dataclass
    class Axis:
        """
        Parameters related to the axis of rotation for revolute joints, the
        axis of translation for prismatic joints.

        Parameters
        ----------
        initial_position: Default joint position for this joint axis.
        xyz: Represents the x,y,z components of the axis unit vector.
            The axis is expressed in the joint frame unless the
            use_parent_model_frame flag is set to true. The vector
            should be normalized.
        use_parent_model_frame: Flag to interpret the axis xyz element
            in the parent model frame instead of joint frame. Provided
            for Gazebo compatibility (see
            https://github.com/osrf/gazebo/issue/494 ).
        dynamics: An element specifying physical properties of the
            joint. These values are used to specify modeling properties
            of the joint, particularly useful for simulation.
        limit: specifies the limits of this joint
        """
        initial_position: List[float] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        xyz: List[str] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
                "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
            }
        )
        use_parent_model_frame: List[bool] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        dynamics: List["JointType.Axis.Dynamics"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        limit: List["JointType.Axis.Limit"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
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
            damping: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            friction: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            spring_reference: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            spring_stiffness: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
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
            lower: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            upper: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            effort: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            velocity: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            stiffness: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            dissipation: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )

    @dataclass
    class Axis2:
        """
        Parameters related to the second axis of rotation for revolute2 joints
        and universal joints.

        Parameters
        ----------
        initial_position: Default joint position for this joint axis.
        xyz: Represents the x,y,z components of the axis unit vector.
            The axis is expressed in the joint frame unless the
            use_parent_model_frame flag is set to true. The vector
            should be normalized.
        use_parent_model_frame: Flag to interpret the axis xyz element
            in the parent model frame instead of joint frame. Provided
            for Gazebo compatibility (see
            https://github.com/osrf/gazebo/issue/494 ).
        dynamics: An element specifying physical properties of the
            joint. These values are used to specify modeling properties
            of the joint, particularly useful for simulation.
        limit:
        """
        initial_position: List[float] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        xyz: List[str] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
                "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
            }
        )
        use_parent_model_frame: List[bool] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        dynamics: List["JointType.Axis2.Dynamics"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        limit: List["JointType.Axis2.Limit"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
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
            damping: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            friction: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            spring_reference: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            spring_stiffness: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
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
            lower: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            upper: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            effort: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            velocity: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            stiffness: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            dissipation: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
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
            For now, provide_feedback under ode block will override this
            tag and given user warning about the migration.
            provide_feedback under ode is scheduled to be removed in
            SDFormat 1.5.
        """
        simbody: List["JointType.Physics.Simbody"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        ode: List["JointType.Physics.Ode"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        provide_feedback: List[bool] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
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
            must_be_loop_joint: List[bool] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )

        @dataclass
        class Ode:
            """
            ODE specific parameters.

            Parameters
            ----------
            provide_feedback: (DEPRECATION WARNING:  In SDFormat 1.5
                this tag will be replaced by the same tag directly under
                the physics-block.  For now, this tag overrides the one
                outside of ode-block, but in SDFormat 1.5 this tag will
                be removed completely.)  If provide feedback is set to
                true, ODE will compute the constraint forces at this
                joint.
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
            provide_feedback: List[bool] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            cfm_damping: List[bool] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            implicit_spring_damper: List[bool] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            fudge_factor: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            cfm: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            erp: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            bounce: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            max_force: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            velocity: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            limit: List["JointType.Physics.Ode.Limit"] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            suspension: List["JointType.Physics.Ode.Suspension"] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
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
                cfm: List[float] = field(
                    default_factory=list,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    }
                )
                erp: List[float] = field(
                    default_factory=list,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    }
                )

            @dataclass
            class Suspension:
                """
                Parameters
                ----------
                cfm: Suspension constraint force mixing parameter
                erp: Suspension error reduction parameter
                """
                cfm: List[float] = field(
                    default_factory=list,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    }
                )
                erp: List[float] = field(
                    default_factory=list,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    }
                )
