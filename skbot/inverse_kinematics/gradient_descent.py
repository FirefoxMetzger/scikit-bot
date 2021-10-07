from .. import transform as tf
from .targets import Target
from typing import List
import numpy as np
from .types import IKJoint
from scipy.optimize import minimize, OptimizeResult, Bounds


def gd(
    targets: List[Target],
    joints: List[IKJoint],
    *,
    atol: float = 1e-3,
    rtol: float = 1e-6,
    maxiter: int = 500,
):
    """L-BFGS-B based Gradient Descent

    .. note::
        This function will modify the links given via ``joints`` as a side effect.

    Use the gradient descent method specified by ``method`` to find values for
    ``joints`` that minimize ``targets``. The implementation relies on
    ``scipy.optimize``, and all methods that scipy supports are available.

    Parameters
    ----------
    targets : List[Target]
        A list of quality measures that a successful pose minimizes.
    joints : List[joint]
        A list of 1DoF joints which should be adjusted to minimize targets.
    jacobian : Callable
        A callable with signature `jacobian(np.ndarray) -> ArrayLike` that
        computes the robot's jacobi matrix at the respective position. The input
        will be an array of shape (len(joints),) and it should return an
        ArrayLike with shape (len(joints), len(joints)). If ``None`` (default)
        the jacobian will be approximated using a 2-point finite difference
        estimate.
    atol : float
        Absolute tolerance above which the IK is considered to have failed.
        Default: ``1e-3``.
    rtol : float
        Relative tolerance for termination. Defaults to ``1e-6``.
    maxiter : int
        The maximum number of iterations.

    Returns
    -------
    joint_values : List[float]
        The final parameters of each joint.

    Notes
    -----
    A common cause of IK faulure due to the chosen initial condition
    is too far away from the desired target position. One indicator for this
    is that :fun:`gd` converges based on ``rtol``, but the result doesn't fall
    under ``atol``.

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
        scores = np.array([x.score() for x in targets])
        normalized_scores = scores / atol
        return np.sum(normalized_scores)
        # return np.max(normalized_scores)

    result: OptimizeResult = minimize(
        objective_function,
        joint_values,
        bounds=bounds,
        method="L-BFGS-B",
        options={"maxiter": maxiter, "ftol": rtol},
    )

    if not result.success:
        raise RuntimeError(f"IK failed. Reason: {result.message}")

    scores = np.array([x.score() for x in targets])
    if np.any(scores > atols):
        raise RuntimeError(
            f"IK failed. Reason: Local minimum doesn't reach one or more targets."
        )

    for joint, value in zip(joints, result.x):
        joint.param = value

    joint_values = np.array([j.param for j in joints])
    return joint_values
