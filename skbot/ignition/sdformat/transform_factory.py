from typing import Union, List, Tuple, Dict
from itertools import chain

from ... import transform as tf
from .load_as_generic import loads_generic
from .generic_sdf.world import World


def to_frame_graph(
    sdf: str,
    *,
    unwrap: bool = True,
    insert_world_frame: bool = True,
    shape: Tuple[int] = (3,),
    axis: int = -1
) -> Union[tf.Frame, List[tf.Frame]]:
    """Create a frame graph from a sdformat string.

    .. versionadded:: 0.8.0
        Added the ability to limit loading to worlds
    .. versionadded:: 0.6.0
        This function has been added to the library.

    Parameters
    ----------
    sdf : str
        A SDFormat XML string describing one (or many) worlds.
    unwrap : bool
        If True (default) and the sdf only contains a single light, model, or
        world element return that element's frame. If the sdf contains multiple
        lights, models, or worlds a list of root frames is returned. If False,
        always return a list of frames.
    insert_world_frame : bool
        If ``False``, creation of frame graphs is restricted to world elements
        contained in the provided SDF. This is because non-world elements
        (simulation fragments) may refer to a ``world`` frame that is defined
        outside of the provided SDF and hence the full graph can't be
        determined. As a consequence, any ``model``, ``actor``, or ``light``
        elements are ignored.

        If ``True`` (default), this function will insert a ``world`` frame into
        the graph of each simulation fragment (non-world element) to allow
        smooth construction of the frame graph.

        The default is ``True``; however, it will change to ``False`` starting
        with scikit-bot v1.0.

    shape : tuple
        A tuple describing the shape of elements that the resulting graph should
        transform. This can be used to add batch dimensions to the graph, for
        example to perform vectorized computation on multiple instances of the
        same world in different states, or for batched coordinate
        transformation. Defaults to (3,), which is the shape of a single 3D
        vector in euclidian space.
    axis : int
        The axis along which elements are stored. The axis must have length 3
        (since SDFormat describes 3 dimensional worlds), and all other axis are
        considered batch dimensions. Defaults to -1.

    Returns
    -------
    frame_graph : Union[Frame, List[Frame]]
        A :class:`skbot.transform.Frame` or list of Frames depending on the value of
        ``unwrap`` and the number of elements in the SDF's root element.

    See Also
    --------
    :mod:`skbot.transform`

    Notes
    -----
    Frames inside the graph are named after the frames defined by the SDF. You can
    retrieve them by searching for them using :func:`skbot.transform.Frame.find_frame`.

    Joins are implicit within the frame graph. The joint frame that is attached
    to the child frame is named after the joint (<joint_name>), and the
    (implicit) joint frame attached to the parent is named
    (<joint_name>_parent). The link between the two frames can be retrieved via
    :func:`skbot.transform.Frame.links_between`. For example if there is a
    joint named "robot_joint0" its link can be retrieved using::

        child_frame = frame_graph.find_frame(".../robot_joint0")
        parent_frame = frame_graph.find_frame(".../robot_joint0_parent")
        link = child_frame.links_between(child_frame)[0]
    """

    root = loads_generic(sdf)
    declared_frames = root.declared_frames()
    dynamic_graphs = root.to_dynamic_graph(declared_frames, shape=shape, axis=axis)

    if insert_world_frame:
        candidates = dynamic_graphs.values()
    else:
        candidates = [dynamic_graphs["worlds"]]

    graphs = list()
    for x in chain([x for x in candidates]):
        graphs.extend(x)

    if len(graphs) == 0:
        raise ValueError("No graphs could be loaded from the provided SDF.")

    if unwrap and len(graphs) == 1:
        return graphs[0]
    else:
        return graphs
