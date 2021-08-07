from math import tan
from typing import Tuple

import numpy as np
from numpy.typing import ArrayLike

from .affine import AffineLink
from ._utils import scalar_project


class PerspectiveProjection(AffineLink):
    """Perspective projection in N-D.

    This link projects a N dimensional frame onto an M dimensional frame. Using
    the parent's origin as the center of projection. In its most common use
    this corresponds to a central projection, e.g., the projection of
    coordinates in a 3D world frame down to a 2D camera frame.

    This link computes the projection using pairs of ``directions`` and
    ``amounts`` (both batches of vectors). To compute each coordinate of a
    vector in the projected space the vector is first scalar projected onto the
    amount (vector). This determines distance from the projection's center. Then
    the vector is scalar projected onto the direction (vector) and the
    result is scaled (anti-)proportional to the distance from the projection's
    center.

    Parameters
    ----------
    directions : ArrayLike
        A batch of (subspace-)vectors onto which points will be projected. The
        vectors run along ``axis`` and the subspace runs along
        ``subspace_axis``. All other dimensions are considered batch dimensions.
        Often this is a normal basis of the projection's subspace, e.g., the
        the x and y axes of a camera's image plane expressed in the parent
        frame.
    amounts : ArrayLike
        A batch of vectors indicating the direction along which to measure
        distance from the projection center. Its shape must match
        ``directions.shape``. Often all amount vectors are pairwise linearly
        dependent, e.g., they all point in the direction a camera is facing.
    axis : int
        The axis along which the projection is computed. It's length is equal to
        the number of dimensions in the parent frame.
    subspace_axis : int
        The axis along which different directions and amounts are stacked. It's
        length is equal to the number of dimensions in the child frame. Note
        that this axis _must_ be present, even if vectors are projected down to
        1D; in this case, the this axis has length 1.



    Methods
    -------
    transform(x)
        Expresses the vector x (assumed to be given in the parent's frame) in
        the child's frame.


    See Also
    --------
    :class:`skbot.transform.FrustumProjection`, :class:`skbot.ignition.FrustumProjection`

    Notes
    -----
    The length of a single direction vector rescales this axis. For example, if you have
    a camera with a certain number of pixels then the length of the direction vector would
    reflect this.

    The length of a single amount vector determines the scaling of distance. For example, if
    you have a camera with a certain focal lengths (fx, fy) then the length of the amount vector
    would reflect this.

    """

    def __init__(
        self,
        directions: ArrayLike,
        amounts: ArrayLike,
        *,
        axis: int = -1,
        subspace_axis: int = -2
    ) -> None:
        self.directions = np.asarray(directions)
        self.amounts = np.asarray(amounts)

        # make data axis the last axis (more efficient and easier to handle)
        # also make subspace axis the second last axis
        self.directions = np.moveaxis(self.directions, [subspace_axis, axis], [-2, -1])
        self.amounts = np.moveaxis(self.amounts, [subspace_axis, axis], [-2, -1])

        super().__init__(self.directions.shape[axis], self.directions.ndim, axis=axis)

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

        Notes
        -----
        This function requires the batch dimensions of ``x``, ``amounts``, and
        ``directions`` to be broadcastable. To make an example assume a
        projection from N dimensions to M dimensions. In the trivial case
        (single vector, single projection) there are no batch dimensions; shapes
        are what you'd expect: ``x.shape=(N,)``, ``amounts.shape = (M, N)``,
        ``directions.shape=(M, N)``. In the case of a batch of vectors and a
        single projection, batch dimensions must be broadcastable:
        ``x.shape=(batch, N)``, ``amounts.shape = (1, M, N)``,
        ``directions.shape=(1, M, N)``. In the case of a single single vector
        and multiple projections the same rule applies: ``x.shape=(1, N)``,
        ``amounts.shape = (batch, M, N)``, ``directions.shape=(batch, M, N)``.
        Other combinations are - of course - possible, too.
        """
        x = np.asarray(x, dtype=np.float64)
        x = np.moveaxis(x, self._axis, -1)

        # make x broadcastable with amounts/directions
        x = np.expand_dims(x, -2)

        scaling = scalar_project(x, self.amounts, axis=-1)
        scaling /= np.linalg.norm(self.amounts, axis=-1)

        projected = scalar_project(x, self.directions, axis=-1)
        projected /= scaling * np.linalg.norm(self.directions, axis=-1)

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
