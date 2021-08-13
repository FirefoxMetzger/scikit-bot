from typing import Union, List

from ... import transform as tf
from ._transform_factory.factory import graph_factory


def transform_graph_from_sdf(sdf: str, *, unwrap=True, axis=-1, shape=(1,)) -> Union[tf.Frame, List[tf.Frame]]:
    """Create a frame graph from a sdformat string.

    .. versionadded:: 0.5.0

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
        The axis along which data is stored. All other axis are batch dimensions.
    shape : tuple
        A tuple describing the shape of elements that this graph should transform.

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

    graph_list  = graph_factory(sdf, unwrap=False)
    for graph in graph_list:
        graph.resolve()

    if unwrap and len(graph_list) == 1:
        return graph_list[0].nodes[graph.root_node]
    else:
        return [graph.nodes[graph.root_node] for graph in graph_list]
