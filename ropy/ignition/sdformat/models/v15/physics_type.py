from dataclasses import dataclass, field
from typing import List, Optional

__NAMESPACE__ = "sdformat/physics"


@dataclass
class PhysicsType:
    """
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
    gravity: The gravity vector in m/s^2, expressed in a coordinate
        frame defined by the spherical_coordinates tag.
    magnetic_field: The magnetic vector in Tesla, expressed in a
        coordinate frame defined by the spherical_coordinates tag.
    simbody: Simbody specific physics properties
    bullet: Bullet specific physics properties
    ode: ODE specific physics properties
    name: The name of this set of physics parameters.
    default: If true, this physics element is set as the default physics
        profile for the world. If multiple default physics elements
        exist, the first element marked as default is chosen. If no
        default physics element exists, the first physics element is
        chosen.
    type: The type of the dynamics engine. Current options are ode,
        bullet, simbody and rtql8.  Defaults to ode if left unspecified.
    """

    class Meta:
        name = "physicsType"

    max_step_size: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    real_time_factor: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    real_time_update_rate: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    max_contacts: List[int] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    gravity: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
            "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
        },
    )
    magnetic_field: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
            "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
        },
    )
    simbody: List["PhysicsType.Simbody"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    bullet: List["PhysicsType.Bullet"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    ode: List["PhysicsType.Ode"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    name: str = field(
        default="default_physics",
        metadata={
            "type": "Attribute",
        },
    )
    default: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
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
            solver when static friction is supposed to hold object in
            place.
        contact: Relationship among dissipation, coef. restitution, etc.
            d = dissipation coefficient (1/velocity) vc = capture
            velocity (velocity where e=e_max) vp = plastic velocity
            (smallest v where e=e_min) &gt; vc Assume real COR=1 when
            v=0. e_min = given minimum COR, at v &gt;= vp (a.k.a.
            plastic_coef_restitution) d = slope = (1-e_min)/vp OR, e_min
            = 1 - d*vp e_max = maximum COR = 1-d*vc, reached at v=vc e =
            0,                       v &lt;= vc = 1 - d*v,
            vc &lt; v &lt; vp = e_min,                   v &gt;= vp
            dissipation factor = d*min(v,vp)   [compliant] cor = e
            [rigid] Combining rule e = 0,               e1==e2==0 =
            2*e1*e2/(e1+e2), otherwise
        """

        min_step_size: List[float] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        accuracy: List[float] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        max_transient_velocity: List[float] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        contact: List["PhysicsType.Simbody.Contact"] = field(
            default_factory=list,
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
            stiffness: Default contact material stiffness (force/dist or
                torque/radian).
            dissipation: dissipation coefficient to be used in compliant
                contact; if not given it is
                (1-min_cor)/plastic_impact_velocity
            plastic_coef_restitution: this is the COR to be used at high
                velocities for rigid impacts; if not given it is 1 -
                dissipation*plastic_impact_velocity
            plastic_impact_velocity: smallest impact velocity at which
                min COR is reached; set to zero if you want the min COR
                always to be used
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
                impact velocity at which COR is set to zero; normally
                inherited from global default but can be overridden
                here. Combining rule: use larger velocity
            override_stiction_transition_velocity: This is the largest
                slip velocity at which we'll consider a transition to
                stiction. Normally inherited from a global default
                setting. For a continuous friction model this is the
                velocity at which the max static friction force is
                reached.  Combining rule: use larger velocity
            """

            stiffness: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            dissipation: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            plastic_coef_restitution: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            plastic_impact_velocity: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            static_friction: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            dynamic_friction: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            viscous_friction: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            override_impact_capture_velocity: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            override_stiction_transition_velocity: List[float] = field(
                default_factory=list,
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
        solver:
        constraints: Bullet constraint parameters.
        """

        solver: List["PhysicsType.Bullet.Solver"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        constraints: List["PhysicsType.Bullet.Constraints"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
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

            type: List[str] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            min_step_size: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            iters: List[int] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            sor: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
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

            cfm: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            erp: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            contact_surface_layer: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            split_impulse: List[bool] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            split_impulse_penetration_threshold: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

    @dataclass
    class Ode:
        """
        Parameters
        ----------
        solver:
        constraints: ODE constraint parameters.
        """

        solver: List["PhysicsType.Ode.Solver"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        constraints: List["PhysicsType.Ode.Constraints"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
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
                of moment of inertia in constrained directions. See
                gazebo pull request 1114 for the implementation of this
                feature. https://osrf-migration.github.io/gazebo-gh-
                pages/#!/osrf/gazebo/pull-request/1114
            """

            type: List[str] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            min_step_size: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            iters: List[int] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            precon_iters: List[int] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            sor: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            use_dynamic_moi_rescaling: List[bool] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
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

            cfm: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            erp: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            contact_max_correcting_vel: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            contact_surface_layer: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
