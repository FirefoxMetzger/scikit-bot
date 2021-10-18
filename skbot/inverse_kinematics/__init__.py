"""
Inverse Kinematics (IK) Algorithms.

.. currentmodule:: skbot.inverse_kinematics

The algorithms in this module find values for a set of joints (a glorified list
of :class:`tf.Links <skbot.transform.Link>`) such that the score of one or more
Targets is below a given threshold.

Targets are specified between two :class:`tf.Frames <skbot.transform.Frame>`
that are connected by a sequence of :class:`tf.Links <skbot.transform.Link>`
(the kinematic chain). For example, the :class:`PositionTarget` can be used to
specify that a position in a robot's tool frame should have a certain position
when transformed into the world frame. The available IK algorithms will then
attempt to find values for the chosen joints - which are assumed to be between
these two frames - such that the value of the transformed tool position and the
value of the world position is closer than some threshold.

Targets
-------

.. autosummary::
    :toctree:

    PositionTarget
    RotationTarget

IK Algorithms
-------------

.. autosummary::
    :toctree:

    skbot.inverse_kinematics.ccd
    skbot.inverse_kinematics.gd

"""

from .targets import Target, PositionTarget, RotationTarget
from .cyclic_coordinate_descent import ccd
from .gradient_descent import gd

__all__ = ["ccd", "gd", "Target", "PositionTarget", "RotationTarget"]
