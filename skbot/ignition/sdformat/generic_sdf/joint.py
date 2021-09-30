import warnings
from typing import List, Union, Dict, Any, Tuple
from itertools import chain
import numpy as np

from .base import BoolElement, ElementBase, FloatElement, Pose, StringElement, vector3
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
                :class:``Joint.Axis``.
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
        :class:`Joint.Axis`.

        .. versionadded:: SDFormat v1.4
    thread_pitch : float
        Parameter for screw joints. The amount of linear displacement for each
        full rotation of the joint.
    axis : Joint.Axis
        Configuration parameters for joints that rotate around or translate
        along at least one axis.
    axis2 : Joint.Axis
        Configuration parameters for joints that rotate around or translate
        along at least two axis.
    physics : Joint.Physics
        Configuration parameters for various physics engines. (Currently: ODE
        and Simbody.)
    frames : List[Frame]
        A list of frames of reference in which poses may be expressed.

        .. deprecated:: SDFormat v1.7
            Use :attr:`Model.frame` instead.
        .. versionadded:: SDFormat v1.5
    sensors : List[Sensor]
        A list of sensors attached to this joint.

        .. versionadded:: SDFormat v1.4
    sdf_version : str
        The SDFormat version to use when constructing this element.
    origin : Origin
        The joint's origin.

        .. deprecated:: SDFormat v1.2
            Use ``Joint.pose`` instead.

    Attributes
    ----------
    name : str
        See ``Parameters`` section.
    type : str
        See ``Parameters`` section.
    parent : str
        See ``Parameters`` section.
    child : str
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
    axis2 : Joint.Axis
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
        axis2: "Joint.Axis" = None,
        physics: "Joint.Physics" = None,
        frames: List[Frame] = None,
        sensors: List[Sensor] = None,
        sdf_version: str,
    ) -> None:
        super().__init__(sdf_version=sdf_version)
        self.name = name
        self.type = type
        if origin is None:
            self._origin = Origin(sdf_version=sdf_version)
        elif sdf_version == "1.0":
            self._origin = origin
        else:
            warnings.warn("`origin` is deprecated. Use `pose` instead.")
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
        self.axis = Joint.Axis(sdf_version=sdf_version) if axis is None else axis
        self.axis2 = Joint.Axis(sdf_version=sdf_version) if axis2 is None else axis2
        self.physics = (
            Joint.Physics(sdf_version=sdf_version) if physics is None else physics
        )
        self._frames = [] if frames is None else frames
        self.sensors = [] if sensors is None else sensors

        self._origin.pose = self.pose

        if isinstance(parent, Joint.Parent):
            self.parent = parent.link
        else:
            self.parent = parent

        if isinstance(child, Joint.Child):
            self.child = child.link
        else:
            self.child = child

        if self.axis._use_parent_model_frame:
            self.axis.xyz.expressed_in = self.parent
        elif self.axis.xyz.expressed_in is None:
            self.axis.xyz.expressed_in = self.child

        if self.axis2._use_parent_model_frame:
            self.axis2.xyz.expressed_in = self.parent
        elif self.axis2.xyz.expressed_in is None:
            self.axis2.xyz.expressed_in = self.child

        for frame in self._frames:
            if frame.attached_to is None:
                frame.attached_to = self.name
            if frame.pose.relative_to is None:
                frame.pose.relative_to = self.name

        for sensor in sensors:
            if sensor.pose.relative_to is None:
                sensor.pose.relative_to = self.name

            if sensor.camera.pose.relative_to is None:
                sensor.camera.pose.relative_to = f"{self.name}::{sensor.name}"

            for frame in sensor.camera._frames:
                if frame.pose.relative_to is None:
                    frame.pose.relative_to = (
                        f"{self.name}::{sensor.name}::{sensor.camera.name}"
                    )
                if frame.attached_to is None:
                    frame.attached_to = f"{self.name}::{sensor.name}"

            for frame in sensor._frames:
                if frame.pose.relative_to is None:
                    frame.pose.relative_to = f"{self.name}::{sensor.name}"

                if frame.attached_to is None:
                    frame.attached_to = f"{self.name}::{sensor.name}"

    @property
    def origin(self):
        warnings.warn(
            "`Joint.origin` is deprecated since SDFormat v1.2."
            " Use `Joint.pose` instead.",
            DeprecationWarning,
        )
        return self._origin

    @property
    def frames(self):
        warnings.warn(
            "`Link.frames` is deprecated since SDF v1.7."
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
            "axis2": Joint.Axis,
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

        for sensor in self.sensors:
            for name, frame in sensor.declared_frames().items():
                declared_frames[f"{self.name}::{name}"] = frame

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
        joint_child = self.name + "_child"
        joint_parent = self.name + "_parent"

        parent = declared_frames[parent_name]
        joint_child = declared_frames[joint_child]
        joint_parent = declared_frames[joint_parent]

        link = self.pose.to_tf_link()
        link(joint_child, parent)
        link(joint_parent, parent)

        for frame in self._frames:
            frame.to_static_graph(declared_frames, seed=seed, shape=shape, axis=axis)

        for sensor in self.sensors:
            sensor.to_static_graph(
                declared_frames,
                f"{self.name}::{sensor.name}",
                seed=seed,
                shape=shape,
                axis=axis,
            )

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
        joint_name_child = self.name + "_child"
        joint_name_parent = self.name + "_parent"

        parent = declared_frames[parent_name]
        child = declared_frames[child_name]
        joint_parent = declared_frames[joint_name_parent]
        joint_child = declared_frames[joint_name_child]

        parent_static = _scaffolding[parent_name]
        joint_static = _scaffolding[joint_name]
        child_static = _scaffolding[child_name]

        link = tf.CompundLink(parent_static.links_between(joint_static))
        link(parent, joint_parent)

        joint_link: tf.Link = self.to_tf_link(_scaffolding, shape=shape, axis=axis)
        joint_link(joint_child, joint_parent)

        link = tf.CompundLink(joint_static.links_between(child_static))
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

        for sensor in self.sensors:
            parent_name = self.name
            child_name = f"{self.name}::{sensor.name}"

            parent = declared_frames[parent_name]
            child = declared_frames[child_name]

            parent_static = _scaffolding[parent_name]
            child_static = _scaffolding[child_name]

            link = tf.CompundLink(parent_static.links_between(child_static))
            link(parent, child)

            sensor.to_dynamic_graph(
                declared_frames,
                f"{self.name}::{sensor.name}",
                seed=seed,
                shape=shape,
                axis=axis,
                apply_state=apply_state,
                _scaffolding=_scaffolding,
            )

        return declared_frames[self.name]

    def to_tf_link(
        self, scaffolding: Dict[str, tf.Frame], *, shape: Tuple = (3,), axis=-1
    ) -> tf.Link:
        """tf.Link from **child** to **parent** frame

        Parameters
        ----------
        scaffolding : Dict[str, tf.Frame]
            A static graph that allows the resolution of ``Joint.Axis.Xyz.expressed_in``
            (``Joint.Axis.Xyz.Value`` needs to be converted to the the implicit frame of
            ``Joint.child`` as per the spec.)
        shape : tuple
            A tuple describing the shape of elements that the resulting graph should
            transform. This can be used to add batch dimensions to the graph, for
            example to perform vectorized computation on multiple instances of the
            same world in different states, or for batched coordinate
            transformation. Defaults to (3,), which is the shape of a single 3D
            vector in euclidian space.
        axis : int
            The axis along which elements are stored. The axis must have length 3
            (since SDFormat describes 3 dimensional worlds), and all other axis are
            considered batch dimensions. Defaults to -1.

        Returns
        -------
        joint_link : tf.Link
            A parameterized link that represents transformation from the joint's
            child into the joint's parent using the constraint defined by this
            joint.

        """
        expressed_frame = scaffolding[self.axis.xyz.expressed_in]
        child_frame = scaffolding[self.child]
        joint_axis1 = expressed_frame.transform(self.axis.xyz.value, child_frame)

        if self.type == "continuous":
            warnings.warn("Hinge joints have not been added yet.")
            link = tf.Translation((0, 0, 0))
        elif self.type == "revolute":
            angle = np.clip(0, self.axis.limit.lower, self.axis.limit.upper)
            link = tf.RotationalJoint(
                joint_axis1,
                angle=angle,
                upper_limit=self.axis.limit.upper,
                lower_limit=self.axis.limit.lower,
                axis=axis,
            )
        elif self.type == "hinge":
            warnings.warn("Hinge joints have not been added yet.")
            link = tf.Translation((0, 0, 0))
        elif self.type == "gearbox":
            warnings.warn("Gearbox joints have not been added yet.")
            link = tf.Translation((0, 0, 0))
        elif self.type == "revolute2":
            warnings.warn("Revolute2 type joint is not added yet.")
            link = tf.Translation((0, 0, 0))
        elif self.type == "prismatic":
            amount = np.clip(1, self.axis.limit.lower, self.axis.limit.upper)
            link = tf.PrismaticJoint(
                joint_axis1,
                amount=amount,
                upper_limit=self.axis.limit.upper,
                lower_limit=self.axis.limit.lower,
                axis=axis,
            )
        elif self.type == "ball":
            warnings.warn("Ball joints have not been added yet.")
            link = tf.Translation((0, 0, 0))
        elif self.type == "screw":
            warnings.warn("Screw joints have not been added yet.")
            link = tf.Translation((0, 0, 0))
        elif self.type == "universal":
            warnings.warn("Universal joints have not been added yet.")
            link = tf.Translation((0, 0, 0))
        elif self.type == "fixed":
            link = tf.Translation((0, 0, 0))
        else:
            raise ValueError(f"Unknown Joint type: {self.type}")

        return link

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
        """Parameters for rotating and/or translating joints.

        Parameters
        ----------
        initial_position : float
            Default joint position for this joint axis.

            .. deprecated:: SDFormat v1.8
                Use `World.State` instead to set the initial position.
            .. versionadded:: SDFormat v1.6
        xyz: Union[str, Joint.Axis.Xyz]
            The direction of the Axis.

            .. versionchanged:: SDFormat v1.7
                ``xyz`` is now a class. The direction vector is stored
                in ``xyz.value``.
        use_parent_model_frame : bool
            Flag to interpret the axis xyz element in the parent model frame
            instead of joint frame. Provided for Gazebo compatibility (see
            https://github.com/osrf/gazebo/issue/494 ). Default is: ``False``.

            .. deprecated:: SDFormat v1.7
                Use :attr:`Joint.Axis.Xyz.expressed_in` instead.
            .. versionadded:: SDFormat v1.5
        dynamics: Joint.Axis.Dynamics
            Dynamic Parameters related to the Axis.
        limit : Joint.Axis.Limit
            Constraints applied to parameters of this joint, e.g., upper/lower
            limits.

            .. versionchanged:: SDFormat v1.6
                The limit element is now optional.
        sdf_version : str
            The SDFormat version to use when constructing this element.

        Attributes
        ----------
        initial_position : float
            See ``Parameters`` section.
        xyz: Joint.Axis.Xyz
            See ``Parameters`` section.
        dynamics: Joint.Axis.Dynamics
            See ``Parameters`` section.
        limit : Joint.Axis.Limit
            See ``Parameters`` section.

        """

        def __init__(
            self,
            *,
            initial_position: float = 0,
            xyz: Union[str, "Joint.Axis.Xyz"] = None,
            use_parent_model_frame: bool = False,
            dynamics: "Joint.Axis.Dynamics" = None,
            limit: "Joint.Axis.Limit" = None,
            sdf_version: str,
        ) -> None:
            super().__init__(sdf_version=sdf_version)
            self.initial_position = initial_position
            if sdf_version in ["1.0", "1.2", "1.3", "1.4", "1.5", "1.6"]:
                if xyz is None:
                    # old default
                    xyz = "0 0 1"
                self.xyz = Joint.Axis.Xyz(
                    value=xyz, expressed_in=None, sdf_version=sdf_version
                )
            elif xyz is None:
                self.xyz = Joint.Axis.Xyz(sdf_version=sdf_version)
            else:
                self.xyz = xyz
            self._use_parent_model_frame = use_parent_model_frame
            self.dynamics = (
                Joint.Axis.Dynamics(sdf_version=sdf_version)
                if dynamics is None
                else dynamics
            )
            self.limit = (
                Joint.Axis.Limit(sdf_version=sdf_version) if limit is None else limit
            )

        @property
        def use_parent_model_frame(self):
            warnings.warn(
                "`Joint.Axis.use_parent_model_frame` is deprecated."
                " Use `Joint.Axis.Xyz.expressed_in` instead."
            )
            return self._use_parent_model_frame

        @classmethod
        def from_specific(cls, specific: Any, *, version: str) -> "ElementBase":
            args_with_default = {
                "initial_position": FloatElement,
                "xyz": Joint.Axis.Xyz,
                "use_parent_model_Frame": BoolElement,
                "dynamics": Joint.Axis.Dynamics,
                "limit": Joint.Axis.Limit,
            }

            if version in ["1.0", "1.2", "1.3", "1.4", "1.5", "1.6"]:
                args_with_default["xyz"] = StringElement

            standard_args = cls._prepare_standard_args(
                specific, args_with_default, version=version
            )

            return Joint.Axis(**standard_args, sdf_version=version)

        class Xyz(ElementBase):
            """The direction of an axis.

            Represents the x,y,z components of the axis unit vector. The
            vector should be normalized.

            .. versionadded:: SDFormat v1.7

            Parameters
            ----------
            value : str
                The numerical value of the direction. Default: "0 0 1".
            expressed_in : str
                The frame of reference in which the direction is expressed.
            sdf_version : str
                The SDFormat version to use when constructing this element.

            Attributes
            ----------
            value : np.ndarray
                See ``Parameters`` section.
            expressed_in : str
                See ``Parameters`` section.

            """

            def __init__(
                self,
                *,
                value: str = "0 0 1",
                expressed_in: str = None,
                sdf_version: str,
            ) -> None:
                super().__init__(sdf_version=sdf_version)
                self.value = vector3(value)

                self.expressed_in = expressed_in
                if self.expressed_in == "":
                    self.expressed_in = None

            @classmethod
            def from_specific(cls, specific: Any, *, version: str) -> "ElementBase":
                return Joint.Axis.Xyz(
                    value=specific.value,
                    expressed_in=specific.expressed_in,
                    sdf_version=version,
                )

        class Dynamics(ElementBase):
            """Dynamic Parameters along an axis.

            An element specifying physical properties of the joint related to
            the axis. These values are used to specify modeling properties of
            the joint, particularly useful for simulation.

            Parameters
            ----------
            damping : float
                Viscous damping coefficient along this axis. The default is
                ``0``.
            friction : float
                Static friction along this axis. The default is ``0``.
            spring_reference : float
                The neutral position of the spring along this axis. The default
                is ``0``.

                .. versionadded:: SDFormat v1.5
            spring_stiffness : float
                The stiffness of the spring along this axis. The default is
                ``0``.

                .. versionadded:: SDFormat v1.5
            sdf_version : str
                The SDFormat version to use when constructing this element. The
                default is ``0``.

            Attributes
            ----------
            damping : float
                See ``Parameters`` section.
            friction : float
                See ``Parameters`` section.
            spring_reference : float
                See ``Parameters`` section.
            spring_stiffness : float
                See ``Parameters`` section.
            """

            def __init__(
                self,
                *,
                damping: float = 0,
                friction: float = 0,
                spring_reference: float = 0,
                spring_stiffness: float = 0,
                sdf_version: str,
            ) -> None:
                super().__init__(sdf_version=sdf_version)
                self.damping = damping
                self.friction = friction
                self.spring_reference = spring_reference
                self.spring_stiffness = spring_stiffness

            @classmethod
            def from_specific(cls, specific: Any, *, version: str) -> "ElementBase":
                args_with_default = {
                    "damping": FloatElement,
                    "friction": FloatElement,
                    "spring_reference": FloatElement,
                    "spring_stiffness": FloatElement,
                }
                standard_args = cls._prepare_standard_args(
                    specific, args_with_default, version=version
                )
                return Joint.Axis.Dynamics(**standard_args, sdf_version=version)

        class Limit(ElementBase):
            """Joint limits along an axis.

            This class specifies limites/constraints for joint parameters along
            the containing axis.

            Parameters
            ----------
            lower : float
                A lower limit for any joint parameter along this axis. In
                radians for revolute joints and in meters for prismatic joints.
                Default: ``-1e16``.
            upper : float
                A upper limit for any joint parameter along this axis. In
                radians for revolute joints and in meters for prismatic joints.
                Default: ``1e16``.
            effort : float
                The maximum effort that may be applied to/by a joint along this
                axis. This limit is not enforced if its value is negative.
                Default: ``-1``.

                .. versionchanged:: SDFormat v1.3
                    The default changed from 0 to -1.
            velocity : float
                The maximum velocity (angular or directional respectively) that
                may be applied to/by this joint. This limit is not enforced if
                its value is negative. Default: ``-1``.

                .. versionchanged:: SDFormat v1.3
                    The default changed from 0 to -1.
            stiffness : float
                Joint stop stiffness. Default: ```1e8``.

                .. versionadded:: SDFormat v1.4
            dissipation : float
                Joint stop dissipation. Default: ```1.0``.

                .. versionadded:: SDFormat v1.4
            sdf_version : str
                The SDFormat version to use when constructing this element.

            Attributes
            ----------
            lower : float
                See ``Parameters`` section.
            upper : float
                See ``Parameters`` section.
            effort : float
                See ``Parameters`` section.
            velocity : float
                See ``Parameters`` section.
            stiffness : float
                See ``Parameters`` section.
            dissipation : float
                See ``Parameters`` section.

            """

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
                super().__init__(sdf_version=sdf_version)
                self.lower = lower
                self.upper = upper
                if effort < 0:
                    self.effort = float("inf")
                else:
                    self.effort = effort
                if velocity < 0:
                    self.velocity = float("inf")
                else:
                    self.velocity = velocity
                self.stiffness = stiffness
                self.dissipation = dissipation

            @classmethod
            def from_specific(cls, specific: Any, *, version: str) -> "ElementBase":
                args_with_default = {
                    "lower": FloatElement,
                    "upper": FloatElement,
                    "effort": FloatElement,
                    "velocity": FloatElement,
                    "stiffness": FloatElement,
                    "dissipation": FloatElement,
                }
                standard_args = cls._prepare_standard_args(
                    specific, args_with_default, version=version
                )
                return Joint.Axis.Limit(**standard_args, sdf_version=version)

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
