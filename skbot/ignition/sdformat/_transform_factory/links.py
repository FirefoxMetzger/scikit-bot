from typing import Union
import numpy as np
from scipy.spatial.transform import Rotation as ScipyRotation

from .... import transform as tf
from .scopes import Scope, SdfLink


class CustomLink(SdfLink):
    def __init__(
        self, parent: Union[str, tf.Frame], child: Union[str, tf.Frame], link: tf.Link
    ) -> None:
        super().__init__(parent, child)
        self._link = link

    def to_transform_link(self, scope: "Scope") -> tf.Link:
        return self._link


class SimplePose(SdfLink):
    def __init__(
        self, parent: Union[str, tf.Frame], child: Union[str, tf.Frame], pose: str
    ) -> None:
        super().__init__(parent, child)
        self.pose = np.array(pose.split(" "), dtype=float)

    def to_transform_link(self, scope: "Scope", *, angle_eps=1e-15) -> tf.Link:
        if np.any(np.abs(self.pose[3:]) > angle_eps):
            return tf.CompundLink(
                [tf.EulerRotation("xyz", self.pose[3:]), tf.Translation(self.pose[:3])]
            )
        else:
            return tf.Translation(self.pose[:3])


class DynamicPose(SdfLink):
    def __init__(
        self,
        parent: Union[str, tf.Frame],
        child: Union[str, tf.Frame],
        *,
        scaffold_parent: Union[str, tf.Frame] = None,
        scaffold_child: Union[str, tf.Frame] = None
    ) -> None:
        super().__init__(parent, child)

        self.scaffold_parent = scaffold_parent
        if scaffold_parent is None:
            self.scaffold_parent = parent

        self.scaffold_child = scaffold_child
        if scaffold_child is None:
            self.scaffold_child = child

    def to_transform_link(self, scope: "Scope", *, angle_eps=1e-15) -> tf.Link:
        parent = self.scaffold_parent
        child = self.scaffold_child
        
        if isinstance(parent, str):
            parent = scope.get(parent, scaffolding=True)

        if isinstance(child, str):
            child = scope.get(child, scaffolding=True)

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
        parent: Union[str, tf.Frame],
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
