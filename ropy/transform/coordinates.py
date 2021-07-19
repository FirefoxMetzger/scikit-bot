import numpy as np
from numpy.typing import ArrayLike


from .base import rotation_matrix, Frame
from .affine import Translation
from .utils3d import EulerRotation


def transform(new_frame: ArrayLike) -> np.ndarray:
    """Compute the homogeneous transformation matrix from the current coordinate
    system into a new coordinate system.

    Given the pose of the new reference frame ``new_frame`` in the current
    reference frame, compute the homogeneous transformation matrix from the
    current reference frame into the new reference frame.
    ``transform(new_frame)`` can, for example, be used to get the transformation
    from the corrdinate frame of the current link in a kinematic chain to the
    next link in a kinematic chain. Here, the next link's origin (``new_frame``)
    is specified relative to the current link's origin, i.e., in the current
    link's coordinate system.


    Parameters
    ----------
    new_frame : np.ndarray
        The pose of the new coordinate system's origin. This is a 6-dimensional
        vector consisting of the origin's position and the frame's orientation
        (xyz Euler Angles): [x, y, z, alpha, beta, gamma].

    Returns
    -------
    transformation_matrix : np.ndarray
        A 4x4 matrix representing the homogeneous transformation.


    Notes
    -----
    For performance reasons, it is better to sequentially apply multiple
    transformations to a vector than to first multiply a sequence of
    transformations and then apply them to a vector afterwards.

    """
    new_frame = np.asarray(new_frame)

    child = Frame(3)
    if np.any(new_frame[3:] != 0):
        tmp = EulerRotation("xyz", new_frame[3:])(child)
    else: 
        tmp = child
    parent = Translation(new_frame[:3])(tmp)
    
    return parent.get_affine_matrix(child)


def inverse_transform(old_frame: ArrayLike) -> np.ndarray:
    """Compute the homogeneous transformation matrix from the current coordinate
    system into the old coordinate system.

    Given the pose of the current reference frame in the old reference frame
    ``old_frame``, compute the homogeneous transformation matrix from the new
    reference frame into the old reference frame. For example,
    ``inverse_transform(camera_frame)`` can, be used to compute the
    transformation from a camera's coordinate frame to the world's coordinate
    frame assuming the camera frame's pose is given in the world's coordinate
    system.

    Parameters
    ----------
    old_frame : {np.ndarray, None}
        The pose of the old coordinate system's origin. This is a 6-dimensional
        vector consisting of the origin's position and the frame's orientation
        (xyz Euler Angles): [x, y, z, alpha, beta, gamma].

    Returns
    -------
    transformation_matrix : np.ndarray
        A 4x4 matrix representing the homogeneous transformation.


    Notes
    -----
    For performance reasons, it is better to sequentially apply multiple
    transformations to a vector than to first multiply a sequence of
    transformations and then apply them to a vector afterwards.

    """

    # Note: this is a naive implementation, but avoids a scipy dependency
    # if scipy does get introduced later, it can be substituted by
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.transform.Rotation.from_euler.html

    old_frame = np.asarray(old_frame)

    child = Frame(3)
    if np.any(old_frame[3:] != 0):
        tmp = EulerRotation("xyz", old_frame[3:])(child)
    else: 
        tmp = child
    parent = Translation(old_frame[:3])(tmp)
    
    return child.get_affine_matrix(parent)


def transform_between(old_frame: ArrayLike, new_frame: ArrayLike) -> np.ndarray:
    """Compute the homogeneous transformation matrix between two frames.

    ``transform_between(old_frame, new_frame)`` computes the
    transformation from the corrdinate system with pose ``old_frame`` to
    the corrdinate system with pose ``new_frame`` where both origins are
    expressed in the same reference frame, e.g., the world's coordinate frame.
    For example, ``transform_between(camera_frame, tool_frame)`` computes
    the transformation from a camera's coordinate system to the tool's
    coordinate system assuming the pose of both corrdinate frames is given in
    a shared world frame (or any other __shared__ frame of reference).

    Parameters
    ----------
    old_frame : np.ndarray
        The pose of the old coordinate system's origin. This is a 6-dimensional
        vector consisting of the origin's position and the frame's orientation
        (xyz Euler Angles): [x, y, z, alpha, beta, gamma].
    new_frame : np.ndarray
        The pose of the new coordinate system's origin. This is a 6-dimensional
        vector consisting of the origin's position and the frame's orientation
        (xyz Euler Angles): [x, y, z, alpha, beta, gamma].

    Returns
    -------
    transformation_matrix : np.ndarray
        A 4x4 matrix representing the homogeneous transformation.

    Notes
    -----
    If the reference frame and ``old_frame`` are identical, use ``transform``
    instead.

    If the reference frame and ``new_frame`` are identical, use
    ``transformInverse`` instead.

    For performance reasons, it is better to sequentially apply multiple
    transformations to a vector than to first multiply a sequence of
    transformations and then apply them to a vector afterwards.

    """

    return transform(new_frame) @ inverse_transform(old_frame)
