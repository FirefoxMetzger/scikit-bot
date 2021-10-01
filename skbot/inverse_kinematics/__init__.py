"""
Inverse Kinematics (IK) Algorithms.

The algorithms in this module assume that the environment is expressed as a
frame graph (see :mod:`skbot.transform`). Once this is done, the problem of
inverse kinematics can be neatly expressed as finding parameters for a set of
:class:`Links <skbot.transform.Link>` such that a point (or set of points,
depending on the algorithm) that has a certain representation in one frame has a
certain representation in another frame.

For example, for a robot like panda we know the tool position in the tool frame
(often 0), and we wish to change the joint angles (joints are
:class:`Links <skbot.transform.Link>`) such that the given position in the tool
frame coincides with a desired position in the world frame.

While using tool and world frame may be most common - after all it is textbook
IK -, this module is not limited to these frames. Any two frames that have (at
least) one valid :func:`transform chain <skbot.transform.Frame.links_between>`
between them that depends on the joints can be used. Expanding on the previous
example, we can specify IK between the camera frame of a static camera and
panda's tool frame.



Functions
---------

.. autosummary::
    :toctree:

    skbot.inverse_kinematics.ccd

"""

from .cyclic_coordinate_descent import ccd

__all__ = ["ccd"]
