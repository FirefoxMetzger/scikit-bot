import numpy as np
from scipy.interpolate import interp1d
from numpy.typing import ArrayLike
from typing import Optional


def linear_trajectory(
    t: ArrayLike,
    control_points: ArrayLike,
    *,
    t_control: Optional[ArrayLike] = None,
    t_min: float = 0,
    t_max: float = 1
) -> np.ndarray:
    """Evaluate the trajectory given by control_points at t using linear
    interpolation.

    ``linear_trajectory`` constructs a piece-wise linear trajectory using the
    given control points and then evaluates the resulting trajectory at ``t``.
    By default, control points are spaced out evenly in the interval ``[t_min,
    t_max]`` where ``t=t_min`` results in ``control_points[0]`` and ``t=t_max``
    results in ``control_poins[-1]``. Alternatively, the spacing of control
    points can be controlled manually by specifying ``t_control``, which
    implicitly specifies ``t_min`` and ``t_max``.

    Parameters
    ----------
    t : ArrayLike
        An array containing positions at which to evaluate the trajectory.
        Elements of ``t`` must be within ``[t_min, t_max]``.
    control_points : ArrayLike
        A batch of control points used to construct the trajectory. The first
        dimension of the array is interpreted as batch dimension and the
        remaining dimensions are used to interpolate between. By default,
        control points are equally spaced within ``[t_min, t_max]`` unless
        ``t_control`` is given explicitly.
    t_control : ArrayLike
        A sequence of strictly increasing floats determining the position of the
        control points along the trajectory. None by default, which results in
        an equidistant spacing of points.
    t_min : float
        Minimum value of the trajectories parametrization. Must be smaller than
        ``t_max``.If ``t_control`` is set, this value is ignored in favor of
        ``t_min=t_control[0]``.
    t_max : float
        Maximum value of the trajectories parametrization. Must be larger than
        ``t_min``. If ``t_control`` is set, this value is ignored in favor of
        ``t_max=t_control[-1]``.

    Returns
    -------
    position : ArrayLike
        The value of the trajectory at ``t``.

    Notes
    -----
    Repeated evaluation of single points on the trajectory, i.e. repeatedly
    calling this function with a scalar ``t``, is possible, but will repeatedly
    reconstruct the trajectory, which can lead to unnecessary slowdown. For
    better performance, it is preferred to use an array-like ``t``.

    Examples
    --------

    .. plot::
        :include-source:

        >>> import numpy as np
        >>> import matplotlib.pyplot as plt
        >>> from skbot.trajectory import linear_trajectory
        >>> t1 = np.linspace(0, 2*np.pi, 10)
        >>> control_points = np.stack((np.cos(t1), np.sin(t1)), axis=1)
        >>> t2 = np.linspace(0, 2*np.pi, 100)
        >>> trajectory = linear_trajectory(t2, control_points, t_min=0, t_max=2*np.pi)
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
        t_max = t_control[1]

    position = interp1d(t_control, control_points, axis=0)(t)

    return position
