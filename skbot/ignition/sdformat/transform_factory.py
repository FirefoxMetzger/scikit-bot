from typing import Union, List, Tuple, Dict

from ... import transform as tf
from .load_as_generic import loads_generic
from .generic_sdf.world import World


def to_frame_graph(
    sdf: str, *, unwrap: bool = True, shape: Tuple[int] = (3,), axis: int = -1
) -> Union[tf.Frame, List[tf.Frame]]:
    """Create a frame graph from a sdformat string.

    .. versionadded:: 0.6.0
        This function has been added to the library.

    Parameters
    ----------
    sdf: str
        A SDFormat XML string describing one (or many) worlds.
    unwrap : bool
        If True (default) and the sdf only contains a single light, model, or
        world element return that element's frame. If the sdf contains multiple
        lights, models, or worlds a list of root frames is returned. If False,
        always return a list of frames.
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
    :func:`skbot.transform.Frame.transform_chain`. For example if there is a
    joint named "robot_joint0" its link can be retrieved using::

        child_frame = frame_graph.find_frame(".../robot_joint0")
        parent_frame = frame_graph.find_frame(".../robot_joint0_parent")
        link = child_frame.transform_chain(child_frame)[0]
    """

    root = loads_generic(sdf)
    worlds = list()
    for world in root.worlds:
        world_frames = world.declared_frames()
        world_graph = world.to_dynamic_graph(world_frames, shape=shape, axis=axis)
        worlds.append(world_graph)

    if unwrap and len(worlds) == 1:
        return worlds[0]
    else:
        return worlds
