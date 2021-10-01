from .. import transform as tf
from numpy.typing import ArrayLike
from typing import List, Callable, Union
import numpy as np
from scipy.optimize import minimize_scalar
from itertools import cycle
from scipy.optimize import OptimizeResult

joint = Union[tf.PrismaticJoint, tf.RotationalJoint]


def ccd(
    pointA: ArrayLike,
    pointB: ArrayLike,
    frameA: tf.Frame,
    frameB: tf.Frame,
    cycle_links: List[joint],
    *,
    metric: Callable[[np.ndarray, np.ndarray], float] = None,
    tol: float = 1e-3,
    maxiter: int = 500,
    line_search_maxiter: int = 500,
) -> List[np.ndarray]:
    """Cyclic Coordinate Descent.

    .. note::
        This function will modify the passed-in frame graph as a side effect.

    .. versionadded:: 0.7.0

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
        The representation of the point in frameA.
    pointB : ArrayLike
        The desired representation of the point in frameB.
    frameA : tf.Frame
        The frame in which pointA is represented.
    frameB : tf.Frame
        The frame in which pointB is represented.
    cycle_links: List[joint]
        A list of 1DoF joints which should be adjusted to make pointA and pointB
        valid representations of the same point.
    metric : Callable
        A function that takes two points (expressed in frameB) and computs the
        distance between them. Its signature is ``metric(transformed_point,
        pointB) -> distance``. If None, the euclidian distance will be used.
    tol : float
        Absolute tolerance for termination.
    maxiter : int
        The maximum number of cycles to perform.
    line_search_maxiter : int
        The maximum number of iterations to use when optimizing a single joint.

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

    joints = cycle(cycle_links)
    joint_values = [0] * len(cycle_links)

    if metric is None:
        metric = lambda x, y: np.linalg.norm(x - y)

    links = frameA.links_between(frameB)

    def optimizely(x, current_joint):
        current_joint.param = x

        current_point = pointA
        for link in links:
            current_point = link.transform(current_point)

        return metric(current_point, pointB)

    for _ in range(maxiter * len(cycle_links)):
        distance = metric(frameA.transform(pointA, frameB), pointB)

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
