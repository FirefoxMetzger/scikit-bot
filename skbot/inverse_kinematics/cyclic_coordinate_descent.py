from .. import transform as tf
from numpy.typing import ArrayLike
from typing import List, Callable, Union
import numpy as np
from scipy.optimize import minimize_scalar
from itertools import cycle
from scipy.optimize import OptimizeResult

joint = Union[tf.PrismaticJoint, tf.RotationalJoint]


def ccd(
    pointA: Union[ArrayLike, List[ArrayLike]],
    pointB: Union[ArrayLike, List[ArrayLike]],
    frameA: Union[tf.Frame, List[tf.Frame]],
    frameB: Union[tf.Frame, List[tf.Frame]],
    cycle_links: List[joint],
    *,
    metric: Callable[[np.ndarray, np.ndarray], float] = None,
    tol: float = 1e-3,
    maxiter: int = 500,
    line_search_maxiter: int = 500,
    weights: List[float] = None,
) -> List[np.ndarray]:
    """Cyclic Coordinate Descent.

    .. note::
        This function will modify the passed-in frame graph as a side effect.

    .. versionadded:: 0.8.1
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
    pointA : ArrayLike
        A list of points. The i-th pointA is represented in the i-th frame of
        frameA. If only one point is given, the list can be omitted and the point
        can be directly used as input.
    pointB : ArrayLike
        The desired positions of each point given in pointA. The i-th pointB is
        represented in the i-th frame of frameB. If only one point is given, the
        list can be omitted and the point can be directly used as input.
    frameA : tf.Frame
        The frame in which the points in pointA are represented. The i-th
        element corresponds to the i-th pointA. If only one point is given, the
        list can be omitted and the frame can be directly used as input.
    frameB : tf.Frame
        The frame in which the points in pointB are represented. The i-th
        element corresponds to the i-th pointB. If only one point is given, the
        list can be omitted and the frame can be directly used as input.
    cycle_links: List[joint]
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

    joints = cycle(cycle_links)
    joint_values = [l.param for l in cycle_links]

    if metric is None:
        metric = lambda x, y: np.linalg.norm(x - y)

    if not isinstance(frameA, list):
        frameA = [frameA]
        frameB = [frameB]
        pointA = [pointA]
        pointB = [pointB]

    pointA = [x for x in map(np.asarray, pointA)]
    pointB = [x for x in map(np.asarray, pointB)]

    targets = [
        (x[0], x[1], x[2].links_between(x[3]))
        for x in zip(pointA, pointB, frameA, frameB)
    ]

    if weights is None:
        weights = [1 / len(targets)] * len(targets)

    def score() -> float:
        scores = np.empty((len(targets),), dtype=np.float_)
        for idx in range(len(targets)):
            current_point, target_point, chain = targets[idx]
            for link in chain:
                current_point = link.transform(current_point)
            scores[idx] = metric(current_point, target_point)

        return np.sum(weights * scores)

    def optimizely(x: float, current_joint: joint) -> float:
        current_joint.param = x
        return score()

    for _ in range(maxiter * len(cycle_links)):
        distance = score()

        if distance <= tol:
            break

        current_joint = next(joints)

        result: OptimizeResult = minimize_scalar(
            lambda x: optimizely(x, current_joint),
            bounds=(current_joint.lower_limit, current_joint.upper_limit),
            method="bounded",
            options={"maxiter": line_search_maxiter},
        )

        if not result.success:
            raise RuntimeError(f"IK failed. Reason: {result.message}")

        current_joint.param = result.x
    else:
        raise RuntimeError(f"IK exceeded maxiter.")

    for idx in range(len(cycle_links)):
        joint_values[idx] = cycle_links[idx].param

    return joint_values
