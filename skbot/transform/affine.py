from numpy.typing import ArrayLike
from typing import List
import numpy as np

from .base import Frame, Link, InvertLink
from ._utils import vector_project, angle_between
from .functions import translate, rotate, as_affine_matrix


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
        self._axis = axis

    @property
    def affine_matrix(self) -> np.ndarray:
        """The transformation matrix mapping the parent to the child frame."""

        cartesian_parent = Frame(self.parent_dim)
        cartesian_child = Frame(self.child_dim)
        self(cartesian_parent, cartesian_child)

        affine_parent = AffineSpace(self.parent_dim, axis=self._axis)(cartesian_parent)
        affine_child = AffineSpace(self.child_dim, axis=self._axis)(cartesian_child)

        affine_matrix = as_affine_matrix(affine_parent, affine_child, axis=self._axis)

        return affine_matrix

    @property
    def _inverse_tf_matrix(self):
        cartesian_parent = Frame(self.parent_dim)
        cartesian_child = Frame(self.child_dim)
        self(cartesian_parent, cartesian_child)

        affine_parent = AffineSpace(self.parent_dim, axis=self._axis)(cartesian_parent)
        affine_child = AffineSpace(self.child_dim, axis=self._axis)(cartesian_child)

        affine_matrix = as_affine_matrix(affine_child, affine_parent, axis=self._axis)

        return affine_matrix

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


class AffineCompound(AffineLink):
    def __init__(self, wrapped_links: List[AffineLink]) -> None:
        super().__init__(wrapped_links[0].parent_dim, wrapped_links[-1].child_dim)
        self._links = wrapped_links

    def transform(self, x: ArrayLike) -> np.ndarray:
        for link in self._links:
            x = link.transform(x)

        return x

    def __inverse_transform__(self, x: ArrayLike) -> np.ndarray:
        for link in reversed(self._links):
            x = link.__inverse_transform__(x)

        return x

    @property
    def affine_matrix(self) -> np.ndarray:
        """The transformation matrix mapping the parent to the child frame."""

        matrix = self._links[0].affine_matrix
        for link in self._links[1:]:
            matrix = link.affine_matrix @ matrix

        return matrix

    def invert(self) -> Frame:
        """Return a new Link that is the inverse of this link."""

        links = list()
        for link in reversed(self._links):
            links.append(Inverse(link))

        return AffineCompound(links)


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

        u = np.moveaxis(u, axis, -1)
        v = np.moveaxis(v, axis, -1)

        frame_dim = u.shape[axis]

        super().__init__(frame_dim, frame_dim)

        self._u = u / np.linalg.norm(u)
        self._v = v / np.linalg.norm(v)
        self._angle = 2 * angle_between(u, v)

        u_orthogonal = v - vector_project(v, u)
        self._u_ortho = u_orthogonal / np.linalg.norm(u_orthogonal)

    def transform(self, x: ArrayLike) -> np.ndarray:
        return rotate(x, self._u, self._v)

    def __inverse_transform__(self, x: ArrayLike) -> np.ndarray:
        return rotate(x, self._v, self._u)

    @property
    def angle(self) -> float:
        """The magnitude of the rotation (in radians)."""
        return self._angle

    @angle.setter
    def angle(self, angle: ArrayLike) -> None:
        self._angle = angle

        self._v = np.cos(angle / 2) * self._u - np.sin(angle / 2) * self._u_ortho


class Translation(AffineLink):
    """Translation in N-D.

    .. versionchanged:: 0.6.0
        ``direction`` and ``scalar`` may now be broadcastable arrays


    Parameters
    ----------
    direction : ArrayLike
        A vector, or batch of vectors, describing the translation.
    amount : ArrayLike
        A scalar indicating by how much to scale ``direction``. Default is 1.
    axis : int
        The axis along which computation takes place. All other axes are considered
        batch dimensions.

    """

    def __init__(
        self, direction: ArrayLike, *, amount: ArrayLike = 1, axis: int = -1
    ) -> None:
        direction = np.asarray(direction)

        frame_dim = direction.shape[axis]

        super().__init__(frame_dim, frame_dim, axis=axis)

        self._axis = axis
        self._amount = np.asarray(amount)
        self._direction = np.moveaxis(direction, axis, -1)

    @property
    def direction(self) -> np.ndarray:
        """The direction in which vectors are translated."""
        return self._direction

    @direction.setter
    def direction(self, direction: ArrayLike) -> None:
        self._direction = np.asarray(direction)

    @property
    def amount(self) -> float:
        """The amount by which to scale the direction vector."""
        return self._amount

    @amount.setter
    def amount(self, amount: ArrayLike) -> None:
        self._amount = np.asarray(amount)

    def transform(self, x: ArrayLike) -> np.ndarray:
        x = np.asarray(x)
        x = np.moveaxis(x, self._axis, -1)
        result = translate(x, self._amount[..., None] * self._direction)
        return np.moveaxis(result, -1, self._axis)

    def __inverse_transform__(self, x: ArrayLike) -> np.ndarray:
        x = np.asarray(x)
        x = np.moveaxis(x, self._axis, -1)
        result = translate(x, -self._amount[..., None] * self._direction)
        return np.moveaxis(result, -1, self._axis)


class AffineSpace(Link):
    """Transform to affine space

    Parameters
    ----------
    ndim : int
        The number of dimensions of the cartesian space.
    axis : int
        The axis along which computation takes place. All other axes are considered
        batch dimensions.


    """

    def __init__(self, ndim: int, *, axis=-1) -> None:
        super().__init__(ndim, ndim + 1)
        self._axis = axis

    def transform(self, x: ArrayLike) -> np.ndarray:
        x = np.moveaxis(x, self._axis, -1)

        shape = list(x.shape)
        shape[-1] += 1

        affine_vector = np.ones(shape, dtype=x.dtype)
        affine_vector[..., :-1] = x

        return np.moveaxis(affine_vector, -1, self._axis)

    def __inverse_transform__(self, x: ArrayLike) -> np.ndarray:
        x = np.moveaxis(x, self._axis, -1)

        values = x[..., :-1]
        scaling = x[..., -1][..., None]

        cartesian_vector = values / scaling

        return np.moveaxis(cartesian_vector, -1, self._axis)
