import numpy as np
from scipy.interpolate import splprep, splev


def spline(
    t: np.array,
    control_points: np.array,
    *,
    t_control: np.array = None,
    degree: int = 3,
    t_min: float = 0,
    t_max: float = 1
) -> np.array:
    """Evaluate the trajectory given by control_points at t using B-spline
    interpolation.

    ``spline`` constructs a ``degree``-times differentiable trajectory using the
    given control points and then evaluates the resulting trajectory at ``t``.
    It does so using B-splines. By default, control points are spaced out evenly
    in the interval ``[t_min, t_max]`` where ``t=t_min`` results in
    ``control_points[0]`` and ``t=t_max`` results in ``control_poins[-1]``.
    Alternatively, the spacing of control points can be set manually by
    specifying ``t_k``. In this case, the inequality ``t_control[0] <= t_min <=
    t_max <= t_control[-1]`` must hold.

    Parameters
    ----------
    t : np.array
        An array containing positions at which to evaluate the trajectory.
        Elements of ``t`` must be within ``[t_min, t_max]``.
    control_points : np.array
        A batch of control points used to construct the trajectory. The first
        dimension of the array is interpreted as batch dimension and the
        remaining dimensions are used to interpolate between. By default,
        control points are equally spaced within ``[t_min, t_max]`` unless
        ``t_control`` is given explicitly.
    t_control : np.array, None
        A sequence of increasing floats determining the position of the control
        points along the trajectory. None by default, which results in an
        equidistant spacing of points. If set, the following inequality must
        hold ``t_control[0] <= t_min <= t_max <= t_control[-1]``.
    degree : int
        The degree of the spline; uneven numbers are preferred. The resulting
        spline is k times continously differentiable.
    t_min : float
        Minimum value of the trajectories parametrization. Must be smaller than
        ``t_max``.
    t_max : float
        Maximum value of the trajectories parametrization. Must be larger than
        ``t_min``.

    Returns
    -------
    position : np.array
        The value of the trajectory at position ``t``.

    Notes
    -----
    The dimension of the space embedding the trajectory must be less than 12,
    i.e. ``<= 11``, due to limitations in scipy.

    """
    t = np.asarray(t)
    control_points = np.asarray(control_points)

    if t_control is None:
        t_control = np.linspace(t_min, t_max, len(control_points), dtype=np.float_)
    else:
        t_control = np.asarray(t_control)

    tck, u = splprep(control_points.T, u=t_control, s=0, ub=t_min, ue=t_max, k=degree)
    return np.stack(splev(t, tck, ext=2), axis=0)
