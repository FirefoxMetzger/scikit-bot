"""
:mod:`ropy.transform`
=====================

Manage n-dimensional coordinate transformations via directed graphs.

``ropy.transform`` allows you to express links (transformations) between frames
(coordinate systems) and transform vectors expressed in one frame into vectors
expressed in another frame. Each frame is modelled as a node in a directed
(cyclic) graph and a link is modelled as a directed edge between two nodes. To
compute a transformation, ``ropy.transform`` searches the graph for a suitable
transform chain - a sequence of links connecting the frames in question - and
iteratively applies the resulting chain to a vector. During this search
``ropy.transform`` assumes that the graph is consistent, i.e., if more than one
transform chain exists, they will yield the same result (up to numerical error).

If you come from a robotics background,this module is very similar to ROS tf2,
but works in (and between) n-dimensions. This means it naturally includes
projections - think a camera viewing a scene - and it offers more esoteric (less
common) transformations, e.g. `ropy.transform.reflect`.

Examples
--------

Manual construction of a 1D robot arm

>>> import ropy.transform as rtf
>>> import numpy as np
>>> # define the frames
>>> world_frame = rtf.Frame(ndim=2)
>>> ellbow_frame = rtf.Frame(2)
>>> tool_frame = rtf.Frame(2)
>>> # model the joint
>>> joint = rtf.affine.PlanarRotation(ellbow_frame, world_frame, (1, 0), (0, 1))
>>> # define the links
>>> tool_frame.add_link(rtf.affine.Fixed(tool_frame, ellbow_frame, lambda x: x + np.array((1, 0))))
>>> ellbow_frame.add_link(joint)
>>> # forward kinematics
>>> joint.angle = 0
>>> tool_frame.transform((0, 0), to_frame=world_frame)
>>> joint.angle = np.pi/2
>>> tool_frame.transform((0, 0), to_frame=world_frame)
"""

from .base import (
    Frame,
    Link,
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
