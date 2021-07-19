from math import tan
import numpy as np
from numpy.typing import ArrayLike

from ..transform.base import Link
from ..transform.projections import PerspectiveProjection
from ..transform.affine import Translation


class FrustumProjection(Link):
    """Frustum based intrinsic camera transformation

    This links behavior is identical to
    :class:`ropy.transform.FrustumProjection`; however, here the camera points
    along the x-axis instead of the z-axis. This is done to match the behavior
    of ignition, which applies the robotic coordinate frame standard instead of
    the computer vision standard here.

    Parameters
    ----------
    hfov : float
        The angle of the viewing frustum in radians. It is assumed to be less than
        pi (180°).
    image_shape : ArrayLike
        The shape (height, width) of the image plane in pixels.

    See Also
    --------
    :class:`ropy.transform.FrustumProjection`

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
        amounts = np.array(
            [[1 / (tan(hfov / 2)), 0, 0], [aspect_ratio * 1 / (tan(hfov / 2)), 0, 0]]
        )
        directions = np.array([[0, 2 / image_shape[0], 0], [0, 0, 2 / image_shape[1]]])

        self.proj = PerspectiveProjection(directions, amounts, axis=-1)
        self.tf = Translation(image_shape / 2)

    def transform(self, x: ArrayLike) -> np.ndarray:
        x_projected = self.proj.transform(x)
        x_transformed = self.tf.transform(x_projected)
        return x_transformed
