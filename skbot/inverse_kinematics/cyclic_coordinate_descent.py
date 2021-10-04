from .. import transform as tf
from numpy.typing import ArrayLike
from typing import List, Callable, Union
import numpy as np
from scipy.optimize import minimize_scalar
from scipy.optimize import OptimizeResult
from .targets import Target, PositionTarget, RotationTarget

import warnings


joint_type = Union[tf.PrismaticJoint, tf.RotationalJoint]


def step_generic_joint(joint: joint_type, score: Callable, maxiter: int) -> float:
    """Find the optimal value for the current joint."""

    def generic_objective(x: float, current_joint: joint_type) -> float:
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
    cycle_links: List[joint_type],
    *,
    pointA: Union[ArrayLike, List[ArrayLike]] = None,
    pointB: Union[ArrayLike, List[ArrayLike]] = None,
    frameA: Union[tf.Frame, List[tf.Frame]] = None,
    frameB: Union[tf.Frame, List[tf.Frame]] = None,
    metric: Callable[[np.ndarray, np.ndarray], float] = None,
    tol: float = 1e-3,
    maxiter: int = 500,
    line_search_maxiter: int = 500,
    weights: List[float] = None,
) -> List[np.ndarray]:
    """Cyclic Coordinate Descent.

    .. note::
        This function will modify the links given via ``cycle_links`` as a side effect.

    .. versionchanged:: 0.10.0
        BREAKING CHANGE: The signature of ``ccd`` has changed. To keep using the old
        signature make each argument a keyword argument.
    .. versionchanged:: 0.10.0
        CCD can now jointly optimize for multiple targets.
    .. versionadded:: 0.7.0
        CCD was added to scikit-bot.

    This function adjusts the parameters of the links in ``cycle_links`` such that a
    point that has ``pointA`` as its representation in ``frameA`` has ``pointB``
    as representation in ``frameB``. Parameters are fitted in a cyclical
    fashion, i.e., by repeatedly iterating over ``cycle_links``. Each time the
    respective link's parameter is updated to minimize the distance between
    ``pointB`` and ``pointA``'s representation in ``frameB``. Distance is
    measured in frameB using euclidian distance or a custom metric if provided.

    Parameters
    ----------
    targets : List[CCDTarget]
        A list of targets that the resulting pose should reach.
    cycle_links : List[joint]
        A list of 1DoF joints which should be adjusted to make pointA and pointB
        valid representations of the same points.
    metric : Callable
        A function that takes two points (expressed in the corresponding frameB)
        and that computs the distance between them. Its signature is
        ``metric(transformed_point, pointB) -> distance``. If None, the
        euclidian distance will be used.
    tol : float
        Absolute tolerance for termination. Defaults to 0.001, which corresponds
        to 1 mm if the coordinate systems use meters as unit.
    maxiter : int
        The maximum number of cycles to perform.
    line_search_maxiter : int
        The maximum number of iterations to use when optimizing a single joint
        during a cycle.
    weights : List[float]
        The relative weight to give to each quartet ``(pointA[i], pointB[i],
        frameA[i], frameB[i])``. If None, each element will have equal weight.
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
    The number of elements given to ``pointA``, ``pointB``, ``frameA``, and
    ``frameB`` must match.

    Joint limits (min/max) are enforced as hard constraints.

    To specify both a position and orientation you can pass a list of two
    points. The second point expresses the orientation and *has unit
    length*. For example, to move a robot's tool frame to the target position
    ``(a, b, c)`` in the world_frame and align the frame's x-axis with the
    world's y-axis you could call::

        ik.ccd([(0, 0, 0), (1, 0, 0)], [(a, b, c), (0, 1, 0)],
               [tool_frame, tool_frame], [world_frame, world_frame])

    The current implementation is a naive python implementation and not very
    optimized. PRs improving performance are welcome :)

    """

    joint_values = [l.param for l in cycle_links]

    if metric is None:
        metric = lambda x, y: np.linalg.norm(x - y)

    if frameA is None:
        pass
    elif not (isinstance(frameA, list) or isinstance(frameA, tuple)):
        warnings.warn(
            "The use of `pointA`, `pointB`, `frameA`, and `frameB` is deprecated."
            " Use `targets` and `CCDPoseTarget` instead."
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
            "The use of `pointA`, `pointB`, `frameA`, and `frameB` is deprecated."
            " Use `targets` and `CCDPoseTarget` instead."
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
        return np.sum(weights * scores)

    step_fn = list()
    for target in targets:
        for joint in cycle_links:
            step_fn.append(step_generic_joint(joint, target.score, line_search_maxiter))

    for step in range(maxiter * len(targets) * len(cycle_links)):
        distance = total_score()
        if distance <= tol:
            break

        joint_idx = step % len(cycle_links)
        residual = step % (len(cycle_links) * len(targets))
        target_idx = residual // len(cycle_links)
        iteration = step // (len(cycle_links) * len(targets))

        if iteration % 10 == 0 and target_idx == 0 and joint_idx == 0:
            print(iteration, target_idx, joint_idx)

        step_joint = step_fn[len(cycle_links) * target_idx + joint_idx]

        result = step_joint()

        joint = cycle_links[joint_idx]
        joint.param = result
    else:
        raise RuntimeError(f"IK exceeded maxiter.")

    for idx in range(len(cycle_links)):
        joint_values[idx] = cycle_links[idx].param

    return joint_values
