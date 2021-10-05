from .. import transform as tf
from numpy.typing import ArrayLike
from typing import List, Callable, Union
import numpy as np
from scipy.optimize import minimize_scalar
from scipy.optimize import OptimizeResult
from .targets import Target, PositionTarget, RotationTarget
from .types import IKJoint

import warnings


def step_generic_joint(joint: IKJoint, score: Callable, maxiter: int) -> float:
    """Find the optimal value for the current joint."""

    def generic_objective(x: float, current_joint: IKJoint) -> float:
        current_joint.param = x
        return score()

    def inner():
        result: OptimizeResult = minimize_scalar(
            lambda x: generic_objective(x, joint),
            bounds=(joint.lower_limit, joint.upper_limit),
            method="bounded",
            options={"maxiter": maxiter},
        )

        if not result.success:
            raise RuntimeError(f"IK failed. Reason: {result.message}")

        return result.x

    return inner


def ccd(
    targets: List[Target],
    joints: List[IKJoint] = None,
    *,
    metric: Callable[[np.ndarray, np.ndarray], float] = None,
    atol: float = 1e-3,
    rtol: float = 1e-6,
    maxiter: int = 500,
    line_search_maxiter: int = 500,
    weights: List[float] = None,
    tol: float = None,
    cycle_links: List[IKJoint] = None,
    pointA: Union[ArrayLike, List[ArrayLike]] = None,
    pointB: Union[ArrayLike, List[ArrayLike]] = None,
    frameA: Union[tf.Frame, List[tf.Frame]] = None,
    frameB: Union[tf.Frame, List[tf.Frame]] = None,
) -> List[np.ndarray]:
    """Cyclic Coordinate Descent.

    .. note::
        This function will modify the links given via ``joints`` as a side effect.

    This function cycles through ``joints`` and - one joint at a time - chooses
    a value for each joint that minimizes the scores of the available targets.

    .. versionchanged:: 0.10.0
        BREAKING CHANGE: The signature of ``ccd`` has changed. To keep using the old
        signature make each argument a keyword argument.
    .. versionchanged:: 0.10.0
        CCD can now jointly optimize for multiple targets.
    .. versionadded:: 0.7.0
        CCD was added to scikit-bot.

    Parameters
    ----------
    targets : List[Target]
        A list of quality measures that a successful pose minimizes.
    metric : Callable
        A function that takes two points (expressed in the corresponding frameB)
        and that computs the distance between them. Its signature is
        ``metric(transformed_point, pointB) -> distance``. If None, the
        euclidian distance will be used.
    atol : float
        Absolute tolerance above which the IK is considered to have failed.
        Default: ``1e-3``.
    rtol : float
        Relative tolerance for termination. Defaults to ``1e-6``.
    required_improvement : float
        The minimum required improvement of the objective after each iteration.
        If the improvement is less than this value, the algorithm fails and
        raises a value error. This is useful to avoid cases where the
        optimization gets stuck without finding a suitable pose.
    maxiter : int
        The maximum number of iterations.
    line_search_maxiter : int
        The maximum number of iterations to use when optimizing a single joint
        during a cycle, if no fast-path is implemented.
    weights : List[float]
        The relative weight to give to each quartet ``(pointA[i], pointB[i],
        frameA[i], frameB[i])``. If None, each element will have equal weight.
    cycle_links : List[IKJoint]
        .. deprecated:: 0.10.0
            Use ``joints`` instead.

        A list of 1DoF joints which should be adjusted to minimize targets.
    tol : float
        .. deprecated:: 0.10.0
            Use ``atol`` instead.

        Absolute tolerance for termination. Defaults to 0.001, which corresponds
        to 1 mm if the coordinate systems use meters as unit.
    pointA : ArrayLike
        .. deprecated:: 0.10.0
            Use ``targets`` and a ``CCDPositionTarget`` instead.

        A list of points. The i-th pointA is represented in the i-th frame of
        frameA. If only one point is given, the list can be omitted and the point
        can be directly used as input.
    pointB : ArrayLike
        .. deprecated:: 0.10.0
            Use ``targets`` and a ``CCDPositionTarget`` instead.

        The desired positions of each point given in pointA. The i-th pointB is
        represented in the i-th frame of frameB. If only one point is given, the
        list can be omitted and the point can be directly used as input.
    frameA : tf.Frame
        .. deprecated:: 0.10.0
            Use ``targets`` and a ``CCDPositionTarget`` instead.

        The frame in which the points in pointA are represented. The i-th
        element corresponds to the i-th pointA. If only one point is given, the
        list can be omitted and the frame can be directly used as input.
    frameB : tf.Frame
        .. deprecated:: 0.10.0
            Use ``targets`` and a ``CCDPositionTarget`` instead.

        The frame in which the points in pointB are represented. The i-th
        element corresponds to the i-th pointB. If only one point is given, the
        list can be omitted and the frame can be directly used as input.

    Returns
    -------
    joint_values : List[float]
        The final parameters of each joint.

    Notes
    -----
    Joint limits (min/max) are enforced as hard constraints.

    The current implementation is a naive python implementation and not very
    optimized. PRs improving performance are welcome :)

    """

    if cycle_links is not None:
        warnings.warn(
            "The use of `cycle_links` is depreciated"
            " and will be removed in scikit-bot v1.0."
            " Use `joints` instead.",
            DeprecationWarning,
        )
        joints = cycle_links

    joint_values = [l.param for l in joints]

    if tol is not None:
        warnings.warn(
            "The use of `tol` is depreciated"
            " and will be removed in scikit-bot v1.0."
            " Use `atol` instead.",
            DeprecationWarning,
        )
        atol = tol

    if metric is None:
        metric = lambda x, y: np.linalg.norm(x - y)

    if frameA is None:
        pass
    elif not (isinstance(frameA, list) or isinstance(frameA, tuple)):
        warnings.warn(
            "The use of `pointA`, `pointB`, `frameA`, and `frameB` is deprecated"
            " and will be removed in scikit-bot v1.0."
            " Use `targets` and `CCDPoseTarget` instead.",
            DeprecationWarning,
        )
        target = PositionTarget(
            static_position=np.asarray(pointA),
            dynamic_position=np.asarray(pointB),
            static_frame=frameA,
            dynamic_frame=frameB,
        )
        targets.append(target)
    else:
        warnings.warn(
            "The use of `pointA`, `pointB`, `frameA`, and `frameB` is deprecated"
            " and will be removed in scikit-bot v1.0."
            " Use `targets` and `CCDPoseTarget` instead.",
            DeprecationWarning,
        )
        for static, dynamic, static_frame, dynamic_frame in zip(
            pointA, pointB, frameA, frameB
        ):
            target = PositionTarget(
                static_position=np.asarray(static),
                dynamic_position=np.asarray(dynamic),
                static_frame=static_frame,
                dynamic_frame=dynamic_frame,
            )
            targets.append(target)

    if weights is None:
        weights = [1 / len(targets)] * len(targets)
    weights = np.asarray(weights)

    def total_score() -> float:
        scores = np.array([x.score() for x in targets])
        return np.mean(weights * scores)

    step_fn = list()
    for target in targets:
        for joint in joints:
            step_fn.append(step_generic_joint(joint, target.score, line_search_maxiter))

    old_distance = float("inf")
    for step in range(maxiter * len(targets) * len(joints)):

        joint_idx = step % len(joints)
        residual = step % (len(joints) * len(targets))
        target_idx = residual // len(joints)
        iteration = step // (len(joints) * len(targets))

        if target_idx == 0 and joint_idx == 0:
            distance = total_score()

            if distance <= atol:
                break

            if (old_distance - distance) < rtol:
                raise RuntimeError(
                    "IK failed. Reason:"
                    " Loss in the local minimum is greater than `atol`."
                )

            old_distance = distance

        step_joint = step_fn[len(joints) * target_idx + joint_idx]

        result = step_joint()

        joint = joints[joint_idx]
        joint.param = result
    else:
        raise RuntimeError(f"IK exceeded maxiter.")

    for idx in range(len(joints)):
        joint_values[idx] = joints[idx].param

    return joint_values
