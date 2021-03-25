import numpy as np
from scipy.interpolate import interp1d


def linear(t, control_points, *, t_control=None, t_min=0, t_max=1):
    """Evaluate the trajectory given by control_points at t using linear
    interpolation.

    ``linear`` constructs a piece-wise linear trajectory using the given control
    points and then evaluates the resulting trajectory at ``t``. By default,
    control points are spaced out evenly in the interval ``[t_min, t_max]``
    where ``t=t_min`` results in ``control_points[0]`` and ``t=t_max`` results
    in ``control_poins[-1]``. Alternatively, the spacing of control points can
    be set via ``t_control``. In this case, the inequality ``t_control[0] <=
    t_min <= t_max <= t_control[-1]`` must hold.

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
        A sequence of strictly increasing floats determining the position of the
        control points along the trajectory. None by default, which results in
        an equidistant spacing of points. If set, the following inequality must
        hold ``t_control[0] <= t_min <= t_max <= t_control[-1]``.
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

    """

    t = np.asarray(t)
    control_points = np.asarray(control_points)

    if t_control is None:
        t_control = np.linspace(t_min, t_max, len(control_points), dtype=np.float_)
    else:
        t_control = np.asarray(t_control)

    position = interp1d(t_control, control_points, axis=0)(t)
    
    return position
