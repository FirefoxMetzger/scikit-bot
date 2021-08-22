from typing import Union, List, Tuple

from ... import transform as tf
from ._transform_factory.scopes import LightScope, ModelScope, Scope, WorldScope
from ._transform_factory.factory import transform_factory


def to_frame_graph(
    sdf: str, *, unwrap: bool = True, axis: int = -1, shape: Tuple[int] = (3,)
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
    axis : int
        The axis along which elements are stored. All other axis are batch dimensions.
    shape : tuple
        A tuple describing the shape of elements that this graph should transform. Defaults
        to (3,), which is the shape of a single 3D vector in euclidian space.

    Returns
    -------
    frame : Union[Frame, List[Frame]]
        A :class:`skbot.transform.Frame` or list of Frames depending on the value of
        ``unwrap`` and the number of elements in the SDF.
    links : Dict[str, Frames]
        A dict of (named) links in the graph.

    See Also
    --------
    :mod:`skbot.transform`

    """

    scope_list:List[Scope] = transform_factory(sdf)
    frame_list:List[tf.Frame] = list()
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