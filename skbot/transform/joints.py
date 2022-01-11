from abc import ABC, abstractmethod

import numpy as np
from numpy.typing import ArrayLike

from .affine import Rotation, Translation
from .utils3d import RotvecRotation


class Joint(ABC):
    """Abstract Joint.

    This class is used to define the joint interface and to create a common base
    class that joints can inherit from.
    """

    @property
    @abstractmethod
    def param(self):
        """Unified name for the parameter controlling this joint"""
        raise NotImplementedError()

    @param.setter
    @abstractmethod
    def param(self, value: ArrayLike):
        """Joints must be modifiable."""
        raise NotImplementedError()

    @property
    @abstractmethod
    def upper_limit(self):
        """Maximum parameter value.

        Notes
        -----
        This can be ``np.inf`` if there is no upper limit.

        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def lower_limit(self):
        """Minimum parameter value.

        Notes
        -----
        This can be ``-np.inf`` if there is no lower limit.

        """
        raise NotImplementedError()


class RotationalJoint(RotvecRotation, Joint):
    """Rotation with constraints in 3D.

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
    upper_limit : ArrayLike
        The maximum joint angle. Default: 2pi.
    lower_limit : ArrayLike
        The minimum joint angle. Default: 0.

    Notes
    -----
    Batch dimensions of ``rotvec`` and ``angle`` must be broadcastable.

    Setting ``RotationalJoint.angle`` will check if the joint angle limits are
    respected; however, setting ``RotationalJoint.param`` will not.

    """

    def __init__(
        self,
        rotvec: ArrayLike,
        *,
        angle: ArrayLike = None,
        degrees: bool = False,
        axis: int = -1,
        upper_limit: ArrayLike = 2 * np.pi,
        lower_limit: ArrayLike = 0,
    ) -> None:
        self._upper_limit = upper_limit
        self._lower_limit = lower_limit
        super().__init__(rotvec, angle=angle, degrees=degrees, axis=axis)

    @property
    def upper_limit(self):
        return self._upper_limit

    @property
    def lower_limit(self):
        return self._lower_limit

    @property
    def param(self) -> float:
        """Magnitude of the rotation (in radians)."""
        return self._angle

    @param.setter
    def param(self, value: ArrayLike) -> None:
        self._angle = value

        self._v = np.cos(value / 2) * self._u - np.sin(value / 2) * self._u_ortho

    @RotvecRotation.angle.setter
    def angle(self, angle: ArrayLike) -> None:
        angle = np.asarray(angle)

        if np.any(angle < self.lower_limit) or np.any(angle > self.upper_limit):
            raise ValueError("An angle exceeds the joint's limit.")

        self.param = angle


class AngleJoint(Rotation, Joint):
    """Rotation with constraints in 2D.

    Parameters
    ----------
    angle : ArrayLike
        The magnitude of the rotation. If None, it will be set to ``lower_limit``.
    degrees : bool
        If True, angle is assumed to be in degrees. Default is False.
    axis : int
        The axis along which to to compute. Default: -1.
    upper_limit : ArrayLike
        The maximum joint angle. Default: 2pi.
    lower_limit : ArrayLike
        The minimum joint angle. Default: 0.

    Notes
    -----

    Setting ``RotationalJoint.angle`` will check if the joint angle limits are
    respected; however, setting ``RotationalJoint.param`` will not.

    """

    def __init__(
        self,
        *,
        angle: ArrayLike = None,
        degrees: bool = False,
        axis: int = -1,
        upper_limit: ArrayLike = 2 * np.pi,
        lower_limit: ArrayLike = 0,
    ) -> None:
        super().__init__((1, 0), (0, 1), axis=axis)

        angle = angle or lower_limit
        if degrees:  # make radians
            angle = angle / 360 * 2 * np.pi

        self.param = angle
        self._upper_limit = upper_limit
        self._lower_limit = lower_limit

    @property
    def upper_limit(self):
        return self._upper_limit

    @property
    def lower_limit(self):
        return self._lower_limit

    @property
    def param(self) -> float:
        """Magnitude of the rotation (in radians)."""
        return self._angle

    @param.setter
    def param(self, value: ArrayLike) -> None:
        self._angle = value

        self._v = np.cos(value / 2) * self._u - np.sin(value / 2) * self._u_ortho

    @Rotation.angle.setter
    def angle(self, angle: ArrayLike) -> None:
        angle = np.asarray(angle)

        if np.any(angle < self.lower_limit) or np.any(angle > self.upper_limit):
            raise ValueError("An angle exceeds the joint's limit.")

        self.param = angle


class PrismaticJoint(Translation, Joint):
    """Translation with constraints in N-D.

    Parameters
    ----------
    direction : ArrayLike
        A vector describing the translation.
    amount : ArrayLike
        A scalar indicating by how much to scale ``direction``. Default is 1.
    axis : int
        The axis along which computation takes place. All other axes are considered
        batch dimensions.
    upper_limit : ArrayLike
        The maximum value of amount. Default: 1.
    lower_limit : ArrayLike
        The minimum value of amount. Default: 0.

    Notes
    -----
    Setting ``PrismaticJoint.amount`` will enforce joint limits; however,
    setting ``PrismaticJoint.param`` will not.

    """

    def __init__(
        self,
        direction: ArrayLike,
        *,
        upper_limit: ArrayLike = 1,
        lower_limit: ArrayLike = 0,
        amount: ArrayLike = 1,
        axis: int = -1,
    ) -> None:
        self._upper_limit = upper_limit
        self._lower_limit = lower_limit
        super().__init__(direction, amount=amount, axis=axis)

    @property
    def upper_limit(self):
        return self._upper_limit

    @property
    def lower_limit(self):
        return self._lower_limit

    @property
    def param(self) -> float:
        """The amount by which to scale the direction vector."""
        return self._amount

    @param.setter
    def param(self, value: ArrayLike) -> None:
        self._amount = np.asarray(value)

    @Translation.amount.setter
    def amount(self, amount: ArrayLike) -> None:
        amount = np.asarray(amount)

        if np.any(amount < self.lower_limit) or np.any(amount > self.upper_limit):
            raise ValueError("An angle exceeds the joint's limit.")

        self.param = amount
