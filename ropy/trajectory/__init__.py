"""
:mod:`ropy.trajectory`
========================

A collection of functions to compute positions along parameterized trajectories.
Here, trajectories are not limited to 3-dimensional space. Instead, they are
arbitrary mathematical paths with time parameterization. This means that a
trajectory may represent a sequence of positions in world space, but it may just 
as well represent a sequence of poses in joint space, or a sequence of
combined positions and velocities.

.. autofunction:: ropy.trajectory.linear
.. autofunction:: ropy.trajectory.spline

"""

from .spline import spline_trajectory
from .linear import linear_trajectory

__all__ = ["spline_trajectory", "linear_trajectory"]
