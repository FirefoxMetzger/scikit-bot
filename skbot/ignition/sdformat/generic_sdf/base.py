import numpy as np
from typing import Any, Dict, Tuple
import warnings

from .... import transform as tf


def vector3(value: str):
    return np.fromstring(value, dtype=float, count=3, sep=" ")


def quaternion(value: str):
    # Note: SDFormat quaternions are XYZW
    return np.fromstring(value, dtype=float, count=4, sep=" ")


def vector2d(value: str):
    return np.fromstring(value, dtype=float, count=2, sep=" ")


def vector2i(value: str):
    return np.fromstring(value, dtype=int, count=2, sep=" ")


class ElementBase:
    def __init__(self, *, sdf_version: str) -> None:
        self.sdf_version = sdf_version

    @classmethod
    def from_specific(cls, specific: Any, *, version: str) -> "ElementBase":
        """Create from version-specific object

        This function converts a version-specific instantce of this element
        into its generic counterpart.

        Parameters
        ----------
        specific : Any
            The version-specific object to convert. It can come from any
            of scikit-bot's version-specific bindings.
        version : str
            The SDFormat version of the specific object.

        Returns
        -------
        generic : ElementBase
            The generic counterpart of the specific element.

        """
        warnings.warn(f"`{cls.__name__}` is not implemented yet.")
        return cls(sdf_version=version)

    def to_static_graph(
        self,
        declared_frames: Dict[str, tf.Frame],
        *,
        seed: int = None,
        shape: Tuple,
        axis: int = -1,
    ) -> tf.Frame:
        """Convert to transform graph

        Turns this element into a :mod:`skbot.transform` graph using the
        _static_ constraints defined by this element. The resulting graph places
        a :class:`tf.Frame <skbot.transform.Frame>` at the position of each
        joint, link, sensor, etc., defined by this Element. It then connects
        these frames using translation and rotation :class:`tf.Links
        <skbot.transform.Link>` in such a way that conversion between any two
        coordinate frames becomes possible.

        It differs from :func:`to_dynamic_graph` in that all links in this graph
        are rigid and that joint connections are not modelled explicitly.
        Further, the resulting graph will (if applicable) ignore any defined
        :class:`State` and instead model this element's initial configuration.
        As such, it can not be used for dynamic calculations, e.g., with
        :mod:`skbot.inverse_kinematics`.

        Parameters
        ----------
        declared_frames : Dict[str, tf.Frame]
            The frames declared in the scope in which this element has
            been defined.
        seed: bool
            The seed to use when procedually generating elements of the simulation.
            This is currently limited to the `Population` element only.
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
        frame_graph : tf.Frame
            A frame graph modelling the (static) initial configuration of this
            element.

        Notes
        -----
        This function modifies ``declared_frames`` as a side-effect by appending
        any frames declared by this frame to it.

        """
        warnings.warn(
            f"`{self.__class__.__name__}` does not implement `to_static_graph` yet."
        )
        return tf.Frame(3, name="missing")

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
        """Convert to transform graph

        Turns this element into a :mod:`skbot.transform` graph using the _dynamic_
        constraints defined by this element. The resulting graph places a
        :class:`tf.Frame <skbot.transform.Frame>` at the position of each joint,
        link, sensor, etc., defined by this Element. It then connects these
        frames according to the dynamic constraints defined within this element,
        e.g., constraints from nested :class:`Joints <Joint>`.

        It differs from :func:`to_static_graph` in that all connections are
        dynamic. As a result, the resuling graph can have :class:`State` applied
        to it and it may be used for dynamic calculation, e.g., with
        :mod:`skbot.inverse_kinematics`.


        Parameters
        ----------
        declared_frames : Dict[str, tf.Frame]
            The frames declared in the scope in which this element has
            been defined.
        seed: bool
            The seed to use when procedually generating elements of the simulation.
            This is currently limited to the `Population` element only.
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
        apply_state: bool
            If True (default) each object's state is set according to `World.state`
            (if present).
        _scaffolding : Dict[str, tf.Frame]
            A dictionary of (connected) frames that used to determine the
            relative (initial) position of objects in the simulation. This
            parameter is for internal use and may be removed or change at any
            time without notice.


        Returns
        -------
        frame_graph : tf.Frame
            A frame graph modelling the dynamic structure of this element.

        Notes
        -----
        If this element contains children that are not dynamically connected to
        this element, they will be discarded.

        This function modifies ``declared_frames`` as a side-effect by appending
        any frames declared by this frame to it.

        """
        warnings.warn(
            f"`{self.__class__.__name__}` does not implement `to_dynamic_graph` yet."
        )
        return tf.Frame(3, name="missing")

    def declared_frames(self) -> Dict[str, tf.Frame]:
        """Frames contained in this element.

        Returns
        -------
        frame_dict : Dict[str, tf.Frame]
            A (namespaced) dictionary of frames declared within this element.
            The dict key of each frame is the full (namespaced) name of the
            element in the corresponding SDF.

        Notes
        -----
        Namespaces follow the SDFormat convention and are separated using `::`.

        """
        warnings.warn(
            f"`{self.__class__.__name__}` does not implement `declared_frames` yet."
        )
        return dict()

    @staticmethod
    def _prepare_standard_args(
        specific: Any,
        args_with_default: Dict[str, "ElementBase"] = None,
        list_args: Dict[str, Tuple[str, "ElementBase"]] = None,
        *,
        version: str,
    ) -> Dict[str, Any]:
        if args_with_default is None:
            args_with_default = dict()

        if list_args is None:
            list_args = dict()

        generic_args: Dict[str, Any] = dict()

        # convert arguments with default values
        for name, clazz in args_with_default.items():
            if not hasattr(specific, name):
                continue

            if clazz in [StringElement, BoolElement, FloatElement, IntegerElement]:
                value = getattr(specific, name)
                if value == "__default__":
                    continue
                elif value is not None:
                    generic_args[name] = value
                else:
                    continue
            elif getattr(specific, name) is None:
                generic_args[name] = clazz(sdf_version=version)
            else:
                generic_args[name] = clazz.from_specific(
                    getattr(specific, name), version=version
                )

        for their_name in list_args:
            our_name, clazz = list_args[their_name]

            if not hasattr(specific, their_name):
                generic_args[our_name] = []
                continue

            generic_args[our_name] = [
                clazz.from_specific(x, version=version)
                for x in getattr(specific, their_name)
            ]

        return generic_args


class StringElement(ElementBase):
    """Plumbing for smoother conversion"""


class FloatElement(ElementBase):
    """Plumbing for smoother conversion"""


class IntegerElement(ElementBase):
    """Plumbing for smoother conversion"""


class BoolElement(ElementBase):
    """Plumbing for smoother conversion"""


class Pose(ElementBase):
    """Position and orientation of a simulated object

    A position (x,y,z) and orientation (roll, pitch yaw) with respect
    to the frame named in the relative_to attribute.

    Parameters
    ----------
    value : str
        The numerical value of the pose. It is a string of 6 numbers
        separated by spaces. Default: "0 0 0 0 0 0"
    relative_to : str
        If specified, this pose is expressed in the named frame. The named frame
        must be declared within the same scope (world/model) as the element that
        has its pose specified by this tag.

        If missing, the pose is expressed in the frame of the parent XML element
        of the element that contains the pose. For exceptions to this rule and
        more details on the default behavior, see
        http://sdformat.org/tutorials?tut=pose_frame_semantics.

        Note that @relative_to merely affects an element's initial pose and
        does not affect the element's dynamic movement thereafter.

        .. versionadded:: SDFormat v1.8
            New in v1.8: @relative_to may use frames of nested scopes. In this
            case, the frame is specified using `::` as delimiter to define the
            scope of the frame, e.g.
            `nested_model_A::nested_model_B::awesome_frame`.
    frame : str
        Old name for `relative_to`.
        .. deprecated:: SDFormat v1.7


    """

    def __init__(
        self,
        *,
        value: str = "0 0 0 0 0 0",
        relative_to: str = None,
        frame: str = None,
        sdf_version: str,
    ) -> None:
        super().__init__(sdf_version=sdf_version)
        self.value = np.fromstring(value, dtype=float, count=6, sep=" ")
        self.relative_to = relative_to
        if frame is not None:
            self.relative_to = frame

        if self.relative_to == "":
            self.relative_to = None

    @property
    def frame(self):
        warnings.warn("`Pose.frame` is deprecated. Use `Pose.relative_to` instead.")
        return self.relative_to

    @classmethod
    def from_specific(cls, specific: Any, *, version: str):
        if specific is None:
            return Pose(sdf_version=version)
        elif version in ["1.0", "1.2", "1.3", "1.4"]:
            return Pose(value=specific, sdf_version=version)
        elif version in ["1.5", "1.6"]:
            return Pose(value=specific.value, frame=specific.frame, sdf_version=version)
        else:
            return Pose(
                value=specific.value,
                relative_to=specific.relative_to,
                sdf_version=version,
            )

    def to_tf_link(self) -> tf.Link:
        """tf.Link from **child** to **parent** frame"""
        offset = self.value[:3]
        angles = self.value[3:]

        return tf.CompundLink(
            [
                tf.EulerRotation("xyz", angles),
                tf.Translation(offset),
            ]
        )

    def to_static_graph(
        self,
        declared_frames: Dict[str, tf.Frame],
        child_name: str,
        *,
        shape: Tuple,
        axis: int = -1,
    ) -> None:
        parent_name = self.relative_to

        parent = declared_frames[parent_name]
        child = declared_frames[child_name]

        link = self.to_tf_link()
        link(child, parent)


class PoseBearing(ElementBase):
    def __init__(self, *, pose: Pose = None) -> None:
        self.pose = pose
        if self.pose is None:
            self.pose = Pose()


class NamedPoseBearing(PoseBearing):
    def __init__(self, *, name: str, pose: Pose = None) -> None:
        super().__init__(pose=pose)
        self.name = name


"""
Elements not yet represented:


<?xml version='1.0' encoding='UTF-8'?>
<xsd:schema xmlns:xsd='http://www.w3.org/2001/XMLSchema'>
  <xsd:simpleType name="time">
    <xsd:restriction base="xsd:string">
      <xsd:whiteSpace value="collapse"/>
      <xsd:pattern value="\d+ \d+"/>
    </xsd:restriction>
  </xsd:simpleType>

  <xsd:simpleType name="color">
    <xsd:restriction base="xsd:string">
      <xsd:pattern value="(\s*\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){3}\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s*"/>
    </xsd:restriction>
  </xsd:simpleType>
</xsd:schema>

"""
