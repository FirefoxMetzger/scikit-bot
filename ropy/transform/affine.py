from numpy.typing import ArrayLike
from typing import Callable
import numpy as np
import math

from .coordinates import Frame, Link
from ._utils import vector_project, angle_between
from .base import translate, rotate


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

    @property
    def transformation(self) -> np.ndarray:
        if self._tf_matrix is None:
            raise RuntimeError("Transformation Matrix not initialized.")

        return self._tf_matrix

    def _update_transformation_matrix(self):
        mapped_basis = list()
        for basis in np.eye(self.parent.ndim):
            mapped_basis.append(self.transform(basis))

        offset = self.transform(np.zeros(self.parent.ndim))
        
        tf_matrix = np.column_stack(mapped_basis) - offset[:, None]

        self._tf_matrix = np.zeros((self.child.ndim + 1, self.parent.ndim + 1))
        self._tf_matrix[:-1, :-1] = tf_matrix
        self._tf_matrix[:-1, -1] = offset
        self._tf_matrix[-1, -1] = 1


class Fixed(AffineLink):
    """ A link representing a affine transformation.

    This link corresponds to a affine transformation of the form ``y = Ax+b``.
    It has no parameters and remains constant after it has been initialized.

    Methods
    -------
    Fixed(parent, child, transformation)
        Initialize a new affine link. ``transformation`` is a callable that
        transforms a vector from the parent frame to the child frame.

    """

    def __init__(self, parent: Frame, child: Frame, transformation:Callable[[ArrayLike], np.ndarray]) -> None:
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

    def transform(self, x: ArrayLike) -> np.ndarray:
        return self._transform(x)
   

class PlanarRotation(AffineLink):
    def __init__(self, parent: Frame, child: Frame, u: ArrayLike, v: ArrayLike) -> None:
        super(AffineLink, self).__init__(parent, child)

        u = np.asarray(u)
        v = np.asarray(v)

        self._u = u
        self._v = v
        self._angle = 2* angle_between(u, v)

        u_orthogonal = u - vector_project(u, v)
        self._u_ortho = u_orthogonal / np.linalg.norm(u_orthogonal)
        

    def transform(self, x: ArrayLike) -> np.ndarray:
        return rotate(x, self._u, self._v)

    @property
    def transformation(self) -> np.ndarray:
        return super().transformation

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, angle):
        self._angle = angle
        self._v = math.cos(angle)*self._u + math.sin(angle) * self._u_ortho
