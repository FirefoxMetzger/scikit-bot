from numpy.typing import ArrayLike
from typing import Callable
import numpy as np
import math

from .base import Frame, Link, InverseLink
from ._utils import vector_project, angle_between
from .functions import translate, rotate


class AffineLink(Link):
    """A link representing a affine transformation.

    This is an abstract class useful when writing links for affine
    transformations. An affine transformation is a transformation that can be
    described using the equation ``y = Ax+b``.

    The main utility of this class is that it computes the corresponding
    transformation matrix once ``self.transform`` is known.
    """

    def __init__(self, parent: Frame, child: Frame) -> None:
        """Initialize a new affine link.

        Parameters
        ----------
        parent : Frame
            The frame in which vectors are specified.
        child : Frame
            The frame into which this link transforms vectors.
        """

        super().__init__(parent, child)

        self._tf_matrix = None
        self._inverse_tf_matrix = None

    @property
    def transformation(self) -> np.ndarray:
        """The transformation matrix mapping the parent to the child frame."""
        return self._tf_matrix

    @property
    def _inverse_transformation(self) -> np.ndarray:
        """The inverse transformation matrix mapping the child to the parent frame."""
        raise NotImplementedError

    def _update_transformation_matrix(self) -> None:
        mapped_basis = list()
        for basis in np.eye(self.parent.ndim):
            mapped_basis.append(self.transform(basis))
        offset = self.transform(np.zeros(self.parent.ndim))

        self._tf_matrix = np.zeros((self.child.ndim + 1, self.parent.ndim + 1))
        self._tf_matrix[:-1, :-1] = np.column_stack(mapped_basis) - offset[:, None]
        self._tf_matrix[:-1, -1] = offset
        self._tf_matrix[-1, -1] = 1

    def _update_inverse_transformation_matrix(self) -> None:
        mapped_basis = list()
        for basis in np.eye(self.child.ndim):
            mapped_basis.append(self.__inverse_transform__(basis))
        offset = self.__inverse_transform__(np.zeros(self.child.ndim))

        self._inverse_tf_matrix = np.zeros((self.child.ndim + 1, self.parent.ndim + 1))
        self._inverse_tf_matrix[:-1, :-1] = (
            np.column_stack(mapped_basis) - offset[:, None]
        )
        self._inverse_tf_matrix[:-1, -1] = offset
        self._inverse_tf_matrix[-1, -1] = 1


class Inverse(InverseLink):
    def __init__(self, link: AffineLink) -> None:
        super().__init__(link)
        self._forward_link: AffineLink

    @property
    def transformation(self) -> np.ndarray:
        """The transformation matrix mapping the parent to the child frame."""
        return self._forward_link._inverse_tf_matrix


class Fixed(AffineLink):
    """A link representing a affine transformation.

    This link corresponds to a affine transformation of the form ``y = Ax+b``.
    It has no parameters and remains constant after it has been initialized.

    Methods
    -------
    Fixed(parent, child, transformation)
        Initialize a new affine link. ``transformation`` is a callable that
        transforms a vector from the parent frame to the child frame.

    Notes
    -----
    This function does not implement __inverse_transform__.

    """

    def __init__(
        self,
        parent: Frame,
        child: Frame,
        transformation: Callable[[ArrayLike], np.ndarray],
    ) -> None:
        """Initialize a new affine link.

        Parameters
        ----------
        parent : Frame
            The frame in which vectors are specified.
        child : Frame
            The frame into which this link transforms vectors.
        transfomration : Callable[[ArrayLike], np.ndarray]
            A callable that takes a vector - in the parent frame - as input and
            returns the vector in the child frame.

        """

        super().__init__(parent, child)
        self._transform = transformation
        self._update_transformation_matrix()

    def transform(self, x: ArrayLike) -> np.ndarray:
        return self._transform(x)


class PlanarRotation(AffineLink):
    """A link representing a planar rotation.

    The plane of rotation is described by the two vectors (u, v). The initial
    angle of rotation is twice the angle between u and v (measured from u to v)
    and can be modified by setting the angle explicitly, e.g. ``link.angle =
    np.pi``. The angle is measured in radians.

    Attributes
    ----------
    angle : float
        The amount (in radians) to rotate. A positive angle rotates u towards v.

    Methods
    -------
    PlanarRotation(parent, child, u, v)
        Create a new link that rotates a vector in the u-v-plane.

    Notes
    -----
    This class implements __inverse_transform__, so you can get a syncronized inverse
    link via ``inverse_link = ropy.transform.affine.Inverse(link)``.
    """

    def __init__(self, parent: Frame, child: Frame, u: ArrayLike, v: ArrayLike) -> None:
        super(AffineLink, self).__init__(parent, child)

        u = np.asarray(u)
        v = np.asarray(v)

        self._u = u / np.linalg.norm(u)
        self._v = v / np.linalg.norm(v)
        self._angle = 2 * angle_between(u, v)

        u_orthogonal = v - vector_project(v, u)
        self._u_ortho = u_orthogonal / np.linalg.norm(u_orthogonal)

        self._update_transformation_matrix()
        self._update_inverse_transformation_matrix()

    def transform(self, x: ArrayLike) -> np.ndarray:
        return rotate(x, self._u, self._v)

    def __inverse_transform__(self, x: ArrayLike) -> np.ndarray:
        return rotate(x, self._v, self._u)

    @property
    def angle(self) -> float:
        return self._angle

    @angle.setter
    def angle(self, angle: float) -> None:
        self._angle = angle
        self._v = math.cos(angle / 2) * self._u + math.sin(angle / 2) * self._u_ortho

        self._update_transformation_matrix()
        self._update_inverse_transformation_matrix()


class Translation(AffineLink):
    """A link representing a translation.

    Attributes
    ----------
    direction : np.ndarray
        The direction in which vectors are translated.

    Methods
    -------
    Translation(parent, child, direction)
        Create a new link that translates vectors in the given direction

    Notes
    -----
    This class implements __inverse_transform__, so you can get a syncronized inverse
    link via ``inverse_link = ropy.transform.affine.Inverse(link)``.

    """

    def __init__(
        self, parent: Frame, child: Frame, direction: ArrayLike, *, amount: float = 1
    ) -> None:
        super().__init__(parent, child)

        self._amount = amount
        self._direction = np.asarray(direction)

        self._update_transformation_matrix()
        self._update_inverse_transformation_matrix()

    @property
    def direction(self) -> np.ndarray:
        return self._direction

    @direction.setter
    def direction(self, direction: ArrayLike) -> None:
        self._direction = np.asarray(direction)

        self._update_transformation_matrix()
        self._update_inverse_transformation_matrix()

    @property
    def amount(self) -> float:
        return self._amount

    @amount.setter
    def amount(self, amount: float) -> None:
        self._amount = amount

        self._update_transformation_matrix()
        self._update_inverse_transformation_matrix()

    def transform(self, x: ArrayLike) -> np.ndarray:
        return translate(x, self._amount * self._direction)

    def __inverse_transform__(self, x: ArrayLike) -> np.ndarray:
        return translate(x, -self._amount * self._direction)


__all__ = [
    # Links
    "Translation",
    "PlanarRotation",
    "Fixed",
    "Inverse",
]
