"""
:mod:`ropy.transform`
=====================

Manage n-dimensional coordinate transformations via directed graphs.

``ropy.transform`` allows you to change the representation of a vector from one
coordinate system to another, i.e., it transforms the basis of the vector.
Contrary to similar libraries, this is not limited to 3D or affine
transformations, but can transform in N dimensions and between different
dimensions, too. Additionally, you can create chains - more precisely directed
graphs - of transformations between different frames, which allows you to
express quite complicated transformations.

If you come from a robotics background, this module is very similar to ROS tf2,
but works in (and between) n-dimensions. This means it naturally includes
projections, e.g. world space to pixel space, and it allows you to use more
esoteric transformations like spherical coordinates, too.


Examples
--------

Manual construction of a 1D robot arm

>>> import ropy.transform as rtf
>>> import numpy as np
>>> arm_link = rtf.affine.Translation((1, 0))
>>> arm_joint = rtf.affine.Rotation((1, 0), (0, 1))

>>> tool_frame = rtf.Frame(2)
>>> ellbow_frame = arm_link(tool_frame)
>>> world_frame = arm_joint(ellbow_frame)

>>> arm_joint.angle = 0
>>> tool_pos = tool_frame.transform((0, 0), to_frame=world_frame)
>>> assert np.allclose(tool_pos, (1, 0))

>>> arm_joint.angle = np.pi / 2
>>> tool_pos = tool_frame.transform((0, 0), to_frame=world_frame)
>>> assert np.allclose(tool_pos, (0, 1))

As with any other repository, you can always find more examples by exploring
the accompanying unit tests.
"""

from .base import (
    Frame,
    Link,
    CustomLink,
    homogenize,
    cartesianize,
    normalize_scale,
    rotation_matrix,
)

from .functions import (
    # basic transformations
    translate,
    rotate,
    reflect,
    shear,
    scale,
)

from .coordinates import transform, inverse_transform, transform_between
from . import affine, coordinates, projections
from .projections import perspective_frustum


__all__ = [
    # Core Classes for Frame Management
    "Frame",
    "Link",
    "CustomLink",
    "affine",
    "coordinates",
    "projections",
    # basic transformation functions
    "translate",
    "rotate",
    "reflect",
    "shear",
    "scale",
    # legacy functions (to be refactored)
    "homogenize",
    "cartesianize",
    "transform",
    "inverse_transform",
    "transform_between",
    "perspective_frustum",
    "rotation_matrix",
]
