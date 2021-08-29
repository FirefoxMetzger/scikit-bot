from typing import Union, List, Tuple

from ... import transform as tf
from ._transform_factory.scopes import LightScope, ModelScope, Scope, WorldScope
from ._transform_factory.factory import transform_factory


def to_frame_graph(
    sdf: str, *, unwrap: bool = True, shape: Tuple[int] = (3,), axis: int = -1
) -> Union[tf.Frame, List[tf.Frame]]:
    """Create a frame graph from a sdformat string.

    .. versionadded:: 0.6.0
        This function has been added to the library.

    Parameters
    ----------
    sdf: str
        A string containing SDFormat XML.
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

    scope_list: List[Scope] = transform_factory(sdf)
    frame_list: List[tf.Frame] = list()
    for scope in scope_list:
        scope.build_scaffolding()
        scope.resolve_links(shape=shape, axis=axis)

        if isinstance(scope, WorldScope):
            frame_list.append(scope.get("world", scaffolding=False))
        elif isinstance(scope, ModelScope):
            frame = scope.get(scope.canonical_link, scaffolding=False)
            frame_list.append(frame)
        else:
            scope: LightScope
            frame = scope.get(scope.name, scaffolding=False)
            frame_list.append(frame)

    if unwrap and len(frame_list) == 1:
        return frame_list[0]
    else:
        return frame_list
