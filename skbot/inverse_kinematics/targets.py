from numpy.typing import ArrayLike
from typing import Callable, List, Union
import numpy as np
from .. import transform as tf


class Target:
    """Abstract IK target.

    .. versionadded:: 0.10.0

    Parameters
    ----------
    static_frame : tf.Frame
        The frame in which the objective is constant.
    dynamic_frame : tf.Frame
        The frame in which the score is computed.
    atol : float
        The absolute tolerance for the score. If score is below this value
        the target is considered to be reached.
    """

    def __init__(
        self, static_frame: tf.Frame, dynamic_frame: tf.Frame, *, atol: float = 1e-3
    ) -> None:
        self.static_frame = static_frame
        self.dynamic_frame = dynamic_frame
        self._chain = self.static_frame.links_between(self.dynamic_frame)
        self.atol = atol

    def score(self):
        """The score of this target."""
        raise NotImplementedError

    def usage_count(self, joint: tf.Link) -> int:
        """Frequency of joint use in this target.

        This function counts the number of times that ``joint`` is used when
        computing the score for this target.

        Parameters
        ----------
        joint : tf.Link
            The link that has its frequency evaluated.

        Returns
        -------
        frequency : int
            The number of occurences of the link.

        """
        occurences = 0

        for link in self._chain:
            if link is joint:
                occurences += 1
            elif isinstance(link, tf.InvertLink) and link._forward_link is joint:
                occurences += 1

        return occurences

    def uses(self, joint: tf.Link) -> bool:
        """Check if target uses a joint.

        Parameters
        ----------
        joint : tf.Link
            The link to check.

        Returns
        -------
        is_used : bool
            True if joint is used when evaluating this target's score. False
            otherwise.
        """

        for link in self._chain:
            if link is joint:
                return True
            elif isinstance(link, tf.InvertLink) and link._forward_link is joint:
                return True
        return False


class PositionTarget(Target):
    """IK position target (nD).

    This target can be used to find an IK solution that positions a point
    (``static_position``) expressed in ``static_frame`` at a desired target
    position (``dynamic_position``) expressed in ``dynamic_frame``. To compute
    the current score, this target transforms ``static_position`` from
    ``static_frame`` into ``dynamic_frame`` and then measures the distance
    between the transformed point and ``dynamic_positon`` under the desired norm
    (default: L2).

    .. versionadded:: 0.10.0

    Parameters
    ----------
    static_position : ArrayLike
        The value of a position that moves in ``dynamic_frame`` expressed in
        ``static_frame``.
    dynamic_positon : ArrayLike
        The value of the target position expressed in ``dynamic_frame``.
    static_frame : tf.Frame
        The frame in which the moving position is expressed.
    dynamic_frame : tf.Frame
        The frame in which the target position is expressed.
    norm : Callable
        A function of the form ``norm(ArrayLike) -> float`` that computes the
        norm of the distance between ``target_position`` and the transformed
        ``static_position`` in ``dynamic_frame``. If None defaults to L2.

    """

    def __init__(
        self,
        static_position: ArrayLike,
        dynamic_position: ArrayLike,
        static_frame: tf.Frame,
        dynamic_frame: tf.Frame,
        norm: Callable[[np.ndarray], float] = None,
        *,
        atol: float = 1e-3,
    ) -> None:
        super().__init__(static_frame, dynamic_frame, atol=atol)
        self.static_position = np.asarray(static_position)
        self.dynamic_position = np.asarray(dynamic_position)

        if norm is None:
            self.norm = np.linalg.norm
        else:
            self.norm = norm

    def score(self):
        current_pos = self.static_position
        for link in self._chain:
            current_pos = link.transform(current_pos)

        return self.norm(self.dynamic_position - current_pos)


class RotationTarget(Target):
    """IK rotation target (2D/3D).

    This target can be used to find an IK solution such that
    ``dynamic_frame`` has rotation ``desired_rotation`` when the
    rotation is expressed relative to ``static_frame``. The score
    function computes the distance in radians between the current
    rotation and desired rotation.

    .. versionadded:: 0.10.0

    Parameters
    ----------
    desired_rotation : Union[tf.Link, List[tf.Link]]
        A link or list of links that expresses the rotation of
        ``dynamic_frame`` relative to ``static_frame``.
    static_frame : tf.Frame
        The frame in which the rotation is expressed.
    dynamic_frame : tf.Frame
        The frame that should be rotated by
        ``desired_rotation`` relative to ``static_frame``.

    """

    def __init__(
        self,
        desired_rotation: Union[tf.Link, List[tf.Link]],
        static_frame: tf.Frame,
        dynamic_frame: tf.Frame,
        *,
        atol: float = 1e-3,
    ) -> None:
        parent_dim = static_frame.ndim
        child_dim = dynamic_frame.ndim
        if parent_dim != child_dim:
            raise NotImplementedError("Projected Targets are not supported yet.")
        if parent_dim not in [2, 3]:
            raise NotImplementedError("Only 2D and 3D is currently supported.")

        super().__init__(static_frame, dynamic_frame, atol=atol)

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
            value = np.clip((trace - 1) / 2, -1, 1)
            theta = np.arccos(value)
        elif self.static_frame.ndim == 2:
            value = np.clip(trace / 2, -1, 1)
            theta = np.arccos(value)
        else:
            raise NotImplementedError("Only 2D and 3D is currently supported.")

        return theta
