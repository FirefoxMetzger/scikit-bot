from numpy.typing import ArrayLike
from typing import Callable, List, Union
import numpy as np
from .. import transform as tf
from ..transform._utils import angle_between


class Target:
    def __init__(self, static_frame: tf.Frame, dynamic_frame: tf.Frame) -> None:
        self.static_frame = static_frame
        self.dynamic_frame = dynamic_frame
        self._chain = self.static_frame.links_between(self.dynamic_frame)

    def score(self):
        raise NotImplementedError

    def usage_count(self, joint: tf.Link):
        """The number of occurences of a link within a chain of links"""
        occurences = 0

        for link in self._chain:
            if link is joint:
                occurences += 1
            elif isinstance(link, tf.InvertLink) and link._forward_link is joint:
                occurences += 1

        return occurences

    def uses(self, joint: tf.Link):
        """Check if joint exists in this goals chain."""

        for link in self._chain:
            if link is joint:
                return True
        return False


class PositionTarget(Target):
    def __init__(
        self,
        static_position: ArrayLike,
        dynamic_position: ArrayLike,
        static_frame: tf.Frame,
        dynamic_frame: tf.Frame,
        norm: Callable[[np.ndarray], float] = None,
    ) -> None:
        super().__init__(static_frame, dynamic_frame)
        self.static_position = np.asarray(static_position)
        self.dynamic_position = np.asarray(dynamic_position)

        if norm is None:
            self.norm = np.linalg.norm

    def score(self):
        current_pos = self.static_position
        for link in self._chain:
            current_pos = link.transform(current_pos)

        return self.norm(self.dynamic_position - current_pos)


class RotationTarget(Target):
    def __init__(
        self,
        desired_rotation: Union[tf.Link, List[tf.Link]],
        static_frame: tf.Frame,
        dynamic_frame: tf.Frame,
    ) -> None:
        parent_dim = static_frame.ndim
        child_dim = dynamic_frame.ndim
        if parent_dim != child_dim:
            raise NotImplementedError("Projected Targets are not supported yet.")
        if parent_dim not in [2, 3]:
            raise NotImplementedError("Only 2D and 3D is currently supported.")

        super().__init__(static_frame, dynamic_frame)

        if isinstance(desired_rotation, tf.Link):
            self.desired_rotation = [desired_rotation]
        else:
            self.desired_rotation = desired_rotation
        self.desired_rotation = tf.simplify_links(self.desired_rotation)
        self.desired_rotation = [
            x for x in self.desired_rotation if not isinstance(x, tf.Translation)
        ]

    def score(self):
        basis = np.eye(self.static_frame.ndim)

        desired_basis = basis
        for link in self.desired_rotation:
            desired_basis = link.transform(desired_basis)

        reduced = tf.simplify_links(self._chain)
        reduced = [x for x in reduced if not isinstance(x, tf.Translation)]
        actual_basis = basis
        for link in reduced:
            actual_basis = link.transform(actual_basis)

        trace = np.trace(desired_basis @ actual_basis.T)
        if self.static_frame.ndim == 3:
            theta = np.arccos((trace - 1) / 2)
        else:
            theta = np.arccos(trace / 2)

        return np.pi - abs(theta - np.pi)
