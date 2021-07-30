from dataclasses import dataclass, field
from typing import List
from .box_shape_type import BoxType
from .cylinder_shape_type import CylinderType
from .heightmap_shape_type import HeightmapType
from .image_shape_type import ImageType
from .mesh_shape_type import MeshType
from .plane_shape_type import PlaneType
from .polyline_shape_type import PolylineType
from .sphere_shape_type import SphereType

__NAMESPACE__ = "sdformat/geometry"


@dataclass
class GeometryType:
    """
    Parameters
    ----------
    empty: You can use the empty tag to make empty geometries.
    box: Box shape
    cylinder: Cylinder shape
    heightmap: A heightmap based on a 2d grayscale image.
    image: Extrude a set of boxes from a grayscale image.
    mesh: Mesh shape
    plane: Plane shape
    polyline: Defines an extruded polyline shape
    sphere: Sphere shape
    """

    class Meta:
        name = "geometryType"

    empty: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    box: List[BoxType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    cylinder: List[CylinderType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    heightmap: List[HeightmapType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    image: List[ImageType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    mesh: List[MeshType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    plane: List[PlaneType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    polyline: List[PolylineType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    sphere: List[SphereType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
