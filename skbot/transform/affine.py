from numpy.typing import ArrayLike
from typing import Callable
import numpy as np

from .base import Frame, Link, InvertLink
from ._utils import vector_project, angle_between
from .functions import translate, rotate


class AffineLink(Link):
    """A link representing a affine transformation.

    This is an abstract class useful when writing links for affine
    transformations. An affine transformation is a transformation that can be
    described using the equation ``y = Ax+b``.

    The main utility of this class is that it computes the corresponding
    transformation matrix once ``self.transform`` is known.

    Parameters
    ----------
    parent : int
        The frame in which vectors are specified.
    child : int
        The frame into which this link transforms vectors.
    axis : int
        The axis along which computation takes place. All other axes are considered
        batch dimensions.

    """

    def __init__(self, parent_dim: int, child_dim: int, *, axis: int = -1) -> None:
        """Initialize a new affine link."""

        super().__init__(parent_dim, child_dim)

        self._tf_matrix = None
        self._inverse_tf_matrix = None
        self._axis = axis

    @property
    def affine_matrix(self) -> np.ndarray:
        """The transformation matrix mapping the parent to the child frame."""
        return self._tf_matrix

    @property
    def _inverse_affine_matrix(self) -> np.ndarray:
        """The inverse transformation matrix mapping the child to the parent frame."""
        raise NotImplementedError

    def _update_transformation_matrix(self, shape: ArrayLike) -> None:
        shape = np.asarray(shape)
        reoreded_shape = np.moveaxis(shape, self._axis, -1)

        mapped_basis = list()
        for basis in np.eye(self.parent_dim):
            batch_vector = np.zeros(reoreded_shape)
            batch_vector[..., :] = basis
            batch_vector = np.moveaxis(batch_vector, -1, self._axis)
            mapped = self.transform(basis)
            mapped = np.moveaxis(mapped, self._axis, -1)
            mapped_basis.append(mapped)
        mapped_basis = np.stack(mapped_basis, axis=-2)
        offset = self.transform(np.zeros(shape))
        offset = np.moveaxis(offset, self._axis, -1)
        offset_remove = np.expand_dims(offset, -2)

        self._tf_matrix = np.zeros(
            (*reoreded_shape[:-1], self.child_dim + 1, self.parent_dim + 1)
        )
        self._tf_matrix[..., :-1, :-1] = mapped_basis - offset_remove
        self._tf_matrix[..., :-1, -1] = offset
        self._tf_matrix[..., -1, -1] = 1

    def _update_inverse_transformation_matrix(self, shape: ArrayLike = None) -> None:
        shape = np.asarray(shape)
        reoreded_shape = np.moveaxis(shape, self._axis, -1)

        mapped_basis = list()
        for basis in np.eye(self.child_dim):
            batch_vector = np.zeros(reoreded_shape)
            batch_vector[..., :] = basis
            batch_vector = np.moveaxis(batch_vector, -1, self._axis)
            mapped = self.__inverse_transform__(basis)
            mapped = np.moveaxis(mapped, self._axis, -1)
            mapped_basis.append(mapped)
        mapped_basis = np.stack(mapped_basis, axis=-2)
        offset = self.__inverse_transform__(np.zeros(shape))
        offset = np.moveaxis(offset, self._axis, -1)

        self._inverse_tf_matrix = np.zeros(
            (*reoreded_shape[:-1], self.child_dim + 1, self.parent_dim + 1)
        )
        self._inverse_tf_matrix[..., :-1, :-1] = mapped_basis - offset[..., None]
        self._inverse_tf_matrix[..., :-1, -1] = offset
        self._inverse_tf_matrix[..., -1, -1] = 1

    def invert(self) -> Frame:
        """Return a new Link that is the inverse of this link."""
        return Inverse(self)


class Inverse(InvertLink):
    def __init__(self, link: AffineLink) -> None:
        super().__init__(link)
        self._forward_link: AffineLink

    @property
    def affine_matrix(self) -> np.ndarray:
        """The transformation matrix mapping the parent to the child frame."""
        return self._forward_link._inverse_tf_matrix


class Rotation(AffineLink):
    """Planar rotation in N-D.

    The plane of rotation is described by two vectors (u, v). The initial
    angle of rotation is twice the angle between u and v (measured from u to v)
    and can be modified by setting the angle explicitly, e.g. ``link.angle =
    np.pi``. The angle is measured in radians.

    Parameters
    ----------
    u : ArrayLike
        The first vector defining the plane of rotation. The angle is mesured
        from here.
    v : ArrayLike
        The second vector defining the plane of rotation. The angle is measured
        to here, i.e., from u to v.

    Notes
    -----
    Implements __inverse_transform__.

    """

    def __init__(self, u: ArrayLike, v: ArrayLike, *, axis: int = -1) -> None:
        u = np.asarray(u)
        v = np.asarray(v)

        frame_dim = u.shape[axis]

        super().__init__(frame_dim, frame_dim)

        self._u = u / np.linalg.norm(u)
        self._v = v / np.linalg.norm(v)
        self._angle = 2 * angle_between(u, v)

        u_orthogonal = v - vector_project(v, u)
        self._u_ortho = u_orthogonal / np.linalg.norm(u_orthogonal)

        self._update_transformation_matrix(shape=u.shape)
        self._update_inverse_transformation_matrix(shape=u.shape)

    def transform(self, x: ArrayLike) -> np.ndarray:
        return rotate(x, self._u, self._v)

    def __inverse_transform__(self, x: ArrayLike) -> np.ndarray:
        return rotate(x, self._v, self._u)

    @property
    def angle(self) -> float:
        """The magnitude of the rotation (in radians)."""
        return self._angle

    @angle.setter
    def angle(self, angle: float) -> None:
        self._angle = angle

        self._v = np.cos(angle / 2) * self._u - np.sin(angle / 2) * self._u_ortho

        self._update_transformation_matrix(self._u.shape)
        self._update_inverse_transformation_matrix(self._u.shape)


class Translation(AffineLink):
    """Translation in N-D.


    Parameters
    ----------
    direction : ArrayLike
        The vector describing the translation.
    amount : float
        A scalar indicating by how much to scale ``direction``. Default is 1.

    Notes
    -----
    This class implements :func:`Link.__inverse_transform__`. You can get a syncronized inverse
    link via ``inverse_link = skbot.transform.affine.Inverse(link)``.

    """

    def __init__(
        self, direction: ArrayLike, *, amount: float = 1, axis: int = -1
    ) -> None:
        direction = np.asarray(direction)

        frame_dim = len(direction)

        super().__init__(frame_dim, frame_dim, axis=axis)

        self._amount = amount
        self._direction = np.asarray(direction)

        self._update_transformation_matrix(self._direction.shape)
        self._update_inverse_transformation_matrix(self._direction.shape)

    @property
    def direction(self) -> np.ndarray:
        """The direction in which vectors are translated."""
        return self._direction

    @direction.setter
    def direction(self, direction: ArrayLike) -> None:
        self._direction = np.asarray(direction)

        self._update_transformation_matrix(self._direction.shape)
        self._update_inverse_transformation_matrix(self._direction.shape)

    @property
    def amount(self) -> float:
        """The amount by which to scale the direction vector."""
        return self._amount

    @amount.setter
    def amount(self, amount: float) -> None:
        self._amount = amount

        self._update_transformation_matrix(self._direction.shape)
        self._update_inverse_transformation_matrix(self._direction.shape)

    def transform(self, x: ArrayLike) -> np.ndarray:
        return translate(x, self._amount * self._direction)

    def __inverse_transform__(self, x: ArrayLike) -> np.ndarray:
        return translate(x, -self._amount * self._direction)
