from dataclasses import dataclass, field
from typing import List, Optional

__NAMESPACE__ = "sdformat/v1.4/geometry.xsd"


@dataclass
class Geometry:
    """
    The shape of the visual or collision object.

    Parameters
    ----------
    empty: You can use the empty tag to make empty geometries.
    box: Box shape
    cylinder: Cylinder shape
    heightmap: A heightmap based on a 2d grayscale image.
    image: Extrude a set of boxes from a grayscale image.
    mesh: Mesh shape
    plane: Plane shape
    sphere: Sphere shape
    """

    class Meta:
        name = "geometry"

    empty: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    box: Optional["Geometry.Box"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    cylinder: Optional["Geometry.Cylinder"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    heightmap: Optional["Geometry.Heightmap"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    image: Optional["Geometry.Image"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    mesh: Optional["Geometry.Mesh"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    plane: Optional["Geometry.Plane"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    sphere: Optional["Geometry.Sphere"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )

    @dataclass
    class Box:
        """
        Box shape.

        Parameters
        ----------
        size: The three side lengths of the box. The origin of the box
            is in its geometric center (inside the center of the box).
        """

        size: str = field(
            default="1 1 1",
            metadata={
                "type": "Element",
                "namespace": "",
                "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
            },
        )

    @dataclass
    class Cylinder:
        """
        Cylinder shape.

        Parameters
        ----------
        radius: Radius of the cylinder
        length: Length of the cylinder along the z axis
        """

        radius: float = field(
            default=1.0,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        length: float = field(
            default=1.0,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

    @dataclass
    class Heightmap:
        """
        A heightmap based on a 2d grayscale image.

        Parameters
        ----------
        uri: URI to a grayscale image file
        size: The size of the heightmap in world units.       When
            loading an image: "size" is used if present, otherwise
            defaults to 1x1x1.       When loading a DEM: "size" is used
            if present, otherwise defaults to true size of DEM.
        pos: A position offset.
        texture: The heightmap can contain multiple textures. The order
            of the texture matters. The first texture will appear at the
            lowest height, and the last texture at the highest height.
            Use blend to control the height thresholds and fade between
            textures.
        blend: The blend tag controls how two adjacent textures are
            mixed. The number of blend elements should equal one less
            than the number of textures.
        use_terrain_paging: Set if the rendering engine will use terrain
            paging
        """

        uri: str = field(
            default="__default__",
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        size: str = field(
            default="1 1 1",
            metadata={
                "type": "Element",
                "namespace": "",
                "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
            },
        )
        pos: str = field(
            default="0 0 0",
            metadata={
                "type": "Element",
                "namespace": "",
                "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
            },
        )
        texture: List["Geometry.Heightmap.Texture"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        blend: List["Geometry.Heightmap.Blend"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        use_terrain_paging: bool = field(
            default=False,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

        @dataclass
        class Texture:
            """The heightmap can contain multiple textures.

            The order of the texture matters. The first texture will
            appear at the lowest height, and the last texture at the
            highest height. Use blend to control the height thresholds
            and fade between textures.

            Parameters
            ----------
            size: Size of the applied texture in meters.
            diffuse: Diffuse texture image filename
            normal: Normalmap texture image filename
            """

            size: float = field(
                default=10.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            diffuse: str = field(
                default="__default__",
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            normal: str = field(
                default="__default__",
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

        @dataclass
        class Blend:
            """The blend tag controls how two adjacent textures are mixed.

            The number of blend elements should equal one less than the
            number of textures.

            Parameters
            ----------
            min_height: Min height of a blend layer
            fade_dist: Distance over which the blend occurs
            """

            min_height: float = field(
                default=0.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            fade_dist: float = field(
                default=0.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

    @dataclass
    class Image:
        """
        Extrude a set of boxes from a grayscale image.

        Parameters
        ----------
        uri: URI of the grayscale image file
        scale: Scaling factor applied to the image
        threshold: Grayscale threshold
        height: Height of the extruded boxes
        granularity: The amount of error in the model
        """

        uri: str = field(
            default="__default__",
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        scale: float = field(
            default=1.0,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        threshold: int = field(
            default=200,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        height: float = field(
            default=1.0,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        granularity: int = field(
            default=1,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

    @dataclass
    class Mesh:
        """
        Mesh shape.

        Parameters
        ----------
        uri: Mesh uri
        submesh: Use a named submesh. The submesh must exist in the mesh
            specified by the uri
        scale: Scaling factor applied to the mesh
        """

        uri: str = field(
            default="__default__",
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        submesh: Optional["Geometry.Mesh.Submesh"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        scale: str = field(
            default="1 1 1",
            metadata={
                "type": "Element",
                "namespace": "",
                "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
            },
        )

        @dataclass
        class Submesh:
            """Use a named submesh.

            The submesh must exist in the mesh specified by the uri

            Parameters
            ----------
            name: Name of the submesh within the parent mesh
            center: Set to true to center the vertices of the submesh at
                0,0,0. This will effectively remove any transformations
                on the submesh before the poses from parent links and
                models are applied.
            """

            name: str = field(
                default="__default__",
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            center: bool = field(
                default=False,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

    @dataclass
    class Plane:
        """
        Plane shape.

        Parameters
        ----------
        normal: Normal direction for the plane
        size: Length of each side of the plane
        """

        normal: str = field(
            default="0 0 1",
            metadata={
                "type": "Element",
                "namespace": "",
                "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
            },
        )
        size: str = field(
            default="1 1",
            metadata={
                "type": "Element",
                "namespace": "",
                "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+)((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
            },
        )

    @dataclass
    class Sphere:
        """
        Sphere shape.

        Parameters
        ----------
        radius: radius of the sphere
        """

        radius: float = field(
            default=1.0,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
