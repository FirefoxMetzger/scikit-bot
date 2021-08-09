from __future__ import annotations  # life's too short for comments
from math import sin, cos
from numpy.typing import ArrayLike
from typing import List, Tuple, Union, Callable
import numpy as np


class Link:
    """A directional relationship between two Frames

    An abstract class that describes a transformation from a parent frame into a
    child frame. Its default use is to express a vector given in the parent
    frame using the child frame.

    Attributes
    ----------
    transformation : np.ndarray
        A affine matrix describing the transformation from the parent frame to
        the child frame.

    Notes
    -----
    :attr:`Link.transformation` may raise a ``NotImplementedError`` if the link
    doesn't support affine transformation matrices, or if the matrix doesn't exist.

    """

    def __init__(self, parent_dim: int, child_dim: int) -> None:
        self.parent_dim: int = parent_dim
        self.child_dim: int = child_dim

    def __call__(
        self, parent: Frame, child: Frame = None, *, add_inverse: bool = True
    ) -> Frame:
        """Add this link to the parent frame.

        Parameters
        ----------
        parent : Frame
            The Frame from which vectors originate.
        child : Frame
            The Frame in which vectors are expressed after they were mapped by
            this link's transform. If None, a new child will be created.
        add_inverse : bool
            Also add the inverse link to the child if this Link is invertible.
            Defaults to ``True``.

        Returns
        -------
        child : Frame
            The Frame in which vectors are expressed after they were mapped
            by this link's transform.

        """

        if child is None:
            child = Frame(self.child_dim)

        parent.add_link(self, child)

        if add_inverse:
            try:
                child.add_link(self.invert(), parent)
            except ValueError:
                # inverse does not exist
                pass

        return child

    def invert(self) -> Frame:
        """Returns a new link that is the inverse of this link.

        The links share parameters, i.e., if the transform of a link changes,
        the transform of its inverse does also.
        """
        return InvertLink(self)

    def transform(self, x: ArrayLike) -> np.ndarray:
        """Expresses the vector x (assumed to be given in the parent's frame) in
        the child's frame.

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


class InvertLink(Link):
    """Inverse of an existing Link.

    This class can be constructed from any link that implements
    __inverse_transform__. It is a tight wrapper around the original link and
    shares any parameters. Accordingly, if the original link updates, so will
    this link.

    Parameters
    ----------
    link : Link
        The link to be inverted. It must implement __inverse_transform__.

    """

    def __init__(self, link: Link) -> None:
        try:
            link.__inverse_transform__(np.zeros(link.child_dim))
        except NotImplementedError:
            raise ValueError("Link doesn't implement __inverse_transform__.") from None

        super().__init__(link.child_dim, link.parent_dim)

        self._forward_link = link

    def transform(self, x: ArrayLike) -> np.ndarray:
        return self._forward_link.__inverse_transform__(x)


class Frame:
    """Representation of a coordinate system.

    Each coordinate frame is a node in a directed graph where edges
    (:class:`skbot.transform.Link`) describe transformations between frames. This
    transformation is not limited to neighbours, but works between any two
    frames that share a chain of links pointing from a parent to the
    (grand-)child.

    Parameters
    ----------
    ndim : int
        Number of coordinate dimensions.
    name : str
        The name of this coordinate frame. Defaults to ``None``.

    """

    def __init__(self, ndim: int, *, name: str = None) -> None:
        self._children: List[Tuple(Frame, Link)] = list()
        self.ndim: int = ndim
        self.name = name

    def transform(
        self,
        x: ArrayLike,
        to_frame: Union[Frame, str],
        *,
        ignore_frames: List[Frame] = None,
    ) -> np.ndarray:
        """Express the vector x in to_frame.

        Express the vector x - assumed to be in this frame - in the coordinate
        frame to_frame. If it is not possible to find a transformation between
        this frame and to_frame a RuntimeError will be raised.

        Parameters
        ----------
        x : ArrayLike
            A vector expressed in this frame.
        to_frame : Frame, str
            The frame in which x should be expressed. If it is a string,
            :func:`~transform` will search for a child frame with the given
            string as name. In case of duplicate names in a frame graph, the
            first one found is used.
        ignore_frames : Frame
            Any frames that should be ignored when searching for a suitable
            transformation chain. Note that this currently does not support
            string aliases.

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

    def get_affine_matrix(
        self, to_frame: Union[Frame, str], *, ignore_frames: List[Frame] = None
    ) -> np.ndarray:
        """Affine transformation matrix to ``to_frame`` (if existant).

        Parameters
        ----------
        to_frame : Frame
            The frame in which x should be expressed.
        ignore_frames : Frame
            Any frames that should be ignored when searching for a suitable
            transformation chain.

        Returns
        -------
        tf_matrix : np.ndarray
            The matrix describing the transformation.

        Raises
        ------
        RuntimeError
            If no suitable chain of transformations can be found, a RuntimeError
            is raised.

        Notes
        -----
        The affine transformation matrix between two frames only exists if the
        transformation chain is linear in ``self.ndim+1`` dimensions. Requesting
        a non-existing affine matrix will raise an Exception. In practice, this
        means that each link along the transformation chain needs to implement
        :attr:`skbot.transform.Link.transformation`.

        """

        tf_matrix = np.eye(self.ndim + 1)
        for link in self._get_transform_chain(to_frame, ignore_frames):
            tf_matrix = link.affine_matrix @ tf_matrix

        return tf_matrix

    def add_link(self, edge: Link, child: Frame) -> None:
        """Add an edge to the frame graph.

        The edge is directional and points from this frame to another (possibliy
        identical) frame.

        Parameters
        ----------
        edge : Link
            The transformation to add to the graph.
        child : Frame
            The frame that following this link leads to.

        """

        self._children.append((child, edge))

    def _get_transform_chain(
        self, to_frame: Union[Frame, str], visited: List[Frame] = None
    ) -> List[Link]:
        """Find a chain of transformations from this frame to to_frame.

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

        Notes
        -----
        DFS (depth-first search) does not guarantee the shortest chain to be returned.

        """
        if to_frame is self or self.name == to_frame:
            return []

        if visited is None:
            visited = [self]
        else:
            visited.append(self)

        for child, link in self._children:
            if child in visited:
                continue

            try:
                new_links = child._get_transform_chain(to_frame, visited=visited)
            except RuntimeError:
                continue

            return [link] + new_links

        raise RuntimeError("Did not find a transformation chain to the target frame.")

    def find_frame(self, path: str, *, ignore_frames: List[Frame] = None) -> Frame:
        """Find a frame matching a given path.

        This method allows you to find reachable frames using an xpath inspired
        syntax. Path elements are spearated using the `/` character. Each
        element of the path is the name of a frame. For example,
        ``world/link1/link2/gripper``, denotes a sequence of 4 frames with names
        ``["world", "link1", "link2", "gripper"]``. The final frame in the path
        (gripper) is returned.

        By default an element along the path is directly connected to its next
        element. In the previous example this means that there must exist a
        direct link from "world" to "link1". An exception to this rule is the
        use of an ellipsis (...), in which case an element must be connected to
        its next element by a transformation chain (a sequence of
        links).

        The following path elements have special meanings:

            - Ellipsis (``...``)
                Indicates that the previous frame and the next frame are
                connected by a transformation chain instead of being connected
                directly.
            - None (``//``)
                Omitting a name indicates that the name of this frame is None.


        Parameters
        ----------
        xpath : str
            A xpath string describing the frame to search for.
        ignore_frames : List[Frame]
            Any frames that should be ignored when matching the path.

        Returns
        -------
        matched_frame : Frame
            A frame matching the given path.


        Notes
        -----
        .. versionadded:: 0.3.0

        In directed graphs there is no clear notion of search order; hence it is
        undefined which frame is found if multiple matches for the path exist.
        In this case an arbitrary match is returned, and you should not count on
        the result to be deterministic.

        Because ``...`` and ``//`` have special meaning, frames with names
        ``"..."`` or ``""`` will be ignored by this method and can not be found.
        Similarly, frames that use slashes, e.g. ``namespace/my_frame``, will be
        ignored and instead the sequences ``["namespace", "my_frame"]`` will be
        matched.

        Each element of the path is assumed to represent a unique frame. This
        means that circular paths will not be matched.

        """

        parts = path.split("/")
        part = parts.pop(0)

        indirect = False
        while len(parts) > 0 and part == "...":
            indirect = True
            part = parts.pop(0)

        if part == "...":
            raise ValueError(f"Path ends with ellipsis: {path}")

        part = None if part == "" else part

        if len(parts) == 0 and self.name == part:
            return self
        elif not indirect and self.name != part:
            raise RuntimeError(f"No match for {path}.")
        elif len(parts) > 0 and self.name == part:
            sub_path = "/".join(parts)
        else:
            parts = ["...", part] + parts
            sub_path = "/".join(parts)

        if ignore_frames is None:
            ignore_frames = []

        local_ignore = [self]
        local_ignore.extend(ignore_frames)

        child_frame: Frame
        for child_frame, _ in self._children:
            if child_frame in local_ignore:
                continue

            try:
                return child_frame.find_frame(sub_path, ignore_frames=local_ignore)
            except RuntimeError:
                continue
        else:
            raise RuntimeError(f"No match for {path}.")


class CustomLink(Link):
    """A link representing a custom transformation.

    Initialize a new link from the callable ``transformation`` that transforms a
    vector from the parent frame to the child frame. This link can represent
    arbitrary transformations between two frames.

    Parameters
    ----------
    parent : Frame
        The frame in which vectors are specified.
    child : Frame
        The frame into which this link transforms vectors.
    transfomration : Callable[[ArrayLike], np.ndarray]
        A callable that takes a vector - in the parent frame - as input and
        returns the vector in the child frame.

    Notes
    -----
    This function does not implement :func:`Link.__inverse_transform__`.

    """

    def __init__(
        self,
        parent_dim: int,
        child_dim: int,
        transformation: Callable[[ArrayLike], np.ndarray],
    ) -> None:
        """Initialize a new custom link."""

        super().__init__(parent_dim, child_dim)
        self._transform = transformation

    def transform(self, x: ArrayLike) -> np.ndarray:
        return self._transform(x)
