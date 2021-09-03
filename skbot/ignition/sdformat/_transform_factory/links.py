""" Link building classes for Frame Graph

The classes below are the various instances used by the Scope.resolve_links
factory. After the pose scaffolding has been built (Scope.build_scaffold) the
classes below can be used to retrieve the links that will connect the frames of
the final frame graph.

"""


from typing import Union, Tuple
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

    def to_transform_link(self, scope: "Scope", shape: tuple, axis: int) -> tf.Link:
        return self._link


class SimplePose(SdfLink):
    """A fixed pose that doesn't need the scaffold"""

    def __init__(
        self, parent: Union[str, tf.Frame], child: Union[str, tf.Frame], pose: str
    ) -> None:
        super().__init__(parent, child)
        self.pose = np.array(pose.split(), dtype=float)

    def to_transform_link(self, scope: "Scope", shape: tuple, axis: int) -> tf.Link:
        offset = np.broadcast_to(self.pose[:3], shape)
        angles = np.broadcast_to(self.pose[3:], shape)

        return tf.CompundLink(
            [
                tf.Translation(-offset, axis=axis),
                tf.EulerRotation("xyz", -angles, axis=axis),
            ]
        )


class DynamicPose(SdfLink):
    """A pose that needs to be worked out after scaffolding has been built."""

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

    def to_transform_link(self, scope: "Scope", shape: tuple, axis: int) -> tf.Link:
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

        translation = np.broadcast_to(translation, shape)
        angles = np.broadcast_to(angles, shape)

        return tf.CompundLink(
            [
                tf.Translation(-translation, axis=axis),
                tf.EulerRotation("xyz", -angles, axis=axis),
            ]
        )


class SingleAxisJoint(SdfLink):
    """Base class for joints using an axis"""

    def __init__(
        self,
        parent: Union[str, tf.Frame],
        child: Union[str, tf.Frame],
        axis: str,
        expressed_in: str,
        lower_limit: float,
        upper_limit: float,
    ) -> None:
        super().__init__(parent, child)
        self.axis = np.array(axis.split(" "), dtype=float)
        self.expressed_in = parent
        self.expressed_in: Union[str, tf.Frame] = expressed_in
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit

    def _convert_axis(self, scope: "Scope", shape: Tuple[int]) -> np.ndarray:
        expressed_in = scope.get(self.expressed_in, scaffolding=True)
        parent = scope.get(self.parent, scaffolding=True)

        rotvec = expressed_in.transform(self.axis, parent)
        rotvec /= np.linalg.norm(rotvec)
        rotvec = np.broadcast_to(rotvec, shape)

        return rotvec


class RotationJoint(SingleAxisJoint):
    def to_transform_link(self, scope: "Scope", shape: tuple, axis: int) -> tf.Link:
        rotvec = self._convert_axis(scope, shape)
        angle_shape = [*shape]
        angle_shape.pop(axis)
        angle = np.zeros(angle_shape)

        # TODO: remove clip in favor of SDF state
        angle = np.clip(angle, self.lower_limit, self.upper_limit)

        return tf.RotationalJoint(
            rotvec,
            angle=angle,
            axis=axis,
            lower_limit=self.lower_limit,
            upper_limit=self.upper_limit,
        )


class PrismaticJoint(SingleAxisJoint):
    def to_transform_link(self, scope: "Scope", shape: tuple, axis: int) -> tf.Link:
        direction = self._convert_axis(scope, shape)
        amount_shape = [*shape]
        amount_shape.pop(axis)
        amount = np.ones(amount_shape)

        # TODO: remove clip in favor of SDF state
        amount = np.clip(amount, self.lower_limit, self.upper_limit)

        return tf.PrismaticJoint(
            direction,
            amount=np.ones(amount_shape),
            axis=axis,
            lower_limit=self.lower_limit,
            upper_limit=self.upper_limit,
        )
