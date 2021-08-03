from dataclasses import dataclass, field
from typing import Optional

__NAMESPACE__ = "sdformat/v1.3/physics.xsd"


@dataclass
class Physics:
    """
    The physics tag specifies the type and properties of the dynamics engine.

    Parameters
    ----------
    update_rate: Rate at which to update the physics engine
    max_contacts: Maximum number of contacts allowed between two
        entities. This value can be over ridden by a max_contacts
        element in a collision element.
    gravity: The gravity vector
    bullet: Bullet specific physics properties
    ode: ODE specific physics properties
    type: The type of the dynamics engine. Currently must be set to ode
    """
    class Meta:
        name = "physics"

    update_rate: Optional[float] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    max_contacts: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    gravity: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
            "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
        }
    )
    bullet: Optional["Physics.Bullet"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    ode: Optional["Physics.Ode"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
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
    class Bullet:
        """
        Bullet specific physics properties.

        Parameters
        ----------
        dt: Time step
        """
        dt: Optional[float] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            }
        )

    @dataclass
    class Ode:
        """
        ODE specific physics properties.
        """
        solver: Optional["Physics.Ode.Solver"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            }
        )
        constraints: Optional["Physics.Ode.Constraints"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            }
        )

        @dataclass
        class Solver:
            """
            Parameters
            ----------
            type: One of the following types: world, quick
            dt: The time duration which advances with each iteration of
                the dynamics engine.
            iters: Number of iterations for each step. A higher number
                produces greater accuracy at a performance cost.
            precon_iters:
            sor: Set the successive over-relaxation parameter.
            """
            type: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                }
            )
            dt: Optional[float] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                }
            )
            iters: Optional[int] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                }
            )
            precon_iters: Optional[int] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            sor: Optional[float] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                }
            )

        @dataclass
        class Constraints:
            """
            Parameters
            ----------
            cfm: Constraint force mixing parameter. See the ODE page for
                more information.
            erp: Error reduction parameter. See the ODE page for more
                information.
            contact_max_correcting_vel: The maximum correcting
                velocities allowed when resolving contacts.
            contact_surface_layer: The depth of the surface layer around
                all geometry objects. Contacts are allowed to sink into
                the surface layer up to the given depth before coming to
                rest. The default value is zero. Increasing this to some
                small value (e.g. 0.001) can help prevent jittering
                problems due to contacts being repeatedly made and
                broken.
            """
            cfm: Optional[float] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                }
            )
            erp: Optional[float] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                }
            )
            contact_max_correcting_vel: Optional[float] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                }
            )
            contact_surface_layer: Optional[float] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                }
            )
