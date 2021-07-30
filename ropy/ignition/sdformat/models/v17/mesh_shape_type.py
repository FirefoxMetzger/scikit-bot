from dataclasses import dataclass, field
from typing import List

__NAMESPACE__ = "sdformat/mesh_shape"


@dataclass
class MeshType:
    """
    Parameters
    ----------
    uri: Mesh uri
    submesh: Use a named submesh. The submesh must exist in the mesh
        specified by the uri
    scale: Scaling factor applied to the mesh
    """

    class Meta:
        name = "meshType"

    uri: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    submesh: List["MeshType.Submesh"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    scale: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
            "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
        },
    )

    @dataclass
    class Submesh:
        """
        Parameters
        ----------
        name: Name of the submesh within the parent mesh
        center: Set to true to center the vertices of the submesh at
            0,0,0. This will effectively remove any transformations on
            the submesh before the poses from parent links and models
            are applied.
        """

        name: List[str] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        center: List[bool] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
