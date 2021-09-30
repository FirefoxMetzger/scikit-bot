from typing import Dict, Any, Tuple

from .base import ElementBase, Pose, StringElement
from .... import transform as tf


class Frame(ElementBase):
    """A frame of reference.

    Frames are coordinate frames that are rigidly attached to a rigid
    body (or inertial frame) and move together with it. Their primary
    purpose is to make it easier to specify the relative position of
    objects in the simulation.

    .. versionadded:: SDFormat v1.5

    Parameters
    ----------
    name : str
        Name of the frame. It must be unique whithin its scope (model/world),
        i.e., it must not match the name of another frame, link, joint, or model
        within the same scope.
    pose : Pose
        The initial position and orientation of this frame
    attached_to : str
        If specified, this frame is attached to the specified frame. The
        specified frame must be within the same scope and may be defined
        implicitly, i.e., the name of any //frame, //model, //joint, or //link
        within the same scope may be used.

        If missing, this frame is attached to the containing scope's frame.
        Within a //world scope this is the implicit world frame, and within a
        //model scope this is the implicit model frame.

        A frame moves jointly with the frame it is @attached_to. This is
        different from //pose/@relative_to. @attached_to defines how the frame
        is attached to a //link, //model, or //world frame, while
        //pose/@relative_to defines how the frame's pose is represented
        numerically. As a result, following the chain of @attached_to attributes
        must always lead to a //link, //model, //world, or //joint (implicitly
        attached_to its child //link).

        .. versionadded:: SDFormat v1.7
    sdf_version : str
        The SDFormat version to use when constructing this element.

    Attributes
    ----------
    name : str
        See ``Parameters`` section.
    pose : Pose
        See ``Parameters`` section.
    attached_to : str
        See ``Parameters`` section.

    """

    def __init__(
        self,
        *,
        name: str,
        pose: Pose = None,
        attached_to: str = None,
        sdf_version: str,
    ) -> None:
        super().__init__(sdf_version=sdf_version)
        self.name = name
        self.pose = Pose(sdf_version=sdf_version) if pose is None else pose
        self.attached_to = attached_to

        if self.attached_to == "":
            self.attached_to = None

    @classmethod
    def from_specific(cls, specific: Any, *, version: str) -> "ElementBase":
        frame_args = {"name": specific.name}

        args_with_default = {"pose": Pose, "attached_to": StringElement}
        standard_args = cls._prepare_standard_args(
            specific, args_with_default, version=version
        )
        frame_args.update(standard_args)

        return Frame(**frame_args, sdf_version=version)

    def declared_frames(self) -> Dict[str, tf.Frame]:
        return {self.name: tf.Frame(3, name=self.name)}

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
        parent_name = self.attached_to
        child_name = self.name

        parent = declared_frames[parent_name]
        child = declared_frames[child_name]

        parent_static = _scaffolding[parent_name]
        child_static = _scaffolding[child_name]

        link = tf.CompundLink(parent_static.links_between(child_static))
        link(parent, child)
