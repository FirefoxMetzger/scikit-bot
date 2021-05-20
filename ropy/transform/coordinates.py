from __future__ import annotations  # life's too short for comments
import numpy as np
from numpy.core.records import array
from numpy.typing import ArrayLike
from typing import List, Callable

from .base import rotation_matrix
from .base import translate, rotate


class Link:
    """A directional relationship between two Frames

    An abstract class that describes a transformation from a parent frame into a
    child frame. Its default use is to express a vector given in the parent
    frame using the child frame.

    Properties
    ----------
    transformation : np.array
        A affine matrix describing the transformation from the parent frame to
        the child frame.

    Methods
    -------
    transform(x)
        Expresses the vector x (assumed to be given in the parent's frame) in
        the child's frame.


    """

    def __init__(self, parent: Frame, child: Frame):
        self.parent: Frame = parent
        self.child: Frame = child

    def transform(self, x: ArrayLike) -> np.array:
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

    @property
    def transformation(self) -> np.array:
        """The transformation matrix mapping the parent to the child frame."""
        raise NotImplementedError


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

    def __init__(self, ndim):
        self._links: List[Link] = list()
        self.ndim: int = ndim

    def transform(self, x: ArrayLike, to_frame: Frame, *, ignore_frames: List[Frame]=None) -> np.array:
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
        x_new : np.array
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

    def get_transformation_matrix(self, to_frame: Frame, *, ignore_frames: List[Frame]=None) -> np.array:
        """ Compute the transformation matrix mapping from this frame into to_frame.

        Parameters
        ----------
        to_frame : Frame
            The frame in which x should be expressed.
        ignore_frames : Frame
            Any frames that should be ignored when searching for a suitable transformation chain.

        Returns
        -------
        tf_matrix : np.array
            The matrix describing the transformation.

        Raises
        ------
        RuntimeError
            If no suitable chain of transformations can be found, a RuntimeError is raised.

        """

        tf_matrix = np.eye(self.dim)
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
                "Did not find a transformation chain to the target frame found."
            )


class FixedLink(Link):
    """ A link representing a fixed transformation.

    A fixed link has no parameters and remains constant after it has been
    initialized.

    Methods
    -------
    FixedLink(parent, child, transformation)
        Initialize a new fixed link. Transformation is a callable that transforms a vector 
        from the parent frame to the child frame.

    """

    def __init__(self, parent: Frame, child: Frame, transformation:Callable[[ArrayLike], np.array], **kwargs):
        """Initialize a new fixed link.

        Parameters
        ----------
        parent : Frame
            The frame in which vectors are specified.
        child : Frame
            The frame into which this link transforms vectors.
        transfomration : Callable[[ArrayLike], np.array]
            A callable that takes a vector - in the parent frame - as input and returns the vector in the child frame.
        """

        super().__init__(parent, child, **kwargs)

        self._transform = transformation

        mapped_basis = list()
        for basis in np.eye(parent.ndim):
            mapped_basis.append(transformation(basis))
        
        self._tf_matrix = np.column_stack(mapped_basis)

    def transform(self, x: ArrayLike) -> np.array:
        return self._transform(x)

    @property
    def transformation(self) -> np.array:
        return self._tf_matrix


def transform(new_frame: np.array) -> np.array:
    """Compute the homogeneous transformation matrix from the current coordinate
    system into a new coordinate system.

    Given the pose of the new reference frame ``new_frame`` in the current
    reference frame, compute the homogeneous transformation matrix from the
    current reference frame into the new reference frame.
    ``transform(new_frame)`` can, for example, be used to get the transformation
    from the corrdinate frame of the current link in a kinematic chain to the
    next link in a kinematic chain. Here, the next link's origin (``new_frame``)
    is specified relative to the current link's origin, i.e., in the current
    link's coordinate system.


    Parameters
    ----------
    new_frame : np.array
        The pose of the new coordinate system's origin. This is a 6-dimensional
        vector consisting of the origin's position and the frame's orientation
        (xyz Euler Angles): [x, y, z, alpha, beta, gamma].

    Returns
    -------
    transformation_matrix : np.ndarray
        A 4x4 matrix representing the homogeneous transformation.


    Notes
    -----
    For performance reasons, it is better to sequentially apply multiple
    transformations to a vector than to first multiply a sequence of
    transformations and then apply them to a vector afterwards.

    """

    # Note: this is a naive implementation, but avoids a scipy dependency
    # if scipy does get introduced later, it can be substituted by
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.transform.Rotation.from_euler.html

    new_frame = np.asarray(new_frame)
    alpha, beta, gamma = -new_frame[3:]

    rot_x = rotation_matrix(alpha, (0, 1, 0, 1), (0, 0, 1, 1))[:-1, :-1]
    rot_y = rotation_matrix(beta, (1, 0, 0, 1), (0, 0, 1, 1))[:-1, :-1]
    rot_z = rotation_matrix(gamma, (1, 0, 0, 1), (0, 1, 0, 1))[:-1, :-1]

    # Note: apply inverse rotation
    rot = np.matmul(rot_z, np.matmul(rot_y, rot_x))

    transform = np.eye(4)
    transform[:3, :3] = rot
    transform[:3, 3] = -np.matmul(rot, new_frame[:3])

    return transform


def inverse_transform(old_frame: np.array) -> np.array:
    """Compute the homogeneous transformation matrix from the current coordinate
    system into the old coordinate system.

    Given the pose of the current reference frame in the old reference frame
    ``old_frame``, compute the homogeneous transformation matrix from the new
    reference frame into the old reference frame. For example,
    ``inverse_transform(camera_frame)`` can, be used to compute the
    transformation from a camera's coordinate frame to the world's coordinate
    frame assuming the camera frame's pose is given in the world's coordinate
    system.

    Parameters
    ----------
    old_frame : {np.array, None}
        The pose of the old coordinate system's origin. This is a 6-dimensional
        vector consisting of the origin's position and the frame's orientation
        (xyz Euler Angles): [x, y, z, alpha, beta, gamma].

    Returns
    -------
    transformation_matrix : np.ndarray
        A 4x4 matrix representing the homogeneous transformation.


    Notes
    -----
    For performance reasons, it is better to sequentially apply multiple
    transformations to a vector than to first multiply a sequence of
    transformations and then apply them to a vector afterwards.

    """

    # Note: this is a naive implementation, but avoids a scipy dependency
    # if scipy does get introduced later, it can be substituted by
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.transform.Rotation.from_euler.html

    old_frame = np.asarray(old_frame)
    alpha, beta, gamma = old_frame[3:]

    rot_x = rotation_matrix(alpha, (0, 1, 0, 1), (0, 0, 1, 1))[:-1, :-1]
    rot_y = rotation_matrix(beta, (1, 0, 0, 1), (0, 0, 1, 1))[:-1, :-1]
    rot_z = rotation_matrix(gamma, (1, 0, 0, 1), (0, 1, 0, 1))[:-1, :-1]

    transform = np.eye(4)
    transform[:3, :3] = np.matmul(rot_x, np.matmul(rot_y, rot_z))
    transform[:3, 3] = old_frame[:3]

    return transform


def transform_between(old_frame: np.array, new_frame: np.array) -> np.array:
    """Compute the homogeneous transformation matrix between two frames.

    ``transform_between(old_frame, new_frame)`` computes the
    transformation from the corrdinate system with pose ``old_frame`` to
    the corrdinate system with pose ``new_frame`` where both origins are
    expressed in the same reference frame, e.g., the world's coordinate frame.
    For example, ``transform_between(camera_frame, tool_frame)`` computes
    the transformation from a camera's coordinate system to the tool's
    coordinate system assuming the pose of both corrdinate frames is given in
    a shared world frame (or any other __shared__ frame of reference).

    Parameters
    ----------
    old_frame : np.array
        The pose of the old coordinate system's origin. This is a 6-dimensional
        vector consisting of the origin's position and the frame's orientation
        (xyz Euler Angles): [x, y, z, alpha, beta, gamma].
    new_frame : np.array
        The pose of the new coordinate system's origin. This is a 6-dimensional
        vector consisting of the origin's position and the frame's orientation
        (xyz Euler Angles): [x, y, z, alpha, beta, gamma].

    Returns
    -------
    transformation_matrix : np.ndarray
        A 4x4 matrix representing the homogeneous transformation.

    Notes
    -----
    If the reference frame and ``old_frame`` are identical, use ``transform``
    instead.

    If the reference frame and ``new_frame`` are identical, use
    ``transformInverse`` instead.

    For performance reasons, it is better to sequentially apply multiple
    transformations to a vector than to first multiply a sequence of
    transformations and then apply them to a vector afterwards.

    """

    return np.matmul(transform(new_frame), inverse_transform(old_frame))
