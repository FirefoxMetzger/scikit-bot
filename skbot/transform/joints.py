from numpy.typing import ArrayLike
import numpy as np
from .utils3d import RotvecRotation
from .affine import Translation


class RotationalJoint(RotvecRotation):
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
        self.upper_limit = upper_limit
        self.lower_limit = lower_limit
        super().__init__(rotvec, angle=angle, degrees=degrees, axis=axis)

    @property
    def param(self) -> float:
        return self._angle

    @param.setter
    def param(self, value: ArrayLike) -> None:
        self._angle = value

        self._v = np.cos(value / 2) * self._u - np.sin(value / 2) * self._u_ortho

        self._update_transformation_matrix(self._u.shape)
        self._update_inverse_transformation_matrix(self._u.shape)

    @RotvecRotation.angle.setter
    def angle(self, angle: ArrayLike) -> None:
        angle = np.asarray(angle)

        if np.any(angle < self.lower_limit) or np.any(angle > self.upper_limit):
            raise ValueError("An angle exceeds the joint's limit.")

        self.param = angle


class PrismaticJoint(Translation):
    def __init__(
        self,
        direction: ArrayLike,
        *,
        upper_limit: ArrayLike = 1,
        lower_limit: ArrayLike = 0,
        amount: ArrayLike = 1,
        axis: int = -1,
    ) -> None:
        self.upper_limit = np.asarray(upper_limit)
        self.lower_limit = np.asarray(lower_limit)
        super().__init__(direction, amount=amount, axis=axis)

    @property
    def param(self) -> float:
        """The amount by which to scale the direction vector."""
        return self._amount

    @param.setter
    def param(self, value: ArrayLike) -> None:
        self._amount = np.asarray(value)

        self._update_transformation_matrix(self._direction.shape)
        self._update_inverse_transformation_matrix(self._direction.shape)

    @Translation.amount.setter
    def amount(self, amount: ArrayLike) -> None:
        amount = np.asarray(amount)

        if np.any(amount < self.lower_limit) or np.any(amount > self.upper_limit):
            raise ValueError("An angle exceeds the joint's limit.")

        self.param = amount
