from typing import Dict, List, Union
import numpy as np
from scipy.spatial.transform import Rotation as ScipyRotation

from .... import transform as tf
from .. import sdformat


class SdfLink:
    def __init__(self, parent: str, child: Union[str, tf.Frame]) -> None:
        self.parent: Union[str, tf.Frame] = parent
        self.child: Union[str, tf.Frame] = child

    def to_transform_link(self, scope: "Scope") -> tf.Link:
        raise NotImplementedError()


class CustomLink(SdfLink):
    def __init__(self, parent: str, child: Union[str, tf.Frame], link: tf.Link) -> None:
        super().__init__(parent, child)
        self._link = link

    def to_transform_link(self, scope: "Scope") -> tf.Link:
        return self._link


class SimplePose(SdfLink):
    def __init__(
        self, parent: str, child: Union[str, tf.Frame], pose: np.ndarray
    ) -> None:
        super().__init__(parent, child)
        self.pose = pose

    def to_transform_link(self, scope: "Scope", *, angle_eps=1e-15) -> tf.Link:
        if np.any(np.abs(self.pose[3:]) > angle_eps):
            return tf.CompundLink(
                [tf.EulerRotation("xyz", self.pose[3:]), tf.Translation(self.pose[:3])]
            )
        else:
            return tf.Translation(self.pose[:3])


class DynamicPose(SdfLink):
    def to_transform_link(self, scope: "Scope", *, angle_eps=1e-15) -> tf.Link:
        child = scope.get(self.child, scaffolding=True)
        parent = scope.get(self.parent, scaffolding=True)

        translation = parent.transform((0, 0, 0), child)

        # link's euler angles
        rot_matrix = list()
        for basis in np.eye(3):
            basis = parent.transform(basis, child)
            rot_matrix.append(basis)
        rot_matrix = np.stack(rot_matrix, axis=1)
        rot_matrix -= translation[:, None]
        angles = ScipyRotation.from_matrix(rot_matrix).as_euler("xyz")

        if np.any(np.abs(angles) > angle_eps):
            return tf.CompundLink(
                [tf.EulerRotation("xyz", angles), tf.Translation(translation)]
            )
        else:
            return tf.Translation(translation)


class SingleAxisJoint(DynamicPose):
    def __init__(
        self,
        parent: str,
        child: Union[str, tf.Frame],
        axis: str,
        expressed_in: str = None,
    ) -> None:
        super().__init__(parent, child)
        self.axis = np.array(axis.split(" "), dtype=float)
        self.expressed_in = parent
        if expressed_in is not None:
            self.expressed_in: Union[str, tf.Frame] = expressed_in


class RotationJoint(SingleAxisJoint):
    def to_transform_link(self, scope: "Scope", *, angle_eps=1e-15) -> tf.Link:
        expressed_in = scope.get(self.expressed_in, scaffolding=True)
        parent = scope.get(self.parent, scaffolding=True)

        pose_tf = super().to_transform_link(scope, angle_eps=angle_eps)

        axis = expressed_in.transform(self.axis, parent)
        joint = tf.RotvecRotation(axis)

        return tf.CompundLink([joint, pose_tf])


class PrismaticJoint(SingleAxisJoint):
    def to_transform_link(self, scope: "Scope", *, angle_eps=1e-15) -> tf.Link:
        expressed_in = scope.get(self.expressed_in, scaffolding=True)
        parent = scope.get(self.parent, scaffolding=True)

        pose_tf = super().to_transform_link(scope, angle_eps=angle_eps)

        axis = expressed_in.transform(self.axis, parent)
        axis /= np.linalg.norm(axis)
        joint = tf.Translation(axis)

        return tf.CompundLink([joint, pose_tf])


class Scope:
    """A scope within SDFormat"""

    def __init__(self, name, *, parent: "Scope" = None) -> None:
        self.nested_scopes: Dict[str, "Scope"] = dict()

        self.frames: Dict[str, tf.Frame] = dict()
        self.links: List[SdfLink] = list()

        self.scaffold_frames: Dict[str, tf.Frame] = dict()
        self.scaffold_links: List[SdfLink] = list()

        # might be able to remove this
        self.name = name

        self.parent = parent
        self.placement_frame: str = None
        if self.name == "world":
            self.default_frame = tf.Frame(3, name="world")
            self.scaffold_frames["world"] = self.default_frame
            self.frames["world"] = tf.Frame(3, name="world")
        else:
            self.default_frame = tf.Frame(3, name="__model__")
            self.scaffold_frames["__model__"] = self.default_frame
            self.cannonical_link: str = None

    def declare_frame(self, name: str, *, scaffold=True, dynamic=True):
        if name in self.frames.keys():
            raise IndexError("Frame already declared.")

        if dynamic:
            self.frames[name] = tf.Frame(3, name=name)

        if scaffold:
            self.scaffold_frames[name] = tf.Frame(3, name=name)

    def add_scaffold(self, frame_name: str, pose: str, relative_to: str = None) -> None:
        pose_array = np.array(pose.split(" "), dtype=float)

        parent = self.default_frame.name
        if relative_to is not None:
            parent = relative_to

        self.scaffold_links.append(SimplePose(frame_name, parent, pose_array))

    def declare_link(self, link: SdfLink) -> None:
        self.links.append(link)

    def get(self, name: str, scaffolding: bool) -> tf.Frame:
        """Find the frame from a (namespaced) SDFormat name"""

        if name == "world":
            if self.parent is None:
                if self.name != "world":
                    raise sdformat.ParseError("Not a world element.")
                if scaffolding:
                    return self.default_frame
                else:
                    return self.frames["world"]
            else:
                return self.parent.get(name, scaffolding)

        if "::" in name:
            elements = name.split("::")
            scope = elements.pop(0)
            name = "::".join(elements)
            return self.nested_scopes[scope].get(name, scaffolding)
        else:
            if scaffolding:
                return self.scaffold_frames[name]
            else:
                return self.frames[name]

    def build_scaffolding(self):
        for el in self.scaffold_links:
            tf_link = el.to_transform_link(self)
            parent = self.get(el.parent, scaffolding=True)
            child = self.get(el.parent, scaffolding=True)
            tf_link(parent, child)

        for scope in self.nested_scopes.values():
            scope.build_scaffolding()

    def resolve_links(self):
        for el in self.links:
            if isinstance(el.parent, str):
                parent = self.get(el.parent, scaffolding=False)
            else:
                parent = el.parent
            
            if isinstance(el.child, str):
                child = self.get(el.parent, scaffolding=False)
            else:
                child = el.child
            
            tf_link = el.to_transform_link(self)
            tf_link(parent, child)

        for scope in self.nested_scopes.values():
            scope.resolve_links()

    def add_subscope(self, nested_scope: "Scope") -> None:
        if nested_scope.name in self.nested_scopes.keys():
            raise KeyError("Nested Scope already defined.")

        self.nested_scopes[nested_scope.name] = nested_scope
        nested_scope.parent = self
