from math import tan
import numpy as np
from numpy.typing import ArrayLike

from ..transform.utils3d import FrustumProjection, EulerRotation
from ..transform.base import Link


class FrustumProjection(FrustumProjection):
    """Frustum based intrinsic camera transformation

    This links behavior is identical to
    :class:`skbot.transform.FrustumProjection`; however, here the camera points
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
    :class:`skbot.transform.FrustumProjection`

    Notes
    -----
    This function assumes that ``hfov`` is less than pi (180°).

    Points outside the viewing frustum will still be projected; however, their values lie
    outside the applicable pixel range.

    """

    def __init__(self, hfov: float, image_shape: ArrayLike) -> None:
        super().__init__(hfov, image_shape)

        self.initial_rotation = EulerRotation("yz", (-90, 90), degrees=True)

    def transform(self, x: ArrayLike) -> np.ndarray:
        x = self.initial_rotation.transform(x)
        return super().transform(x)
