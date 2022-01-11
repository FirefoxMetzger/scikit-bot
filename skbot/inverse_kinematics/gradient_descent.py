from .. import transform as tf
from .targets import Target
from typing import List
import numpy as np
from scipy.optimize import minimize, OptimizeResult, Bounds
import warnings


def gd(
    targets: List[Target],
    joints: List[tf.Joint],
    *,
    rtol: float = 1e-6,
    maxiter: int = 500,
):
    """L-BFGS-B based Gradient Descent.

    .. note::
        This function will modify the objects in ``joints`` as a side effect.

    Use L-BFGS-B to find values for ``joints`` such that the sum of all target
    scores is minimal. L-BFGS-B is a quasi-Newton method that approximates both
    the targets Jacobian and Hessian.

    Parameters
    ----------
    targets : List[Target]
        A list of quality measures that a successful pose minimizes.
    joints : List[joint]
        A list of 1DoF joints which should be adjusted to minimize ``targets``.
    rtol : float
        Relative tolerance for termination. If, after one iteration, the sum of
        scores has not improved by more than rtol the algorithm terminates and
        assumes that a local optimum has been found.
    maxiter : int
        The maximum number of iterations to perform.

    Returns
    -------
    joint_values : List[float]
        The final parameters of each joint.

    Notes
    -----
    Joint limits (min/max) are enforced as hard constraints throughout the
    optimization.

    A common cause of IK faulure is that the chosen initial condition is too far
    away from the desired target position. One indicator for this is that
    :func:`gd` converges based on ``rtol``, but the score of one or more targets
    isn't below ``atol``.

    """

    joint_values = np.array([l.param for l in joints])

    for target in targets:
        target._chain = tf.simplify_links(target._chain, keep_links=joints)

    atols = np.array([x.atol for x in targets])
    bounds = Bounds(
        [x.lower_limit for x in joints],
        [x.upper_limit for x in joints],
        keep_feasible=True,
    )

    def objective_function(joint_config: np.ndarray) -> float:
        for joint, value in zip(joints, joint_config):
            joint.param = value
        normalized_scores = np.array([x.score() / x.atol for x in targets])
        return np.sum(normalized_scores)
        # return np.max(normalized_scores)

    # check if optimization is needed
    skip = False
    for target in targets:
        if target.score() > target.atol:
            break
    else:
        skip = True

    if not skip:
        result: OptimizeResult = minimize(
            objective_function,
            joint_values,
            bounds=bounds,
            method="L-BFGS-B",
            options={"maxiter": maxiter, "ftol": rtol},
        )

        if not result.success:
            warnings.warn(
                f"L-BFGS-B terminated abnormally with message `{result.message}`."
            )

        scores = np.array([x.score() for x in targets])
        if np.any(scores > atols):

            raise RuntimeError(
                f"IK failed. Reason: Local minimum doesn't reach one or more targets."
            )

        for joint, value in zip(joints, result.x):
            joint.param = value

    joint_values = np.array([j.param for j in joints])
    return joint_values
