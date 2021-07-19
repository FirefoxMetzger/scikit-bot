from typing import Tuple
from math import tan
import numpy as np
from numpy.typing import ArrayLike

from .base import Link
from .projections import NDPerspectiveProjection
from .affine import Translation


class FrustumProjection(Link):
    """Frustum based intrinsic camera transformation (world2px)
    
    This link computes the 2D camera/pixel position of a point in 3D (world)
    space. The projection's center point is located in the origin and the camera
    is pointing along the positive z-axis.

    Parameters
    ----------
    hfov : float
        The angle of the viewing frustum in radians. It is assumed to be less than
        pi (180°).
    image_shape : ArrayLike
        The shape (height, width) of the image plane in pixels.
    
    Notes
    -----
    This function assumes that ``hfov`` is less than pi (180°).

    Points outside the viewing frustum will still be projected; however, their values lie
    outside the applicable pixel range.
    """

    def __init__(self, hfov: float, image_shape: ArrayLike) -> None:
        super().__init__(3, 2)

        image_shape = np.asarray(image_shape)

        aspect_ratio = image_shape[1] / image_shape[0]
        amounts = np.array([
            [0, 0, 1/(tan(hfov / 2))],
            [0, 0, aspect_ratio * 1/(tan(hfov / 2))]
        ])
        directions = np.array([[0, 2 / image_shape[0], 0], [2 / image_shape[1], 0, 0]])

        self.proj = NDPerspectiveProjection(directions, amounts, axis=-1)
        self.tf = Translation(image_shape/2)


    def transform(self, x: ArrayLike) -> np.ndarray:
        x_projected = self.proj.transform(x)
        x_transformed = self.tf.transform(x_projected)
        return x_transformed


