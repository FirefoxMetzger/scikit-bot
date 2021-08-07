from dataclasses import dataclass, field
from typing import Optional
from .geometry import Geometry

__NAMESPACE__ = "sdformat/v1.4/collision.xsd"


@dataclass
class Collision:
    """The collision properties of a link.

    Note that this can be different from the visual properties of a
    link, for example, simpler collision models are often used to reduce
    computation time.

    Parameters
    ----------
    laser_retro: intensity value returned by laser sensor.
    max_contacts: Maximum number of contacts allowed between two
        entities. This value overrides the max_contacts element defined
        in physics.
    pose: The reference frame of the collision element, relative to the
        reference frame of the link.
    geometry: The shape of the visual or collision object.
    surface: The surface parameters
    name: Unique name for the collision element within the scope of the
        parent link.
    """

    class Meta:
        name = "collision"

    laser_retro: float = field(
        default=0.0,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    max_contacts: int = field(
        default=10,
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
    geometry: Optional[Geometry] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    surface: Optional["Collision.Surface"] = field(
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

    @dataclass
    class Surface:
        """
        The surface parameters.
        """

        bounce: Optional["Collision.Surface.Bounce"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        friction: Optional["Collision.Surface.Friction"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        contact: Optional["Collision.Surface.Contact"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        soft_contact: Optional["Collision.Surface.SoftContact"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

        @dataclass
        class Bounce:
            """
            Parameters
            ----------
            restitution_coefficient: Bounciness coefficient of
                restitution, from [0...1], where 0=no bounciness.
            threshold: Bounce capture velocity, below which effective
                coefficient of restitution is 0.
            """

            restitution_coefficient: float = field(
                default=0.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            threshold: float = field(
                default=100000.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

        @dataclass
        class Friction:
            """
            Parameters
            ----------
            ode: ODE friction parameters
            bullet:
            """

            ode: Optional["Collision.Surface.Friction.Ode"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            bullet: Optional["Collision.Surface.Friction.Bullet"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Ode:
                """
                ODE friction parameters.

                Parameters
                ----------
                mu: Coefficient of friction in the range of [0..1].
                mu2: Second coefficient of friction in the range of
                    [0..1]
                fdir1: 3-tuple specifying direction of mu1 in the
                    collision local reference frame.
                slip1: Force dependent slip direction 1 in collision
                    local frame, between the range of [0..1].
                slip2: Force dependent slip direction 2 in collision
                    local frame, between the range of [0..1].
                """

                mu: float = field(
                    default=1.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    },
                )
                mu2: float = field(
                    default=1.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    },
                )
                fdir1: str = field(
                    default="0 0 0",
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
                    },
                )
                slip1: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    },
                )
                slip2: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    },
                )

            @dataclass
            class Bullet:
                """
                Parameters
                ----------
                friction: Coefficient of friction in the range of
                    [0..1].
                friction2: Coefficient of friction in the range of
                    [0..1].
                fdir1: 3-tuple specifying direction of mu1 in the
                    collision local reference frame.
                rolling_friction: coefficient of friction in the range
                    of [0..1]
                """

                friction: float = field(
                    default=1.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    },
                )
                friction2: float = field(
                    default=1.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    },
                )
                fdir1: str = field(
                    default="0 0 0",
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
                    },
                )
                rolling_friction: float = field(
                    default=1.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    },
                )

        @dataclass
        class Contact:
            """
            Parameters
            ----------
            collide_without_contact: Flag to disable contact force
                generation, while still allowing collision checks and
                contact visualization to occur.
            collide_without_contact_bitmask: Bitmask for collision
                filtering when collide_without_contact is on
            collide_bitmask: Bitmask for collision filtering. This will
                override collide_without_contact. Parsed as 16-bit
                unsigned integer.
            ode: ODE contact parameters
            bullet: Bullet contact parameters
            """

            collide_without_contact: bool = field(
                default=False,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            collide_without_contact_bitmask: int = field(
                default=1,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            collide_bitmask: int = field(
                default=1,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            ode: Optional["Collision.Surface.Contact.Ode"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            bullet: Optional["Collision.Surface.Contact.Bullet"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Ode:
                """
                ODE contact parameters.

                Parameters
                ----------
                soft_cfm: Soft constraint force mixing.
                soft_erp: Soft error reduction parameter
                kp: dynamically "stiffness"-equivalent coefficient for
                    contact joints
                kd: dynamically "damping"-equivalent coefficient for
                    contact joints
                max_vel: maximum contact correction velocity truncation
                    term.
                min_depth: minimum allowable depth before contact
                    correction impulse is applied
                """

                soft_cfm: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    },
                )
                soft_erp: float = field(
                    default=0.2,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    },
                )
                kp: float = field(
                    default=1000000000000.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    },
                )
                kd: float = field(
                    default=1.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    },
                )
                max_vel: float = field(
                    default=0.01,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    },
                )
                min_depth: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    },
                )

            @dataclass
            class Bullet:
                """
                Bullet contact parameters.

                Parameters
                ----------
                soft_cfm: Soft constraint force mixing.
                soft_erp: Soft error reduction parameter
                kp: dynamically "stiffness"-equivalent coefficient for
                    contact joints
                kd: dynamically "damping"-equivalent coefficient for
                    contact joints
                split_impulse: Similar to ODE's max_vel implementation.
                    See
                    http://bulletphysics.org/mediawiki-1.5.8/index.php/BtContactSolverInfo#Split_Impulse
                    for more information.
                split_impulse_penetration_threshold: Similar to ODE's
                    max_vel implementation.  See
                    http://bulletphysics.org/mediawiki-1.5.8/index.php/BtContactSolverInfo#Split_Impulse
                    for more information.
                """

                soft_cfm: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    },
                )
                soft_erp: float = field(
                    default=0.2,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    },
                )
                kp: float = field(
                    default=1000000000000.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    },
                )
                kd: float = field(
                    default=1.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    },
                )
                split_impulse: bool = field(
                    default=True,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    },
                )
                split_impulse_penetration_threshold: float = field(
                    default=-0.01,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    },
                )

        @dataclass
        class SoftContact:
            """
            Parameters
            ----------
            dart: soft contact pamameters based on paper:
                http://www.cc.gatech.edu/graphics/projects/Sumit/homepage/papers/sigasia11/jain_softcontacts_siga11.pdf
            """

            dart: Optional["Collision.Surface.SoftContact.Dart"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Dart:
                """
                soft contact pamameters based on paper:              http://www
                .cc.gatech.edu/graphics/projects/Sumit/homepage/papers/sigasia1
                1/jain_softcontacts_siga11.pdf.

                Parameters
                ----------
                bone_attachment: This is variable k_v in the soft
                    contacts paper.  Its unit is N/m.
                stiffness: This is variable k_e in the soft contacts
                    paper.  Its unit is N/m.
                damping: Viscous damping of point velocity in body
                    frame.  Its unit is N/m/s.
                flesh_mass_fraction: Fraction of mass to be distributed
                    among deformable nodes.
                """

                bone_attachment: float = field(
                    default=100.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    },
                )
                stiffness: float = field(
                    default=100.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    },
                )
                damping: float = field(
                    default=10.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    },
                )
                flesh_mass_fraction: float = field(
                    default=0.05,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    },
                )
