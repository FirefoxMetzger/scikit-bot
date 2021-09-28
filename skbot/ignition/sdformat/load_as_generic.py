from . import sdformat
from .generic_sdf.sdf import Sdf


def loads_generic(sdf: str):
    """Turn a SDFormat string into an object tree.

    The returned object tree is oppinionated. In addition to converting the
    tree, it does the following:

    - Some SDFormat elements are ignored/not implemented (contributions welcome!)
    - its variable names differ from SDFormat

        - If an element may have multiple children of the same kind, they
          corresponding attribute uses plural instead of singular, e.g.
          ``models`` instead of ``model``.
        - If different SDF versions use different names for the same variable,
          they are converted into the name used in the most recent SDFormat
          version. Old names are still available via a @property and will raise
          a depreciation warning.

    - it converts all vectors to numpy arrays
    - it resolves includes, removes them, and inserts the included element
    - it appends __model__ to frame references where necessary

    Parameters
    ----------
    sdf : str
        A string containing SDFormat XML.

    Returns
    -------
    root : generic.Sdf
        The root/sdf element of the generic SDF representation.

    """

    version = sdformat.get_version(sdf)
    specific_tree = sdformat.loads(sdf)
    generic_tree = Sdf.from_specific(specific_tree, version=version)

    return generic_tree
