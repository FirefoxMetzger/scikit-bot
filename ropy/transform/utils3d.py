from math import tan, sin, cos
import numpy as np
from numpy.typing import ArrayLike
from scipy.spatial.transform import Rotation as scipy_rotation

from .base import Link
from .projections import PerspectiveProjection
from .affine import Translation, Rotation
from ._utils import angle_between, vector_project


class EulerRotation(Rotation):
    """Rotation based on Euler angles in 3D.

    Parameters
    ----------
    sequence : str
        Specifies sequence of axes for rotations. Up to 3 characters belonging
        to the set {‘X’, ‘Y’, ‘Z’} for intrinsic rotations, or {‘x’, ‘y’, ‘z’}
        for extrinsic rotations. Extrinsic and intrinsic rotations cannot be
        mixed in one function call.
    angles : ArrayLike
        Euler angles specified in radians (degrees is False) or degrees (degrees
        is True). Each value of angles corresponds to the respective angle
        listed in ``sequence``.
    degrees : bool
        If True, angles are assumed to be in degrees. Default is False.
    """

    def __init__(
        self, sequence: str, angles: ArrayLike, *, degrees: bool = False
    ) -> None:
        rot = scipy_rotation.from_euler(sequence, angles, degrees)

        rotvec = rot.as_rotvec()
        angle = rot.magnitude()

        # arbitrary vector that isn't parallel to rotvec
        tmp_vector = np.array((1, 0, 0), dtype=np.float_)
        enclosing_angle = abs(angle_between(tmp_vector, rotvec))
        if enclosing_angle < np.pi / 4 or abs(enclosing_angle - np.pi) < np.pi / 4:
            tmp_vector = np.array((0, 1, 0), dtype=np.float_)

        vec_u = tmp_vector - vector_project(tmp_vector, rotvec)
        basis2 = np.cross(vec_u, rotvec)
        basis2 /= np.linalg.norm(basis2)

        vec_v = cos(angle / 2) * vec_u + sin(angle / 2) * basis2

        super().__init__(vec_u, vec_v)


class QuaternionRotation(Rotation):
    """Rotation based on Quaternions in 3D.

    Parameters
    ----------
    quaternion : ArrayLike
        A (possibly non-unit norm) quaternion in ``sequence`` format. It will be
        normalized to unit norm.
    sequence : str
        Specifies the order of parameters in the quaternion. Possible values are
        ``"xyzw"`` (default), i.e., scalar-last, or "wxyz", i.e., scalar-first.
    """

    def __init__(self, quaternion: ArrayLike, *, sequence: str = "xyzw") -> None:

        quaternion = np.asarray(quaternion)

        if sequence == "xyzw":
            pass
        elif sequence == "wxyz":
            quaternion = quaternion[[1, 2, 3, 0]]
        else:
            raise ValueError(
                "Invalid value for sequence. Possible values are 'xyzw' or 'wxyz'."
            )

        rot = scipy_rotation.from_quat(quaternion)

        rotvec = rot.as_rotvec()
        angle = rot.magnitude()

        # arbitrary vector that isn't parallel to rotvec
        tmp_vector = np.array((1, 0, 0), dtype=np.float_)
        enclosing_angle = abs(angle_between(tmp_vector, rotvec))
        if enclosing_angle < np.pi / 4 or abs(enclosing_angle - np.pi) < np.pi / 4:
            tmp_vector = np.array((0, 1, 0), dtype=np.float_)

        vec_u = tmp_vector - vector_project(tmp_vector, rotvec)
        basis2 = np.cross(vec_u, rotvec)
        basis2 /= np.linalg.norm(basis2)

        vec_v = cos(angle / 2) * vec_u + sin(angle / 2) * basis2

        super().__init__(vec_u, vec_v)


class FrustumProjection(Link):
    """Frustum based intrinsic camera transformation.

    This link computes the 2D camera/pixel position of a point in 3D (world)
    space. The projection's center point is located in the origin and the camera
    is pointing along the positive z-axis. The origin of the pixel frame is
    located at the top left corner of the image with the y-axis pointing down
    and the x-axis pointing right. Points along the z-axis are projected into
    the center of the image (``image_shape/2``).


    Parameters
    ----------
    hfov : float
        The angle of the viewing frustum in radians. It is assumed to be less than
        pi (180°).
    image_shape : ArrayLike
        The shape (height, width) of the image plane in pixels.

    See Also
    --------
    :class:`ropy.ignition.FrustumProjection`

    Notes
    -----
    This function assumes that ``hfov`` is less than pi (180°).

    Points outside the viewing frustum will still be projected. While most will
    be mapped into points outside of ``image_shape``, points on the backside of
    the camera may alias with points inside the image. In this case special care
    must be taken.
    """

    def __init__(self, hfov: float, image_shape: ArrayLike) -> None:
        super().__init__(3, 2)

        image_shape = np.asarray(image_shape)

        aspect_ratio = image_shape[1] / image_shape[0]
        amounts = np.array(
            [[0, 0, 1 / (tan(hfov / 2))], [0, 0, aspect_ratio * 1 / (tan(hfov / 2))]]
        )
        directions = np.array([[0, 2 / image_shape[0], 0], [2 / image_shape[1], 0, 0]])

        self.proj = PerspectiveProjection(directions, amounts, axis=-1)
        self.tf = Translation(image_shape / 2)

    def transform(self, x: ArrayLike) -> np.ndarray:
        x_projected = self.proj.transform(x)
        x_transformed = self.tf.transform(x_projected)
        return x_transformed
