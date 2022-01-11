from .. import transform as tf
from ..transform._utils import scalar_project, angle_between
from numpy.typing import ArrayLike
from typing import List, Callable
import numpy as np
from scipy.optimize import minimize_scalar
from scipy.optimize import OptimizeResult
from .targets import Target, PositionTarget, RotationTarget

import warnings


def step_generic_joint(
    joint: tf.Joint, target: Target, maxiter: int
) -> Callable[[], None]:
    """Find the optimal value for the current joint."""

    def generic_objective(x: float, current_joint: tf.Joint) -> float:
        current_joint.param = x
        return target.score()

    def inner() -> None:
        if target.score() < target.atol:
            return  # nothing to do

        result: OptimizeResult = minimize_scalar(
            lambda x: generic_objective(x, joint),
            bounds=(joint.lower_limit, joint.upper_limit),
            method="bounded",
            options={"maxiter": maxiter},
        )

        if not result.success:
            raise RuntimeError(f"IK failed. Reason: {result.message}")

        joint.param = result.x

    return inner


def analytic_rotation(
    joint: tf.RotationalJoint, target: PositionTarget
) -> Callable[[], None]:
    """Fast-path for rotation joints and position targets.

    This computes the optimal joint value analytically instead of solving
    a sub-optimization problem.

    .. versionadded:: 0.10.0

    """
    joint_idx = target._chain.index(joint)

    basis1 = np.array((1, 0), dtype=float)
    basis2 = np.array((0, 1), dtype=float)

    eps = 1e-10

    def inner() -> None:
        if target.score() < target.atol:
            return  # nothing to do

        target_point = target.dynamic_position
        for link in reversed(target._chain[joint_idx:]):
            target_point = link.__inverse_transform__(target_point)
        target_projected = np.array(
            [
                scalar_project(target_point, joint._u),
                scalar_project(target_point, joint._u_ortho),
            ]
        )

        current_position = target.static_position
        for link in target._chain[:joint_idx]:
            current_position = link.transform(current_position)
        current_projected = np.array(
            [
                scalar_project(current_position, joint._u),
                scalar_project(current_position, joint._u_ortho),
            ]
        )

        # skip adjustment if the desired position is in the joints null space
        if np.linalg.norm(target_projected) < eps:
            return

        target_angle = angle_between(target_projected, basis1)
        if angle_between(target_projected, basis2) > np.pi / 2:
            target_angle = -target_angle

        current_angle = angle_between(current_projected, basis1)
        if angle_between(current_projected, basis2) > np.pi / 2:
            current_angle = -current_angle

        angle = target_angle - current_angle

        # it is a bit odd that I have to use - angle here instead of using
        # + angle. There may be a bug regarding left/right handedness somewhere
        joint.param = np.clip(joint.param - angle, joint.lower_limit, joint.upper_limit)

    return inner


def ccd(
    targets: List[Target],
    joints: List[tf.Joint] = None,
    *args,
    rtol: float = 1e-6,
    maxiter: int = 500,
    line_search_maxiter: int = 500,
    weights: List[float] = None,
    tol: float = None,
    cycle_links: List[tf.Joint] = None,
    pointA: ArrayLike = None,
    pointB: ArrayLike = None,
    frameA: tf.Frame = None,
    frameB: tf.Frame = None,
    metric: Callable[[np.ndarray, np.ndarray], float] = None,
) -> List[np.ndarray]:
    """Cyclic Coordinate Descent.

    .. note::
        This function will modify the objects in ``joints`` as a side effect.

    This function cycles through ``targets`` and ``joints``. For each pair it -
    one joint at a time - chooses a value for the joint that minimizes the score
    of the target. If all targets are reached, this function returns the the
    corresponding joint parameters; otherwise an exception is raised.

    .. versionchanged:: 0.10.0
        CCD has a new signature and now makes use of Targets.
    .. versionchanged:: 0.10.0
        CCD can now jointly optimize for multiple targets.
    .. versionadded:: 0.7.0

    Parameters
    ----------
    targets : List[Target]
        A list of quality measures that a successful pose minimizes.
    joints : List[joint]
        A list of 1DoF joints which should be adjusted to minimize ``targets``.
    rtol : float
        Relative tolerance for termination. If, after one full cycle, none
        of the targets have improved by more than rtol the algorithm terminates
        and assumes that a local optimum has been found.
    maxiter : int
        The maximum number of times to cycle over target+joint pairs.
    line_search_maxiter : int
        If no fast-path is implemented for a joint+target pair then CCD solves a
        1D sub-optimization problem for the pair instead. This parameter limits
        the total number of iterations for this sub-optimization.
    weights : List[float]
        .. deprecated:: 0.10.0
            Targets are optimized cyclical instead of optimizing a weighted sum.

        This parameter has no effect.
    cycle_links : List[tf.Joint]
        .. deprecated:: 0.10.0
            Use ``joints`` instead.

        A list of 1DoF joints which should be adjusted to minimize targets.
    tol : float
        .. deprecated:: 0.10.0
            Specify ``atol`` on the desired target instead.

        Absolute tolerance for termination.
    pointA : ArrayLike
        .. deprecated:: 0.10.0
            Use ``targets`` and a :class:`ik.PositionTarget
            <skbot.inverse_kinematics.PositionTarget>` instead.

        A list of points. The i-th pointA is represented in the i-th frame of
        frameA. If only one point is given, the list can be omitted and the point
        can be directly used as input.
    pointB : ArrayLike
        .. deprecated:: 0.10.0
            Use ``targets`` and a :class:`ik.PositionTarget
            <skbot.inverse_kinematics.PositionTarget>` instead.

        The desired positions of each point given in pointA. The i-th pointB is
        represented in the i-th frame of frameB. If only one point is given, the
        list can be omitted and the point can be directly used as input.
    frameA : tf.Frame
        .. deprecated:: 0.10.0
            Use ``targets`` and a :class:`ik.PositionTarget
            <skbot.inverse_kinematics.PositionTarget>` instead.

        The frame in which the points in pointA are represented. The i-th
        element corresponds to the i-th pointA. If only one point is given, the
        list can be omitted and the frame can be directly used as input.
    frameB : tf.Frame
        .. deprecated:: 0.10.0
            Use ``targets`` and a :class:`ik.PositionTarget
            <skbot.inverse_kinematics.PositionTarget>` instead.

        The frame in which the points in pointB are represented. The i-th
        element corresponds to the i-th pointB. If only one point is given, the
        list can be omitted and the frame can be directly used as input.
    metric : Callable
        .. deprecated:: 0.10.0
            Specify ``norm`` in a :class:`PositionTarget
            <skbot.inverse_kinematics.PositionTarget>` instead.

        A function that takes two points (expressed in the corresponding frameB)
        and that computs the distance between them. Its signature is
        ``metric(transformed_point, pointB) -> distance``. If None, the
        euclidian distance will be used.

    Returns
    -------
    joint_values : List[float]
        The final parameters of each joint.

    Notes
    -----
    Joint limits (min/max) are enforced as hard constraints.

    The current implementation is a naive python implementation and not very
    optimized. PRs improving performance are welcome :)

    References
    ----------
    .. [kenwright2012] Kenwright, Ben. "Inverse kinematics-cyclic coordinate descent (CCD)."
        Journal of Graphics Tools 16.4 (2012): 177-217.

    """

    if len(args) > 0:
        if len(args) != 3:
            raise TypeError(
                f"ccd() takes 2 positional arguments, but {2+len(args)} were given."
            )

        warnings.warn(
            "The signature `ccd(pointA, pointB, frameA, frameB, cycle_links)`"
            " is depreciated and will be removed in scikit-bot v1.0."
            " Use `targets` combined with a `ik.PositionTarget` instead.",
            DeprecationWarning,
        )

        target = PositionTarget(targets, joints, args[0], args[1])
        targets = [target]
        joints = args[2]

    elif frameA is not None:
        warnings.warn(
            "The use of `pointA`, `pointB`, `frameA`, and `frameB` is deprecated"
            " and will be removed in scikit-bot v1.0."
            " Use `targets` combined with a `ik.PositionTarget` instead.",
            DeprecationWarning,
        )

        target = PositionTarget(
            static_position=np.asarray(pointA),
            dynamic_position=np.asarray(pointB),
            static_frame=frameA,
            dynamic_frame=frameB,
        )
        targets.append(target)

    if cycle_links is not None:
        warnings.warn(
            "The use of `cycle_links` is depreciated"
            " and will be removed in scikit-bot v1.0."
            " Use `joints` instead.",
            DeprecationWarning,
        )
        joints = cycle_links

    for target in targets:
        target._chain = tf.simplify_links(target._chain, keep_links=joints)

    joint_values = [l.param for l in joints]

    if tol is not None:
        warnings.warn(
            "The use of `tol` is depreciated"
            " and will be removed in scikit-bot v1.0."
            " Specify `atol` on the respective target instead.",
            DeprecationWarning,
        )
        for target in targets:
            target.atol = tol

    if weights is None:
        weights = [1 / len(targets)] * len(targets)
    weights = np.asarray(weights)

    step_fn = list()
    for target in targets:
        for joint in joints:
            stepper = None
            if (
                isinstance(target, PositionTarget)
                and isinstance(joint, tf.RotationalJoint)
                and target.static_frame.ndim == target.dynamic_frame.ndim
                and target.static_frame.ndim == 3
                and target.usage_count(joint) == 1
            ):
                stepper = analytic_rotation(joint, target)

            if stepper is None:
                stepper = step_generic_joint(joint, target, line_search_maxiter)

            step_fn.append(stepper)

    old_scores = np.array([float("inf")] * len(targets))
    atols = np.array([x.atol for x in targets])
    for step in range(maxiter * len(targets) * len(joints)):
        joint_idx = step % len(joints)
        residual = step % (len(joints) * len(targets))
        target_idx = residual // len(joints)
        iteration = step // (len(joints) * len(targets))

        if target_idx == 0 and joint_idx == 0:
            scores = np.array([x.score() for x in targets])

            if np.all(scores < atols):
                break

            if not any(old_scores - scores > rtol):
                raise RuntimeError(
                    "IK failed. Reason:"
                    " Loss in the local minimum is greater than `atol`."
                )

            old_scores = scores

        step_fn[len(joints) * target_idx + joint_idx]()
    else:
        raise RuntimeError(f"IK failed: maxiter exceeded.")

    for idx in range(len(joints)):
        joint_values[idx] = joints[idx].param

    return joint_values
