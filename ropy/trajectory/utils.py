import numpy as np
from numpy.typing import ArrayLike


def discrete_integral(
    control_points: ArrayLike, t: ArrayLike = None, *, axis: int = 0
) -> float:
    """Estimate the integral along a curve.

    Estimates the integral of a time-parameterized curve along the chosen axis.
    The curve is given by a sequence of control points and the respective times
    when a control point is reached. The time need not be spaced out uniformly.

    Parameters
    ----------
    control_points : ArrayLike
        The values of the curve at time points t.
    t : ArrayLike
        The time points at which the curve was evaluated. If None, it will be
        set to ``np.linspace(0, 1, control_points.shape[axis])``.
    axis : int
        The axis along which to integrate. All other axes are
        treated as batch dimensions.

    Returns
    -------
    estimate : float
        The estimate of the integral under the curve.

    Notes
    -----
    The shapes of control_points and t must match or be broadcastable.

    """

    # This implementation uses the trapezoidal rule

    control_points = np.asarray(control_points)

    if t is None:
        t = np.linspace(0, 1, control_points.shape[axis])
    else:
        t = np.asarray(t)

    f_range = np.arange(control_points.shape[axis] - 1)
    f_lower = np.take(control_points, f_range, axis=axis)
    f_upper = np.take(control_points, f_range + 1, axis=axis)
    f_k = (f_lower + f_upper) / 2

    t_range = np.arange(t.shape[axis] - 1)
    t_lower = np.take(t, t_range, axis=axis)
    t_upper = np.take(t, t_range + 1, axis=axis)
    delta_t = t_upper - t_lower

    return np.sum(f_k * delta_t, axis=axis)
