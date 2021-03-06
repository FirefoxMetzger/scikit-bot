from dataclasses import dataclass, field
from typing import Optional

__NAMESPACE__ = "sdformat/v1.4/physics.xsd"


@dataclass
class Physics:
    """
    The physics tag specifies the type and properties of the dynamics engine.

    Parameters
    ----------
    max_step_size: Maximum time step size at which every system in
        simulation can interact with the states of the world.  (was
        physics.sdf's dt).
    real_time_factor: target simulation speedup factor, defined by ratio
        of simulation time to real-time.
    real_time_update_rate: Rate at which to update the physics engine
        (UpdatePhysics calls per real-time second). (was physics.sdf's
        update_rate).
    max_contacts: Maximum number of contacts allowed between two
        entities. This value can be over ridden by a max_contacts
        element in a collision element.
    gravity: The gravity vector
    simbody: Simbody specific physics properties
    bullet: Bullet specific physics properties
    ode: ODE specific physics properties
    type: The type of the dynamics engine. Current options are ode,
        bullet, simbody and rtql8.  Defaults to ode if left unspecified.
    """

    class Meta:
        name = "physics"

    max_step_size: float = field(
        default=0.001,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    real_time_factor: float = field(
        default=1.0,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    real_time_update_rate: float = field(
        default=1000.0,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    max_contacts: int = field(
        default=20,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    gravity: str = field(
        default="0 0 -9.8",
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
            "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
        },
    )
    simbody: Optional["Physics.Simbody"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    bullet: Optional["Physics.Bullet"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    ode: Optional["Physics.Ode"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
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
    class Simbody:
        """
        Simbody specific physics properties.

        Parameters
        ----------
        min_step_size: (Currently not used in simbody) The time duration
            which advances with each iteration of the dynamics engine,
            this has to be no bigger than max_step_size under physics
            block.  If left unspecified, min_step_size defaults to
            max_step_size.
        accuracy: Roughly the relative error of the system.
            -LOG(accuracy) is roughly the number of significant digits.
        max_transient_velocity: Tolerable "slip" velocity allowed by the
            solver when static         friction is supposed to hold
            object in place.
        contact: Relationship among dissipation, coef. restitution, etc.
            d = dissipation coefficient (1/velocity)         vc =
            capture velocity (velocity where e=e_max)         vp =
            plastic velocity (smallest v where e=e_min) &amp;gt; vc
            Assume real COR=1 when v=0.         e_min = given minimum
            COR, at v &amp;gt;= vp (a.k.a. plastic_coef_restitution)
            d = slope = (1-e_min)/vp         OR, e_min = 1 - d*vp
            e_max = maximum COR = 1-d*vc, reached at v=vc         e = 0,
            v &amp;lt;= vc           = 1 - d*v,               vc
            &amp;lt; v &amp;lt; vp           = e_min,
            v &amp;gt;= vp          dissipation factor = d*min(v,vp)
            [compliant]         cor = e
            [rigid]          Combining rule e = 0,
            e1==e2==0                          = 2*e1*e2/(e1+e2),
            otherwise
        """

        min_step_size: float = field(
            default=0.0001,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        accuracy: float = field(
            default=0.001,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        max_transient_velocity: float = field(
            default=0.01,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        contact: Optional["Physics.Simbody.Contact"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

        @dataclass
        class Contact:
            """Relationship among dissipation, coef.

            restitution, etc.         d = dissipation coefficient (1/velocity)         vc = capture velocity (velocity where e=e_max)         vp = plastic velocity (smallest v where e=e_min) &amp;gt; vc         Assume real COR=1 when v=0.         e_min = given minimum COR, at v &amp;gt;= vp (a.k.a. plastic_coef_restitution)         d = slope = (1-e_min)/vp         OR, e_min = 1 - d*vp         e_max = maximum COR = 1-d*vc, reached at v=vc         e = 0,                       v &amp;lt;= vc           = 1 - d*v,               vc &amp;lt; v &amp;lt; vp           = e_min,                   v &amp;gt;= vp          dissipation factor = d*min(v,vp)   [compliant]         cor = e                            [rigid]          Combining rule e = 0,               e1==e2==0                          = 2*e1*e2/(e1+e2), otherwise

            Parameters
            ----------
            stiffness: Default contact material stiffness
                (force/dist or torque/radian).
            dissipation: dissipation coefficient to be used in compliant
                contact;     if not given it is
                (1-min_cor)/plastic_impact_velocity
            plastic_coef_restitution: this is the COR to be used at high
                velocities for rigid     impacts; if not given it is 1 -
                dissipation*plastic_impact_velocity
            plastic_impact_velocity: smallest impact velocity at which
                min COR is reached; set       to zero if you want the
                min COR always to be used
            static_friction: static friction (mu_s) as described by this
                plot:
                http://gazebosim.org/wiki/File:Stribeck_friction.png
            dynamic_friction: dynamic friction (mu_d) as described by
                this plot:
                http://gazebosim.org/wiki/File:Stribeck_friction.png
            viscous_friction: viscous friction (mu_v) with units of
                (1/velocity) as described by this plot:
                http://gazebosim.org/wiki/File:Stribeck_friction.png
            override_impact_capture_velocity: for rigid impacts only,
                impact velocity at which           COR is set to zero;
                normally inherited from global default but can
                be overridden here. Combining rule: use larger velocity
            override_stiction_transition_velocity: This is the largest
                slip velocity at which            we'll consider a
                transition to stiction. Normally inherited
                from a global default setting. For a continuous friction
                model            this is the velocity at which the max
                static friction force            is reached.  Combining
                rule: use larger velocity
            """

            stiffness: float = field(
                default=100000000.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            dissipation: float = field(
                default=100.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            plastic_coef_restitution: float = field(
                default=0.5,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            plastic_impact_velocity: float = field(
                default=0.5,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            static_friction: float = field(
                default=0.9,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            dynamic_friction: float = field(
                default=0.9,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            viscous_friction: float = field(
                default=0.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            override_impact_capture_velocity: float = field(
                default=0.001,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            override_stiction_transition_velocity: float = field(
                default=0.001,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )

    @dataclass
    class Bullet:
        """
        Bullet specific physics properties.

        Parameters
        ----------
        solver:
        constraints: Bullet constraint parameters.
        """

        solver: Optional["Physics.Bullet.Solver"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        constraints: Optional["Physics.Bullet.Constraints"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )

        @dataclass
        class Solver:
            """
            Parameters
            ----------
            type: One of the following types: sequential_impulse only.
            min_step_size: The time duration which advances with each
                iteration of the dynamics engine, this has to be no
                bigger than max_step_size under physics block.  If left
                unspecified, min_step_size defaults to max_step_size.
            iters: Number of iterations for each step. A higher number
                produces greater accuracy at a performance cost.
            sor: Set the successive over-relaxation parameter.
            """

            type: str = field(
                default="sequential_impulse",
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            min_step_size: float = field(
                default=0.0001,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            iters: int = field(
                default=50,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            sor: float = field(
                default=1.3,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )

        @dataclass
        class Constraints:
            """
            Bullet constraint parameters.

            Parameters
            ----------
            cfm: Constraint force mixing parameter. See the ODE page for
                more information.
            erp: Error reduction parameter. See the ODE page for more
                information.
            contact_surface_layer: The depth of the surface layer around
                all geometry objects. Contacts are allowed to sink into
                the surface layer up to the given depth before coming to
                rest. The default value is zero. Increasing this to some
                small value (e.g. 0.001) can help prevent jittering
                problems due to contacts being repeatedly made and
                broken.
            split_impulse: Similar to ODE's max_vel implementation. See
                http://web.archive.org/web/20120430155635/http://bulletphysics.org/mediawiki-1.5.8/index.php/BtContactSolverInfo#Split_Impulse
                for more information.
            split_impulse_penetration_threshold: Similar to ODE's
                max_vel implementation.  See
                http://web.archive.org/web/20120430155635/http://bulletphysics.org/mediawiki-1.5.8/index.php/BtContactSolverInfo#Split_Impulse
                for more information.
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
            contact_surface_layer: float = field(
                default=0.001,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            split_impulse: bool = field(
                default=True,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            split_impulse_penetration_threshold: float = field(
                default=-0.01,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )

    @dataclass
    class Ode:
        """
        ODE specific physics properties.

        Parameters
        ----------
        solver:
        constraints: ODE constraint parameters.
        """

        solver: Optional["Physics.Ode.Solver"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        constraints: Optional["Physics.Ode.Constraints"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )

        @dataclass
        class Solver:
            """
            Parameters
            ----------
            type: One of the following types: world, quick
            min_step_size: The time duration which advances with each
                iteration of the dynamics engine, this has to be no
                bigger than max_step_size under physics block.  If left
                unspecified, min_step_size defaults to max_step_size.
            iters: Number of iterations for each step. A higher number
                produces greater accuracy at a performance cost.
            precon_iters: Experimental parameter.
            sor: Set the successive over-relaxation parameter.
            use_dynamic_moi_rescaling: Flag to enable dynamic rescaling
                of moment of inertia in constrained directions.
                See gazebo pull request 1114 for the implementation of
                this feature.           https://osrf-
                migration.github.io/gazebo-gh-pages/#!/osrf/gazebo/pull-
                request/1114
            """

            type: str = field(
                default="quick",
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            min_step_size: float = field(
                default=0.0001,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            iters: int = field(
                default=50,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            precon_iters: int = field(
                default=0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            sor: float = field(
                default=1.3,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            use_dynamic_moi_rescaling: bool = field(
                default=False,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )

        @dataclass
        class Constraints:
            """
            ODE constraint parameters.

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
            contact_max_correcting_vel: float = field(
                default=100.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            contact_surface_layer: float = field(
                default=0.001,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
