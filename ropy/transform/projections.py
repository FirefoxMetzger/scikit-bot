from math import tan
from typing import Tuple

import numpy as np

from .coordinates import transform


def perspective_frustum(hfov: float, image_shape: Tuple[int, int]) -> np.ndarray:
    """Compute a projection matrix (3D -> 2D) from a viewing frustum.

    Given a perspective camera system with known horizontal vield of view
    (``hfov``) and pixel density (``image_shape``), compute a transformation
    that projects scale normalized camera coordinates to image coordinates.

    In more detail this takes point in (3d) world space that is described in the
    camera's coordinate system (using scale-normalized homogeneous coordinates)
    and projects it onto the camera's (2d) image that is described in the
    image's coordinate system (using homogeneous coordinates).

    The camera's coordinate system follows the robot joint convention. This
    means that it is assumed that the x-axis is pointing forward (in the
    direction of the imager), the y-axis is pointing left, and the z-axis is
    pointing up. This is the same convention used by Ignition and Gazebo.

    The image's coordinate system has it's origin in the top left corner of the
    image with the x-axis pointing right and the y-axis pointing down. It sits
    in the y-z-plane of the camera's coordinate system, with the camera frames
    origin being positioned in the center of the image. This means that the

    Parameters
    ----------
    hfov : float
        The camera's horizontal field of view in radians within the
        interval (0, 2pi) image_shape: Tuple[int, int] The shape of the image
        produced by the camera as ``(height, width)``.
    image_shape : Tuple[int, int]
        The number of pixels in the image given as a (height, width) tuple.

    Returns
    -------
    projection_matrix : np.ndarray
        The matrix describing the projection.

    Notes
    -----
    To index the image with the result of this projection, you may need to swap
    the order of the elements to (y, x).
    """

    height, width = image_shape
    aspect_ratio = width / height
    scale = 2 * tan(hfov / 2)

    # translate to origin of image frame
    translation = np.array(
        [
            [1, 0, 0, 0],
            [-tan(hfov / 2), 1, 0, 0],
            [-tan(hfov / 2) / aspect_ratio, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )

    # rotate to image frame
    rotate_frame = np.array([[0, -1, 0, 0], [0, 0, -1, 0], [1, 0, 0, 0], [0, 0, 0, 1]])

    # project to 2D
    camera_matrix = np.array([[width, 0, 0, 0], [0, width, 0, 0], [0, 0, scale, 0]])

    return np.matmul(camera_matrix, np.matmul(rotate_frame, translation))
