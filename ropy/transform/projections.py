from math import tan
from typing import Tuple

import numpy as np
from numpy.typing import ArrayLike

from .affine import AffineLink
from ._utils import scalar_project


class PerspectiveProjection(AffineLink):
    """Perspective projection in N-D.

    This link projects a N dimensional frame onto an M dimensional frame.
    In it's most common use this corresponds to a central projection, e.g.,
    the projection of coordinates in a 3D world frame down to a 2D camera frame.

    This link computes the projection using pairs of ``directions`` and
    ``amounts`` (both batches of vectors). To compute a coordinate of a vector
    in the projected space the vector is first scalar projected onto the amount
    (vector). Then direction is scaled proportional to the value of this scalar
    projection. Finally, the vector is vector projected onto the desired
    direction.

    Methods
    -------
    transform(x)
        Expresses the vector x (assumed to be given in the parent's frame) in
        the child's frame.


    """

    def __init__(
        self, directions: ArrayLike, amounts: ArrayLike, *, axis: int = -1
    ) -> None:
        self.directions = np.asarray(directions)
        self.amounts = np.asarray(amounts)
        self.axis = axis

        # make data axis the last axis (more efficient and easier to handle)
        self.directions = np.moveaxis(self.directions, axis, -1)
        self.amounts = np.moveaxis(self.amounts, axis, -1)

        super().__init__(self.directions.shape[axis], self.directions.ndim)

    def transform(self, x: ArrayLike) -> np.ndarray:
        """Transform x (given in parent frame) into the child frame.

        Parameters
        ----------
        x : ArrayLike
            A batch of vectors expressed in the parent's frame. The parent frame runs
            along ``axis`` specified in the constructor.

        Returns
        -------
        y : ArrayLike
            A batch of vectors expressed in the child's frame. The child frame runs
            along ``axis`` specified in the constructor.

        """
        x = np.asarray(x, dtype=np.float64)
        x = np.moveaxis(x, self.axis, -1)

        # match shapes of all involved tensors final shape is
        # (x_batch.shape, directions_batch.shape, axis)
        amounts = np.expand_dims(self.amounts, [y for y in range(x.ndim - 1)])
        directions = np.expand_dims(self.directions, [y for y in range(x.ndim - 1)])

        scaling = scalar_project(x, self.amounts, axis=-1)
        scaling /= np.linalg.norm(amounts, axis=-1)

        projected = scalar_project(x, self.directions, axis=-1)
        projected /= scaling * np.linalg.norm(directions, axis=-1)

        return projected

    def __inverse_transform__(self, x: ArrayLike) -> np.ndarray:
        """Transform x (given in the child frame) into the parent frame.

        Parameters
        ----------
        x : ArrayLike
            The vector expressed in the childs's frame

        Returns
        -------
        y : ArrayLike
            The vector expressed in the parents's frame

        """
        raise NotImplementedError("A projection isn't invertable in general.")
