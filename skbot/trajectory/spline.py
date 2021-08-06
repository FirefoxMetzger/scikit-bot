import numpy as np
from scipy.interpolate import splprep, splev
from numpy.typing import ArrayLike
from typing import Optional


def spline_trajectory(
    t: ArrayLike,
    control_points: ArrayLike,
    *,
    t_control: Optional[ArrayLike] = None,
    degree: int = 3,
    t_min: float = 0,
    t_max: float = 1,
    derivative: int = 0,
) -> np.ndarray:
    """Evaluate the trajectory given by control_points at t using B-spline
    interpolation.

    ``spline_trajectory`` constructs a ``degree``-times differentiable
    trajectory using the given control points and then evaluates the resulting
    trajectory at ``t``. It does so using B-splines. By default, control points
    are spaced out evenly in the interval ``[t_min, t_max]`` where ``t=t_min``
    results in ``control_points[0]`` and ``t=t_max`` results in
    ``control_poins[-1]``. Alternatively, the spacing of control points can be
    set manually by specifying ``t_control``, which implicitly specifies
    ``t_min`` and ``t_max``.

    Parameters
    ----------
    t : np.ndarray
        An array containing positions at which to evaluate the trajectory.
        Elements of ``t`` must be within ``[t_min, t_max]``.
    control_points : np.ndarray
        A batch of control points used to construct the trajectory. The first
        dimension of the array is interpreted as batch dimension and the
        remaining dimensions are used to interpolate between. By default,
        control points are equally spaced within ``[t_min, t_max]`` unless
        ``t_control`` is given explicitly.
    t_control : np.ndarray, None
        A sequence of strictly increasing floats determining the position of the
        control points along the trajectory. None by default, which results in
        an equidistant spacing of points.
    degree : int
        The degree of the spline; uneven numbers are preferred. The resulting
        spline is k times continously differentiable.
    t_min : float
        Minimum value of the trajectories parametrization. Must be smaller than
        ``t_max``. If ``t_control`` is set, this value is ignored in favor of
        ``t_min=t_control[0]``
    t_max : float
        Maximum value of the trajectories parametrization. Must be larger than
        ``t_min``. If ``t_control`` is set, this value is ignored in favor of
        ``t_max=t_control[-1]``.
    derivative : int
        The derivative of the interpolated trajectory to compute. For example,
        ``derivative=2`` differentiates the trajectory twice with respect to
        ``t`` and then evaluates the derivative at the given ``t``.

    Returns
    -------
    position : np.ndarray
        The value of the trajectory at ``t``.

    Notes
    -----
    The dimension of the space embedding the trajectory must be less than 12,
    i.e. ``<= 11``, due to limitations in scipy. If more dimensions are needed,
    please open an issue; a workaround is to split the trajectory into chunks
    of less than 11 dimensions each.

    Repeated evaluation of single points on the trajectory, i.e. repeatedly
    calling this function with scalar ``t``, is possible, but will repeatedly
    reconstruct the trajectory, which can lead to unnecessary slowdown. For
    better performance, it is preferred to use an array-like ``t``.

    Examples
    --------

    .. plot::
        :include-source:

        >>> import numpy as np
        >>> import matplotlib.pyplot as plt
        >>> from skbot.trajectory import spline_trajectory
        >>> t1 = np.linspace(0, 2*np.pi, 10)
        >>> control_points = np.stack((np.cos(t1), np.sin(t1)), axis=1)
        >>> t2 = np.linspace(0, 2*np.pi, 100)
        >>> trajectory = spline_trajectory(t2, control_points, t_min=0, t_max=2*np.pi)
        >>> fig, ax = plt.subplots()
        >>> ax.plot(trajectory[:,0], trajectory[:,1], control_points[:,0], control_points[:,1], 'o')
        >>> fig.legend(('Trajectory', 'Control Points'))
        >>> plt.show()

    """
    t = np.asarray(t)
    control_points = np.asarray(control_points)

    if t_control is None:
        t_control = np.linspace(t_min, t_max, len(control_points), dtype=np.float_)
    else:
        t_control = np.asarray(t_control)
        t_min = t_control[0]
        t_max = t_control[-1]

    tck, u = splprep(control_points.T, u=t_control, s=0, ub=t_min, ue=t_max, k=degree)
    return np.stack(splev(t, tck, der=derivative, ext=2), axis=-1)
