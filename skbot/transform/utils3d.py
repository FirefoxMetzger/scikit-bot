from math import tan
import numpy as np
from numpy.typing import ArrayLike
from scipy.spatial.transform import Rotation as scipy_rotation

from .base import Link
from .projections import PerspectiveProjection
from .affine import AffineCompound, Translation, Rotation
from ._utils import angle_between, vector_project


class RotvecRotation(Rotation):
    """Rotation based on rotation vector in 3D.

    Parameters
    ----------
    rotvec : ArrayLike
        The vector around which points are rotated.
    angle : ArrayLike
        The magnitude of the rotation. If None, the length of ``vector`` will be
        used.
    degrees : bool
        If True, angle is assumed to be in degrees. Default is False.
    axis : int
        The axis along which to to compute. Default: -1.

    Notes
    -----
    Batch dimensions of ``rotvec`` and ``angle`` must be broadcastable.
    """

    def __init__(
        self,
        rotvec: ArrayLike,
        *,
        angle: ArrayLike = None,
        degrees: bool = False,
        axis: int = -1
    ) -> None:

        rotvec = np.asarray(rotvec)
        rotvec = np.moveaxis(rotvec, axis, -1)

        if angle is None:
            angle = np.linalg.norm(rotvec, axis=axis, keepdims=True)
            angle = np.moveaxis(angle, axis, -1)
        else:
            angle = np.asarray(angle)
            if angle.ndim > 0:
                angle = np.moveaxis(angle, axis, -1)[..., None]

        if degrees:  # make radians
            angle = angle / 360 * 2 * np.pi

        # arbitrary vector that isn't parallel to rotvec
        alternativeA = np.zeros_like(rotvec)
        alternativeA[..., :] = (1, 0, 0)
        alternativeB = np.zeros_like(rotvec)
        alternativeB[..., :] = (0, 1, 0)

        enclosing_angle = np.abs(angle_between(alternativeA, rotvec))[..., None]
        switch_vectors = (enclosing_angle < (np.pi / 4)) | (
            abs(enclosing_angle - np.pi) < (np.pi / 4)
        )
        arbitrary_vector = np.where(switch_vectors, alternativeB, alternativeA)

        vec_u = arbitrary_vector - vector_project(arbitrary_vector, rotvec)
        vec_u /= np.linalg.norm(vec_u, axis=-1, keepdims=True)
        basis2 = np.cross(vec_u, rotvec, axisa=-1, axisb=-1, axisc=-1)
        basis2 /= np.linalg.norm(basis2, axis=-1, keepdims=True)

        super().__init__(vec_u, basis2)

        self.angle = angle


class EulerRotation(AffineCompound):
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
    axis : int
        The axis along which to to compute. Default: -1.
    """

    def __init__(
        self, sequence: str, angles: ArrayLike, *, degrees: bool = False, axis: int = -1
    ) -> None:
        angles = np.asarray(angles)
        if angles.ndim == 0:
            angles = angles[None, ...]

        angles = np.moveaxis(angles, axis, 0)
        rotations = list()
        for idx, char in enumerate(sequence):
            angle: np.ndarray = angles[idx, ...]
            if char in ["x", "X"]:
                rotvec = np.array((1, 0, 0), dtype=np.float_)
            elif char in ["y", "Y"]:
                rotvec = np.array((0, 1, 0), dtype=np.float_)
            elif char in ["z", "Z"]:
                rotvec = np.array((0, 0, 1), dtype=np.float_)
            else:
                raise ValueError("Unknown axis '{char}' in rotation sequence.")

            rotvec = np.broadcast_to(rotvec, (*angle.shape, 3))
            rotvec = np.moveaxis(rotvec, -1, axis)
            rot = RotvecRotation(rotvec, angle=angle, degrees=degrees, axis=axis)
            rotations.append(rot)

        if sequence.islower():
            super().__init__(rotations)
        elif sequence.isupper():
            rotations = [x for x in reversed(rotations)]
            super().__init__(rotations)
        else:
            raise ValueError("Can not mix intrinsic and extrinsic rotations.")


class QuaternionRotation(RotvecRotation):
    """Rotation based on Quaternions in 3D.

    Parameters
    ----------
    quaternion : ArrayLike
        A (possibly non-unit norm) quaternion in ``sequence`` format. It will be
        normalized to unit norm.
    sequence : str
        Specifies the order of parameters in the quaternion. Possible values are
        ``"xyzw"`` (default), i.e., scalar-last, or "wxyz", i.e., scalar-first.
    axis : int
        The axis along which to to compute. Default: -1.

    Notes
    -----
    The current implementation uses scipy's rotation class. As such you are
    limited to a single batch dimension. If this is to little, please open an
    issue.

    """

    def __init__(
        self, quaternion: ArrayLike, *, sequence: str = "xyzw", axis: int = -1
    ) -> None:

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

        super().__init__(rotvec, angle=angle, axis=axis)


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
    :class:`skbot.ignition.FrustumProjection`

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

        f_x = 1 / (tan(hfov / 2))
        f_y = aspect_ratio * f_x
        amounts = np.array([[0, 0, f_y], [0, 0, f_x]])
        directions = np.array([[0, 2 / image_shape[0], 0], [2 / image_shape[1], 0, 0]])

        self.proj = PerspectiveProjection(directions, amounts, axis=-1)
        self.tf = Translation(image_shape / 2)

    def transform(self, x: ArrayLike) -> np.ndarray:
        x_projected = self.proj.transform(x)
        x_transformed = self.tf.transform(x_projected)
        return x_transformed
