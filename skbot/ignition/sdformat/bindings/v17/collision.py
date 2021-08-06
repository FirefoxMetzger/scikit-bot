from dataclasses import dataclass, field
from typing import Optional
from .geometry import Geometry

__NAMESPACE__ = "sdformat/v1.7/collision.xsd"


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
    pose: A position(x,y,z) and orientation(roll, pitch yaw) with
        respect to the frame named in the relative_to attribute.
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
    pose: "Collision.Pose" = field(
        default="0 0 0 0 0 0",
        metadata={
            "type": "Element",
            "namespace": "",
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
    class Pose:
        """
        Parameters
        ----------
        value:
        relative_to: Name of frame relative to which the pose is
            applied.
        """

        value: Optional[str] = field(
            default=None,
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
            torsional: Parameters for torsional friction
            ode: ODE friction parameters
            bullet:
            """

            torsional: Optional["Collision.Surface.Friction.Torsional"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
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
            class Torsional:
                """
                Parameters for torsional friction.

                Parameters
                ----------
                coefficient: Torsional friction coefficient, unitless
                    maximum ratio of           tangential stress to
                    normal stress.
                use_patch_radius: If this flag is true,
                    torsional friction is calculated using the
                    "patch_radius" parameter.           If this flag is
                    set to false,           "surface_radius" (R) and
                    contact depth (d)           are used to compute the
                    patch radius as sqrt(R*d).
                patch_radius: Radius of contact patch surface.
                surface_radius: Surface radius on the point of contact.
                ode: Torsional friction parameters for ODE
                """

                coefficient: float = field(
                    default=1.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    },
                )
                use_patch_radius: bool = field(
                    default=True,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    },
                )
                patch_radius: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    },
                )
                surface_radius: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    },
                )
                ode: Optional["Collision.Surface.Friction.Torsional.Ode"] = field(
                    default=None,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    },
                )

                @dataclass
                class Ode:
                    """
                    Torsional friction parameters for ODE.

                    Parameters
                    ----------
                    slip: Force dependent slip for torsional friction,
                        equivalent to inverse of viscous damping
                        coefficient             with units of
                        rad/s/(Nm).             A slip value of 0 is
                        infinitely viscous.
                    """

                    slip: float = field(
                        default=0.0,
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
                mu: Coefficient of friction in first friction pyramid
                    direction,           the unitless maximum ratio of
                    force in first friction pyramid           direction
                    to normal force.
                mu2: Coefficient of friction in second friction pyramid
                    direction,           the unitless maximum ratio of
                    force in second friction pyramid           direction
                    to normal force.
                fdir1: Unit vector specifying first friction pyramid
                    direction in           collision-fixed reference
                    frame.           If the friction pyramid model is in
                    use,           and this value is set to a unit
                    vector for one of the           colliding surfaces,
                    the ODE Collide callback function will align the
                    friction pyramid directions           with a
                    reference frame fixed to that collision surface.
                    If both surfaces have this value set to a vector of
                    zeros,           the friction pyramid directions
                    will be aligned with the world frame.           If
                    this value is set for both surfaces, the behavior is
                    undefined.
                slip1: Force dependent slip in first friction pyramid
                    direction,           equivalent to inverse of
                    viscous damping coefficient           with units of
                    m/s/N.           A slip value of 0 is infinitely
                    viscous.
                slip2: Force dependent slip in second friction pyramid
                    direction,           equivalent to inverse of
                    viscous damping coefficient           with units of
                    m/s/N.           A slip value of 0 is infinitely
                    viscous.
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
                friction: Coefficient of friction in first friction
                    pyramid direction,           the unitless maximum
                    ratio of force in first friction pyramid
                    direction to normal force.
                friction2: Coefficient of friction in second friction
                    pyramid direction,           the unitless maximum
                    ratio of force in second friction pyramid
                    direction to normal force.
                fdir1: Unit vector specifying first friction pyramid
                    direction in           collision-fixed reference
                    frame.           If the friction pyramid model is in
                    use,           and this value is set to a unit
                    vector for one of the           colliding surfaces,
                    the friction pyramid directions will be aligned
                    with a reference frame fixed to that collision
                    surface.           If both surfaces have this value
                    set to a vector of zeros,           the friction
                    pyramid directions will be aligned with the world
                    frame.           If this value is set for both
                    surfaces, the behavior is undefined.
                rolling_friction: Coefficient of rolling friction
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
            category_bitmask: Bitmask for category of collision
                filtering. Collision happens if ((category1 &amp;
                collision2) | (category2 &amp; collision1)) is not zero.
                If not specified, the category_bitmask should be
                interpreted as being the same as collide_bitmask. Parsed
                as 16-bit unsigned integer.
            poissons_ratio: Poisson's ratio is the unitless ratio
                between transverse and axial strain.         This value
                must lie between (-1, 0.5).  Defaults to 0.3 for typical
                steel.         Note typical silicone elastomers have
                Poisson's ratio near 0.49 ~ 0.50.          For
                reference, approximate values for Material:(Young's
                Modulus, Poisson's Ratio)         for some of the
                typical materials are:           Plastic:  (1e8 ~ 3e9
                Pa,  0.35 ~ 0.41),           Wood:     (4e9 ~ 1e10 Pa,
                0.22 ~ 0.50),           Aluminum: (7e10 Pa,       0.32 ~
                0.35),           Steel:    (2e11 Pa,       0.26 ~ 0.31).
            elastic_modulus: Young's Modulus in SI derived unit Pascal.
                Defaults to -1.  If value is less or equal to zero,
                contact using elastic modulus (with Poisson's Ratio) is
                disabled.          For reference, approximate values for
                Material:(Young's Modulus, Poisson's Ratio)         for
                some of the typical materials are:           Plastic:
                (1e8 ~ 3e9 Pa,  0.35 ~ 0.41),           Wood:     (4e9 ~
                1e10 Pa, 0.22 ~ 0.50),           Aluminum: (7e10 Pa,
                0.32 ~ 0.35),           Steel:    (2e11 Pa,       0.26 ~
                0.31).
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
                default=65535,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            category_bitmask: int = field(
                default=65535,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            poissons_ratio: float = field(
                default=0.3,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            elastic_modulus: float = field(
                default=-1.0,
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
