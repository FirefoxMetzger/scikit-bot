from __future__ import annotations  # life's too short for comments
from math import sin, cos
from numpy.typing import ArrayLike
from typing import List
import numpy as np


def homogenize(vector: ArrayLike) -> np.ndarray:
    """Convert a vector from cartesian coordinates into homogeneous coordinates.

    Parameters
    ----------
    vector : np.ndarray
        The vector to be converted.

    Returns
    -------
    homogeneous_vector : np.ndarray
        The vector in homogeneous coordinates.


    Examples
    --------

    >>> import ropy.transform as rtf
    >>> import numpy as np
    >>> cartesian_vector = np.array((1, 2, 3))
    >>> rtf.homogenize(cartesian_vector)
    array([1., 2., 3., 1.])

    """
    vector = np.asarray(vector)

    shape = vector.shape
    homogeneous_vector = np.ones((*shape[:-1], shape[-1] + 1))
    homogeneous_vector[..., :-1] = vector
    return homogeneous_vector


def cartesianize(vector: ArrayLike) -> np.ndarray:
    """Convert a vector from homogeneous coordinates to cartesian coordinates.

    Parameters
    ----------
    vector : np.ndarray
        The vector in homogeneous coordinates.

    Returns
    -------
    cartesian_vector : np.ndarray
        The vector to be converted.

    Examples
    --------

    >>> import numpy as np
    >>> import ropy.transform as rtf
    >>> rtf.cartesianize(np.array((1, 2, 3, 41)))
    array([1., 2., 3.])
    >>> rtf.cartesianize((2, 0, 2, 2))
    array([1., 0., 1.])
    >>> rtf.cartesianize((2, 0, 2, 1))
    array([2., 0., 2.])
    >>> rtf.cartesianize((2, 0, 2, 2*np.sqrt(2)))
    array([0.70710678, 0.        , 0.70710678])
    >>> np.array((2, 0, 2)) / np.linalg.norm(np.array(( 2, 0, 2)))
    array([0.70710678, 0.        , 0.70710678])

    """
    vector = np.asarray(vector)

    return vector[..., :-1] / vector[..., -1]


def normalize_scale(vector: ArrayLike) -> np.ndarray:
    """Return an equivalent homogeneous vector with scale set to 1.

    Parameters
    ----------
    vector : np.ndarray
        The vector (in homogeneous coordinates) to be scale-normalized.

    Returns
    -------
    vector : np.ndarray
        An equivalent vector with scale component set to 1.

    Examples
    --------

    >>> import numpy as np
    >>> import ropy.transform as rtf
    >>> cartesian = np.array((1, 2, 3))
    >>> length = np.linalg.norm(cartesian)
    >>> length
    3.7416573867739413
    >>> cartesian / length
    array([0.26726124, 0.53452248, 0.80178373])
    >>> rtf.base.normalize_scale((*cartesian, length))
    array([0.26726124, 0.53452248, 0.80178373, 1.        ])

    """

    vector = np.asarray(vector)

    return vector / vector[-1]


def rotation_matrix(angle: float, u: ArrayLike, v: ArrayLike) -> np.ndarray:
    """Return a rotation matrix to rotate by angle in the plane span by u and v.

    The function creates a N-dimensional rotation matrix that rotates a point by
    a set angle inside an oriented plane. The plane is defined by the two basis
    vectors u and v and the (positive) direction of rotation is from u to v.

    For example, if ``u=(1,0,0,1)`` (the x-axis) and ``v=(0,1,0,1)`` (the
    y-axis) then the resulting matrix rotates vectors counter-clockwise around
    the z-axis, i.e., it rotates vectors in the x-y plane.

    Parameters
    ----------
    angle : float
        The amount (in radians) by which to rotate the plane.
    u : np.ndarray
        The first basis vectors (u,v) spanning the plane of
        rotation. The vector is given in homogeneous coordinates.
    v : np.ndarray
        The second basis vectors (u,v) that span the plane of rotation. The
        vector is given in homogeneous coordinates.

    Returns
    -------
    rotation_matrix : np.ndarray
        A matrix representing the rotation in homogeneous coordinates.

    Notes
    -----
    If u and v are not orthonormal, the resulting matrix is no longer a pure
    rotation.

    Examples
    --------
    .. plot::
        :include-source:

        >>> import numpy as np
        >>> import matplotlib.pyplot as plt
        >>> import ropy.transform as rtf
        >>> rotation = rtf.base.rotation_matrix(np.pi/4, (1, 0, 1), (0, 1, 1))
        >>> points = rtf.homogenize(np.array([[1, 1], [1, -1], [-1, 1], [-1, -1]]))
        >>> points_rotated = np.matmul(rotation, points.T)
        >>> fig, ax = plt.subplots()
        >>> ax.plot(points[:, 0], points[:, 1], points_rotated[0], points_rotated[1])
        >>> ax.legend(["Original", "Rotated 45°"])
        >>> fig.show()

    """

    # This implementation is based on a very insightful stackoverflow
    # comment
    # https://math.stackexchange.com/questions/197772/generalized-rotation-matrix-in-n-dimensional-space-around-n-2-unit-vector#comment453048_197778

    u = cartesianize(np.asarray(u))
    v = cartesianize(np.asarray(v))

    ndim = u.size

    rotation_matrix = np.eye(ndim)
    rotation_matrix += sin(angle) * (np.outer(v, u) - np.outer(u, v))
    rotation_matrix += (cos(angle) - 1) * (np.outer(u, u) + np.outer(v, v))

    homogeneous_rotation = np.eye(ndim + 1)
    homogeneous_rotation[:-1, :-1] = rotation_matrix

    return homogeneous_rotation


class Link:
    """A directional relationship between two Frames

    An abstract class that describes a transformation from a parent frame into a
    child frame. Its default use is to express a vector given in the parent
    frame using the child frame.

    Properties
    ----------
    transformation : np.ndarray
        A affine matrix describing the transformation from the parent frame to
        the child frame.

    Methods
    -------
    transform(x)
        Expresses the vector x (assumed to be given in the parent's frame) in
        the child's frame.


    """

    def __init__(self, parent: Frame, child: Frame) -> None:
        self.parent: Frame = parent
        self.child: Frame = child

    def transform(self, x: ArrayLike) -> np.ndarray:
        """Transform x (given in parent frame) into the child frame.

        Parameters
        ----------
        x : ArrayLike
            The vector expressed in the parent's frame

        Returns
        -------
        y : ArrayLike
            The vector expressed in the child's frame

        """
        raise NotImplementedError

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
        raise NotImplementedError


class InverseLink(Link):
    """A link between two frames based on the inverse of an existing Link.

    This class can be constructed from any link that implements
    __inverse_transform__. It is a tight wrapper around the original link and
    shares any parameters. Accordingly, if the original link updates, so will
    this link.
    
    """

    def __init__(self, link: Link) -> None:
        try:
            link.__inverse_transform__(np.zeros(link.child.ndim))
        except NotImplementedError:
            raise ValueError("Link doesn't implement __inverse_transform__.") from None

        super().__init__(link.child, link.parent)

        self._forward_link = link

    def transform(self, x: ArrayLike) -> np.ndarray:
        return self._forward_link.__inverse_transform__(x)


class Frame:
    """A frame representing a coordinate system.

    Each coordinate frame is a node in a directed graph where edges (type Link)
    describe transformations between different frames. Its default use is to
    transform coordinates between different coordinate frames.

    Methods
    -------
    transform(x, to_frame)
        Express the vector x - assumed to be in this frame - in the coordinate
        frame to_frame. If it is not possible to find a transformation between
        this frame and to_frame a RuntimeError will be raised.
    get_transformation_matrix(to_frame)
        Computes (and returns) the transformation matrix between this frame
        and to_frame.
    add_link(edge)
        Add a new transformation from this frame to another frame to the list of known
        transformations.

    """

    def __init__(self, ndim: int) -> None:
        self._links: List[Link] = list()
        self.ndim: int = ndim

    def transform(self, x: ArrayLike, to_frame: Frame, *, ignore_frames: List[Frame]=None) -> np.ndarray:
        """ Express the vector x in to_frame.

        Parameters
        ----------
        x : ArrayLike
            A vector expressed in this frame.
        to_frame : Frame
            The frame in which x should be expressed.
        ignore_frames : Frame
            Any frames that should be ignored when searching for a suitable transformation chain.

        Returns
        -------
        x_new : np.ndarray
            The vector x expressed to_frame.

        Raises
        ------
        RuntimeError
            If no suitable chain of transformations can be found, a RuntimeError is raised.

        """

        x_new = x
        for link in self._get_transform_chain(to_frame, ignore_frames):
            x_new = link.transform(x_new)

        return x_new

    def get_transformation_matrix(self, to_frame: Frame, *, ignore_frames: List[Frame]=None) -> np.ndarray:
        """ Compute the transformation matrix mapping from this frame into to_frame.

        Parameters
        ----------
        to_frame : Frame
            The frame in which x should be expressed.
        ignore_frames : Frame
            Any frames that should be ignored when searching for a suitable transformation chain.

        Returns
        -------
        tf_matrix : np.ndarray
            The matrix describing the transformation.

        Raises
        ------
        RuntimeError
            If no suitable chain of transformations can be found, a RuntimeError is raised.

        """

        tf_matrix = np.eye(self.ndim + 1)
        for link in self._get_transform_chain(to_frame, ignore_frames):
            tf_matrix = link.transformation @ tf_matrix

        return tf_matrix

    def add_link(self, edge: Link) -> None:
        """ Add an edge to the frame graph.

        The edge is directional and points from this frame to another (possibliy identical) frame.

        Parameters
        ----------
        edge : Link
            The transformation to add to the graph.

        Raises
        ------
        ValueError
            If the edge doesn't have this frame as parent.

        """

        if not edge.parent is self:
            raise ValueError("Can not add edge. This frame is not the edge's parent.")
        self._links.append(edge)

    def _get_transform_chain(self, to_frame: Frame, visited: List[Frame]=None) -> List[Link]:
        """ Find a chain of transformations from this frame to to_frame.

        This function performs a recursive depth-first search on the frame graph defined by this
        frame and its (recursively) connected links. Previously visited frames are pruned to avoid
        cycles.

        Parameters
        ----------
        to_frame : Frame
            The frame to reach.
        visited : List[Frame]
            The frames that were already checked

        Returns
        -------
        chain : List[Link]
            A list of links that can transform from this frame to to_frame.

        """
        if to_frame is self:
            return []


        if visited is None:
            visited = [self]
        else:
            visited.append(self)

        for link in self._links:
            child = link.child
            if child in visited:
                continue

            try:
                new_links = child._get_transform_chain(to_frame, visited=visited)
            except RuntimeError:
                continue
            
            return [link] + new_links


        raise RuntimeError(
                "Did not find a transformation chain to the target frame."
            )

