import warnings
from typing import List, Union, Dict, Any, Tuple
from itertools import chain

from .base import ElementBase, FloatElement, Pose, StringElement
from .sensor import Sensor
from .frame import Frame
from .origin import Origin
from .... import transform as tf


class Joint(ElementBase):
    """A constraint between two rigid bodys.

    A joint connects two links with kinematic and dynamic properties. This
    defines a constraint between the two bodies, and constructing a
    :mod``transform graph <skbot.transform>`` using ``to_dynamic_graph`` will
    build this constraint into the underlying graph structure.

    Parameters
    ----------
    name : str
        The name of the joint.
    type : str
        The type of joint, which must be one of the following:
            continuous
                A hinge joint that rotates around :class:``Joint.Axis``with a
                continuous range of motion.  This means that the upper
                and lower axis limits are ignored.
            revolute
                a hinge joint that rotates around :class:``Joint.Axis`` with
                a fixed range of motion.
            gearbox
                A geared revolute joints.
            revolute2
                Two revolute joints connected in series. The first one rotates
                around :class:``Joint.Axis``, and the second one rotates around
                :class:``Joint.Axis2``.
            prismatic
                A sliding joint that slides along :class:``Joint.Axis`` with a
                limited range of motion.
            ball
                A ball and socket joint.
            screw
                A 1DoF joint with coupled sliding and rotational motion.
            universal
                Like a joint with type ``ball`` but constrains one degree of
                freedom.
            fixed
                A joint with zero DoF that rigidly connects two links.
    parent : Union[str, Joint.Parent]
        The first :class:`Link` that this joint constraints. It may be set to
        "world", in which case the movement of the rigid body in ``Joint.child``
        is constrained relative to the inertial world frame.

        .. versionchanged:: SDFormat v1.7
            Parent may now be set to "world" and, if so, will connect
            to the inertial world frame.
        .. versionchanged:: SDFormat v1.2
            Parent is now a string instead of :class:`Joint.Parent`.
    child : Union[str, Joint.Child]
        The second :class:`Link` that this joint constraints.

        .. versionchanged:: SDFormat v1.2
            Child is now a string instead of :class:`Joint.Child`.
    pose : Pose
        The links's initial position (x,y,z) and orientation (roll, pitch, yaw).

        .. versionadded:: SDFormat 1.2
    gearbox_ratio : float
        Parameter for gearbox joints. Given theta_1 and theta_2 defined in
        description for gearbox_reference_body, ``theta_2 = -gearbox_ratio *
        theta_1``. Default: 1.0

        .. versionadded:: SDFormat v1.4
    gearbox_reference_body : str
        Parameter for gearbox joints. Gearbox ratio is enforced over two joint
        angles. First joint angle (theta_1) is the angle from the
        gearbox_reference_body to the parent link defined by :class:`Joint.Axis`
        and the second joint angle (theta_2) is the angle from the
        gearbox_reference_body to the child link defined by
        :class:`Joint.Axis2`.

        .. versionadded:: SDFormat v1.4
    thread_pitch : float
        Parameter for screw joints. The amount of linear displacement for each
        full rotation of the joint.
    axis : Joint.Axis
        Configuration parameters for joints that rotate around or translate
        along at least one axis.
    axis2 : Joint.Axis2
        Configuration parameters for joints that rotate around or translate
        along at least two axis.
    physics : Joint.Physics
        Configuration parameters for various physics engines. (Currently: ODE
        and Simbody.)
    frames : List[Frame]
        A list of frames of reference in which poses may be expressed.

        .. depreciated:: SDFormat v1.7
            Use :attr:`Model.frame` instead.
        .. versionadded:: SDFormat v1.5
    sensors : List[Sensor]
        A list of sensors attached to this joint.

        .. versionadded:: SDFormat v1.4
    sdf_version : str
        The SDFormat version to use when constructing this element.
    origin : Origin
        The joint's origin.

        .. depreciated:: SDFormat v1.2
            Use ``Joint.pose`` instead.

    Attributes
    ----------
    name : str
        See ``Parameters`` section.
    type : str
        See ``Parameters`` section.
    parent : Union[str, Joint.Parent]
        See ``Parameters`` section.
    child : Union[str, Joint.Child]
        See ``Parameters`` section.
    pose : Pose
        See ``Parameters`` section.
    gearbox_ratio : float
        See ``Parameters`` section.
    gearbox_reference_body : str
        See ``Parameters`` section.
    thread_pitch : float
        See ``Parameters`` section.
    axis : Joint.Axis
        See ``Parameters`` section.
    axis2 : Joint.Axis2
        See ``Parameters`` section.
    physics : Joint.Physics
        See ``Parameters`` section.
    frames : List[Frame]
        See ``Parameters`` section.
    sensors : List[Sensor]
        See ``Parameters`` section.
    sdf_version : str
        See ``Parameters`` section.
    origin : Origin
        See ``Parameters`` section.

    Notes
    -----
    A joint defines an implicit frame of reference to which other
    :class:`Frame`s may be ``attached_to``. As such its name must be unique
    among all frames and frame-bearing elements.

    """

    def __init__(
        self,
        *,
        name: str,
        type: str,
        parent: Union[str, "Joint.Parent"],
        child: Union[str, "Joint.Child"],
        origin: Origin = None,
        pose: Pose = None,
        gearbox_ratio: float = 1.0,
        gearbox_reference_body: str = None,
        thread_pitch: float = 1.0,
        axis: "Joint.Axis" = None,
        axis2: "Joint.Axis2" = None,
        physics: "Joint.Physics" = None,
        frames: List[Frame] = None,
        sensors: List[Sensor] = None,
        sdf_version: str,
    ) -> None:
        super().__init__(sdf_version=sdf_version)
        self.name = name
        self.type = type
        self.parent = parent
        self.child = child
        if origin is None:
            self._origin = Origin(sdf_version=sdf_version)
        elif sdf_version == "1.0":
            self._origin = origin
        else:
            warnings.warn("`origin` is depreciated. Use `pose` instead.")
            self._origin = origin
        if sdf_version == "1.0":
            self.pose = self._origin.pose
        elif pose is None:
            self.pose = Pose(sdf_version=sdf_version)
        else:
            self.pose = pose
        self.gearbox_ratio = gearbox_ratio
        self.gearbox_reference_body = gearbox_reference_body
        self.thread_pitch = thread_pitch
        self.axis = Joint.Axis() if axis is None else axis
        self.axis2 = Joint.Axis2() if axis2 is None else axis2
        self.physics = (
            Joint.Physics() if physics is None else physics
        )  #: "Joint.Physics" = None,
        self._frames = [] if frames is None else frames
        self.sensors = [] if sensors is None else sensors

        self._origin.pose = self.pose

    @property
    def origin(self):
        warnings.warn(
            "`Joint.origin` is depreciated since SDFormat v1.2."
            " Use `Joint.pose` instead.",
            DeprecationWarning,
        )
        return self._origin

    @property
    def frames(self):
        warnings.warn(
            "`Link.frames` is depreciated since SDF v1.7."
            " Use `Model.frames` instead and set `Frame.attached_to`"
            " to the name of this joint.",
            DeprecationWarning,
        )
        return self._frames

    @classmethod
    def from_specific(cls, specific: Any, *, version: str) -> "ElementBase":
        joint_args = {
            "name": specific.name,
            "type": specific.type,
            "parent": specific.parent,
            "child": specific.child,
        }
        args_with_default = {
            "origin": Origin,
            "pose": Pose,
            "gearbox_ratio": FloatElement,
            "gearbox_reference_body": StringElement,
            "thread_pitch": FloatElement,
            "axis": Joint.Axis,
            "axis2": Joint.Axis2,
            "physics": Joint.Physics,
        }
        list_args = {"frame": ("frames", Frame), "sensor": ("sensors", Sensor)}
        standard_args = cls._prepare_standard_args(
            specific, args_with_default, list_args, version=version
        )
        joint_args.update(standard_args)

        return Joint(**joint_args, sdf_version=version)

    def declared_frames(self) -> Dict[str, tf.Frame]:
        joint_frame = tf.Frame(3, name=self.name)
        declared_frames = {
            self.name: joint_frame,
            self.name + "_child": joint_frame,
            self.name + "_parent": tf.Frame(3, name=self.name + "_parent"),
        }

        for el in chain(self._frames):
            declared_frames.update(el.declared_frames())

        return declared_frames

    def to_static_graph(
        self,
        declared_frames: Dict[str, tf.Frame],
        *,
        seed: int = None,
        shape: Tuple,
        axis: int = -1,
    ) -> tf.Frame:
        parent_name = self.pose.relative_to
        child_name = self.name

        parent = declared_frames[parent_name]
        child = declared_frames[child_name]

        link = self.pose.to_tf_link()
        link(child, parent)

        for el in chain(self._frames):
            el.to_static_graph(declared_frames, seed=seed, shape=shape, axis=axis)

        return declared_frames[self.name]

    def to_dynamic_graph(
        self,
        declared_frames: Dict[str, tf.Frame],
        *,
        seed: int = None,
        shape: Tuple,
        axis: int = -1,
        apply_state: bool = True,
        _scaffolding: Dict[str, tf.Frame],
    ) -> tf.Frame:
        parent_name = self.parent
        child_name = self.child
        joint_name = self.name
        joint_name_parent = self.name + "_parent"

        parent = declared_frames[parent_name]
        joint_parent = declared_frames[joint_name_parent]
        joint_child = declared_frames[joint_name]
        child = declared_frames[child_name]

        parent_static = _scaffolding[parent_name]
        joint_static = _scaffolding[joint_name]
        child_static = _scaffolding[child_name]

        link = tf.CompundLink(parent_static.transform_chain(joint_static))
        link(parent, joint_parent)

        joint_link: tf.Link = self.to_tf_link()
        joint_link(joint_parent, joint_child)

        link = tf.CompundLink(joint_static.transform_chain(child_static))
        link(joint_child, child)

        for el in chain(self._frames):
            el.to_dynamic_graph(
                declared_frames,
                seed=seed,
                shape=shape,
                axis=axis,
                apply_state=apply_state,
                _scaffolding=_scaffolding,
            )

        return declared_frames[self.name]

    def to_tf_link(self):
        pass

    class Parent(ElementBase):
        def __init__(self, *, link: str, sdf_version: str) -> None:
            super().__init__(sdf_version=sdf_version)
            self.link = link

        @classmethod
        def from_specific(cls, specific: Any, *, version: str) -> "ElementBase":
            return Joint.Parent(link=specific.link, version=version)

    class Child(ElementBase):
        def __init__(self, *, link: str, sdf_version: str) -> None:
            super().__init__(sdf_version=sdf_version)
            self.link = link

        @classmethod
        def from_specific(cls, specific: Any, *, version: str) -> "ElementBase":
            return Joint.Parent(link=specific.link, version=version)

    class Axis(ElementBase):
        """
          <element name="axis" required="0">
          <description>
            Parameters related to the axis of rotation for revolute joints,
            the axis of translation for prismatic joints.
          </description>
          <element name="initial_position" type="double" default="0" required="-1">
            <description>
              (DEPRECATION WARNING: This tag has no known implementation. It is deprecated SDFormat 1.8 and will be removed in SDFormat 1.9) Default joint position for this joint axis.
            </description>
          </element>
          <element name="xyz" type="vector3" default="0 0 1" required="1">
            <description>
              Represents the x,y,z components of the axis unit vector. The axis is
              expressed in the joint frame unless a different frame is expressed in
              the expressed_in attribute. The vector should be normalized.
            </description>
            <attribute name="expressed_in" type="string" default="" required="0">
              <description>
                Name of frame in whose coordinates the xyz unit vector is expressed.
              </description>
            </attribute>
          </element>
          <element name="dynamics" required="0">
            <description>An element specifying physical properties of the joint. These values are used to specify modeling properties of the joint, particularly useful for simulation.</description>
            <element name="damping" type="double" default="0" required="0">
              <description>The physical velocity dependent viscous damping coefficient of the joint.</description>
            </element>
            <element name="friction" type="double" default="0" required="0">
              <description>The physical static friction value of the joint.</description>
            </element>
            <element name="spring_reference" type="double" default="0" required="1">
              <description>The spring reference position for this joint axis.</description>
            </element>
            <element name="spring_stiffness" type="double" default="0" required="1">
              <description>The spring stiffness for this joint axis.</description>
            </element>
          </element> <!-- End Dynamics -->
          <element name="limit" required="1">
            <description>specifies the limits of this joint</description>
            <element name="lower" type="double" default="-1e16" required="1">
              <description>Specifies the lower joint limit (radians for revolute joints, meters for prismatic joints). Omit if joint is continuous.</description>
            </element>
            <element name="upper" type="double" default="1e16" required="1">
              <description>Specifies the upper joint limit (radians for revolute joints, meters for prismatic joints). Omit if joint is continuous.</description>
            </element>
            <element name="effort" type="double" default="-1" required="0">
              <description>A value for enforcing the maximum joint effort applied. Limit is not enforced if value is negative.</description>
            </element>
            <element name="velocity" type="double" default="-1" required="0">
              <description>A value for enforcing the maximum joint velocity.</description>
            </element>

            <element name="stiffness" type="double" default="1e8" required="0">
              <description>Joint stop stiffness.</description>
            </element>

            <element name="dissipation" type="double" default="1.0" required="0">
              <description>Joint stop dissipation.</description>
            </element>

          </element> <!-- End Limit -->
        </element> <!-- End Axis -->
        """

        def __init__(
            self,
            *,
            initial_position: float = 0,
            xyz: Union[str, "Joint.Axis.Xyz"] = "0 0 1",
            use_parent_model_frame: bool = False,
            dynamics: "Joint.Axis.Dynamics" = None,
            limit: "Joint.Axis.Limit" = None,
            sdf_version: str,
        ) -> None:
            warnings.warn("`Joint.Axis` is not implemented yet.")
            super().__init__(sdf_version=sdf_version)

        class Xyz(ElementBase):
            def __init__(
                self,
                *,
                value: str = "0 0 1",
                expressed_in: str = None,
                sdf_version: str,
            ) -> None:
                warnings.warn("`Joint.Axis.Xyz` is not implemented yet.")
                super().__init__(sdf_version=sdf_version)

        class Dynamics(ElementBase):
            def __init__(
                self,
                *,
                damping: float = 0,
                friction: float = 0,
                spring_reference: float = 0,
                spring_stiffness: float = 0,
                sdf_version: str,
            ) -> None:
                warnings.warn("`Joint.Axis.Dynamics` is not implemented yet.")
                super().__init__(sdf_version=sdf_version)

        class Limit(ElementBase):
            def __init__(
                self,
                *,
                lower: float = -1e16,
                upper: float = 1e16,
                effort: float = -1,
                velocity: float = -1,
                stiffness: float = 1e8,
                dissipation: float = 1.0,
                sdf_version: str,
            ) -> None:
                warnings.warn("`Joint.Axis.Limit` is not implemented yet.")
                super().__init__(sdf_version=sdf_version)

    class Axis2(ElementBase):
        """
          <element name="axis2" required="0">
          <description>
            Parameters related to the second axis of rotation for revolute2 joints and universal joints.
          </description>
          <element name="initial_position" type="double" default="0" required="-1">
            <description>
              (DEPRECATION WARNING: This tag has no known implementation. It is deprecated SDFormat 1.8 and will be removed in SDFormat 1.9) Default joint position for this joint axis.
            </description>
          </element>
          <element name="xyz" type="vector3" default="0 0 1" required="1">
            <description>
              Represents the x,y,z components of the axis unit vector. The axis is
              expressed in the joint frame unless a different frame is expressed in
              the expressed_in attribute. The vector should be normalized.
            </description>
            <attribute name="expressed_in" type="string" default="" required="0">
              <description>
                Name of frame in whose coordinates the xyz unit vector is expressed.
              </description>
            </attribute>
          </element>
          <element name="dynamics" required="0">
            <description>An element specifying physical properties of the joint. These values are used to specify modeling properties of the joint, particularly useful for simulation.</description>
            <element name="damping" type="double" default="0" required="0">
              <description>The physical velocity dependent viscous damping coefficient of the joint.  EXPERIMENTAL: if damping coefficient is negative and implicit_spring_damper is true, adaptive damping is used.</description>
            </element>
            <element name="friction" type="double" default="0" required="0">
              <description>The physical static friction value of the joint.</description>
            </element>
            <element name="spring_reference" type="double" default="0" required="1">
              <description>The spring reference position for this joint axis.</description>
            </element>
            <element name="spring_stiffness" type="double" default="0" required="1">
              <description>The spring stiffness for this joint axis.</description>
            </element>
          </element> <!-- End Dynamics -->

          <element name="limit" required="1">
            <description></description>
            <element name="lower" type="double" default="-1e16" required="0">
              <description>An attribute specifying the lower joint limit (radians for revolute joints, meters for prismatic joints). Omit if joint is continuous.</description>
            </element>
            <element name="upper" type="double" default="1e16" required="0">
              <description>An attribute specifying the upper joint limit (radians for revolute joints, meters for prismatic joints). Omit if joint is continuous.</description>
            </element>
            <element name="effort" type="double" default="-1" required="0">
              <description>An attribute for enforcing the maximum joint effort applied by Joint::SetForce.  Limit is not enforced if value is negative.</description>
            </element>
            <element name="velocity" type="double" default="-1" required="0">
              <description>(not implemented) An attribute for enforcing the maximum joint velocity.</description>
            </element>

            <element name="stiffness" type="double" default="1e8" required="0">
              <description>Joint stop stiffness. Supported physics engines: SimBody.</description>
            </element>

            <element name="dissipation" type="double" default="1.0" required="0">
              <description>Joint stop dissipation. Supported physics engines: SimBody.</description>
            </element>

          </element> <!-- End Limit -->
        </element> <!-- End Axis2 -->
        """

        def __init__(
            self,
            *,
            initial_position: float = 0,
            xyz: Union[str, "Joint.Axis2.Xyz"] = "0 0 1",
            use_parent_model_frame: bool = False,
            dynamics: "Joint.Axis2.Dynamics" = None,
            limit: "Joint.Axis2.Limit" = None,
            sdf_version: str,
        ) -> None:
            warnings.warn("`Joint.Axis2` is not implemented yet.")
            super().__init__(sdf_version=sdf_version)

        class Xyz(ElementBase):
            def __init__(
                self,
                *,
                value: str = "0 0 1",
                expressed_in: str = None,
                sdf_version: str,
            ) -> None:
                warnings.warn("`Joint.Axis2.Xyz` is not implemented yet.")
                super().__init__(sdf_version=sdf_version)

        class Dynamics(ElementBase):
            def __init__(
                self,
                *,
                damping: float = 0,
                friction: float = 0,
                spring_reference: float = 0,
                spring_stiffness: float = 0,
                sdf_version: str,
            ) -> None:
                warnings.warn("`Joint.Axis2.Dynamics` is not implemented yet.")
                super().__init__(sdf_version=sdf_version)

        class Limit(ElementBase):
            def __init__(
                self,
                *,
                lower: float = -1e16,
                upper: float = 1e16,
                effort: float = 0,
                velocity: float = 0,
                stiffness: float = 1e8,
                dissipation: float = 1.0,
                sdf_version: str,
            ) -> None:
                warnings.warn("`Joint.Axis2.Limit` is not implemented yet.")
                super().__init__(sdf_version=sdf_version)

    class Physics(ElementBase):
        """
          <element name="physics" required="0">
          <description>Parameters that are specific to a certain physics engine.</description>
          <element name="simbody" required="0">
            <description>Simbody specific parameters</description>
            <element name="must_be_loop_joint" type="bool" default="false" required="0">
              <description>Force cut in the multibody graph at this joint.</description>
            </element>
          </element>
          <element name="ode" required="0">
            <description>ODE specific parameters</description>
            <element name="cfm_damping" type="bool" default="false" required="0">
              <description>If cfm damping is set to true, ODE will use CFM to simulate damping, allows for infinite damping, and one additional constraint row (previously used for joint limit) is always active.</description>
            </element>

            <element name="implicit_spring_damper" type="bool" default="false" required="0">
              <description>If implicit_spring_damper is set to true, ODE will use CFM, ERP to simulate stiffness and damping, allows for infinite damping, and one additional constraint row (previously used for joint limit) is always active.  This replaces cfm_damping parameter in SDFormat 1.4.</description>
            </element>

            <element name="fudge_factor" type="double" default="0" required="0">
              <description>Scale the excess for in a joint motor at joint limits. Should be between zero and one.</description>
            </element>
            <element name="cfm" type="double" default="0" required="0">
              <description>Constraint force mixing for constrained directions</description>
            </element>
            <element name="erp" type="double" default="0.2" required="0">
              <description>Error reduction parameter for constrained directions</description>
            </element>
            <element name="bounce" type="double" default="0" required="0">
              <description>Bounciness of the limits</description>
            </element>
            <element name="max_force" type="double" default="0" required="0">
              <description>Maximum force or torque used to reach the desired velocity.</description>
            </element>
            <element name="velocity" type="double" default="0" required="0">
              <description>The desired velocity of the joint. Should only be set if you want the joint to move on load.</description>
            </element>

            <element name="limit" required="0">
              <description></description>
              <element name="cfm" type="double" default="0.0" required="1">
                <description>Constraint force mixing parameter used by the joint stop</description>
              </element>
              <element name="erp" type="double" default="0.2" required="1">
                <description>Error reduction parameter used by the joint stop</description>
              </element>
            </element>

            <element name="suspension" required="0">
              <description></description>
              <element name="cfm" type="double" default="0.0" required="1">
                <description>Suspension constraint force mixing parameter</description>
              </element>
              <element name="erp" type="double" default="0.2" required="1">
                <description>Suspension error reduction parameter</description>
              </element>
            </element>
          </element>

          <element name="provide_feedback" type="bool" default="false" required="0">
            <description>If provide feedback is set to true, physics engine will compute the constraint forces at this joint.</description>
          </element>
        </element> <!-- End Physics -->
        """

        def __init__(
            self,
            *,
            simbody: "Joint.Physics.Simbody" = None,
            ode: "Joint.Physics.Ode" = None,
            provide_feedback: bool = False,
            sdf_version: str,
        ) -> None:
            warnings.warn("`Joint.Physics` is not implemented yet.")
            super().__init__(sdf_version=sdf_version)

        class Simbody(ElementBase):
            def __init__(
                self,
                *,
                must_be_loop_joint: bool = False,
                sdf_version: str,
            ) -> None:
                warnings.warn("`Joint.Physics.Simbody` is not implemented yet.")
                super().__init__(sdf_version=sdf_version)

        class Ode(ElementBase):
            def __init__(
                self,
                *,
                provide_feedback: bool = False,
                cfm_damping: bool = False,
                implicit_spring_damper: bool = False,
                fudge_factor: float = 0,
                cfm: float = 0,
                erp: float = 0.2,
                bounce: float = 0,
                max_force: float = 0,
                velocity: float = 0,
                limit: "Joint.Physics.Ode.Limit" = None,
                suspension: "Joint.Physics.Ode.Suspension" = None,
                sdf_version: str,
            ) -> None:
                warnings.warn("`Joint.Physics.Ode` is not implemented yet.")
                super().__init__(sdf_version=sdf_version)

            class Limit(ElementBase):
                def __init__(
                    self,
                    *,
                    cfm: float = 0,
                    erp: float = 0.2,
                    sdf_version: str,
                ) -> None:
                    warnings.warn("`Joint.Physics.Ode.Limit` is not implemented yet.")
                    super().__init__(sdf_version=sdf_version)

            class Suspension(ElementBase):
                def __init__(
                    self,
                    *,
                    cfm: float = 0,
                    erp: float = 0.2,
                    sdf_version: str,
                ) -> None:
                    warnings.warn(
                        "`Joint.Physics.Ode.Suspension` is not implemented yet."
                    )
                    super().__init__(sdf_version=sdf_version)
