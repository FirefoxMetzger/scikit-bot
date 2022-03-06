from math import sqrt
from .base import Link
from .affine import Rotation
from numpy.typing import ArrayLike
import numpy as np


class Rotation2D(Rotation):
    """Rotation in 2D.

    A convenient way of initializing a rotation in 2D.

    Parameters
    ----------
    angle : ArrayLike
        The magnitude of the rotation.
    degrees : bool
        If True, angle is assumed to be in degrees. Default is False.
    axis : int
        The axis along which computation takes place. All other axes are
        considered batch dimensions.

    """

    def __init__(
        self,
        angle: ArrayLike,
        *,
        degrees: bool = False,
        axis: int = -1,
    ) -> None:
        angle = np.asarray(angle)
        vector_shape = [*angle.shape]
        vector_shape[axis] = 2

        u_vector = np.zeros(vector_shape)
        u_vector[..., 1] = 1

        v_vector = np.zeros(vector_shape)
        v_vector[..., 0] = 1

        super().__init__(u_vector, v_vector, axis=axis)

        if degrees:  # make radians
            angle = angle / 360 * 2 * np.pi

        self.angle = angle


class AxialHexagonTransform(Link):
    """Conversion to Axial Hexagon Coordininates in 2D

    This transform takes a 2D vector in euclidian (x, y) coordinates and
    converts it into coordinates on a (r, q, s) hexagonal grid. For this, it
    uses axial coordinates for which the value of s is implied, because r+q+s=0;
    hence this transform returns a 2D vector in (r, q) coordinates.

    See here for an overview of `Hexagon Coordinate Systems
    <https://www.redblobgames.com/grids/hexagons/#coordinates>`_.

    Parameters
    ----------
    size : ArrayLike
        The size of a single hexagon. It measures the distance from a hexagon
        center to one of it's corners.
    flat_top : bool
        If True (default), hexagons are oriented with one side parallel to the x
        axis (top is flat). Otherwise they are oriented with one side
        parallel to the y-axis (top is pointy).
    axis : int
        The axis along which computation takes place. All other axes are
        considered batch dimensions.

    """

    def __init__(
        self, *, size: ArrayLike = 1.0, flat_top: bool = True, axis: int = -1
    ) -> None:
        super().__init__(2, 2)

        self.size = size
        self._axis = axis

        if flat_top:
            self.q_basis = np.array([2 / 3, 0])
            self.r_basis = np.array([-1 / 3, sqrt(3) / 3])

            # basis for inverse transform
            self.x_basis = np.array([3 / 2, 0])
            self.y_basis = np.array([sqrt(3) / 2, sqrt(3)])
        else:
            self.q_basis = np.array([sqrt(3) / 3, -1 / 3])
            self.r_basis = np.array([0, 2 / 3])

            # basis for inverse transform
            self.x_basis = np.array([sqrt(3), sqrt(3) / 2])
            self.y_basis = np.array([0, 3 / 2])

    def transform(self, x: ArrayLike) -> np.ndarray:
        x = np.asfarray(x)
        x = np.moveaxis(x, self._axis, -1)

        result = np.empty_like(x)
        result[..., 0] = np.sum(x * self.q_basis, axis=-1)
        result[..., 1] = np.sum(x * self.r_basis, axis=-1)
        result /= self.size

        return result

    def __inverse_transform__(self, x: ArrayLike) -> np.ndarray:
        x = np.asfarray(x)
        x = np.moveaxis(x, self._axis, -1)

        result = np.empty_like(x)
        result[..., 0] = np.sum(x * self.x_basis, axis=-1)
        result[..., 1] = np.sum(x * self.y_basis, axis=-1)
        result *= self.size

        return result


class HexagonAxisRound(Link):
    """Round Hexagon Axis Coordinates in 2D.

    This link rounds hexagon coordinates given in axis coordinates (r, q) to
    their closest hexagon.

    Parameters
    ----------
    axis : int
        The axis along which rounding takes place.


    Notes
    -----
    This link is _not_ invertible.

    """

    def __init__(self, *, axis=-1) -> None:
        super().__init__(2, 2)
        self._axis = axis

    def transform(self, x: ArrayLike) -> np.ndarray:
        x = np.moveaxis(x, self._axis, -1)

        # convert to cube coordinates
        cube_coordinates = np.empty((*x.shape[:-1], 3))
        cube_coordinates[..., :-1] = x
        cube_coordinates[..., -1] = -x[..., 0] - x[..., 1]
        cube_coordinates = cube_coordinates.reshape(-1, 3)

        # round and enforce q+r+s=0 constraint
        cube_rounded = np.round(cube_coordinates).astype(int)
        residual = np.abs(cube_coordinates - cube_rounded)
        first_max = np.argmax(residual, axis=-1)
        matching_range = np.arange(first_max.shape[0])
        cube_rounded[matching_range, first_max] -= np.sum(cube_rounded, axis=-1)

        rounded_coordinates = np.moveaxis(cube_rounded[..., :2], -1, self._axis)
        return rounded_coordinates
