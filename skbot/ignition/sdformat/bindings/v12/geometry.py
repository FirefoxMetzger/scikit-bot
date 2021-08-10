from dataclasses import dataclass, field
from typing import List, Optional

__NAMESPACE__ = "sdformat/v1.2/geometry.xsd"


@dataclass
class Geometry:
    """
    The shape of the visual or collision object.

    Parameters
    ----------
    box: Box shape
    sphere: Sphere shape
    cylinder: Cylinder shape
    mesh: Mesh shape
    plane: Plane shape
    image: Extrude a set of boxes from a grayscale image.
    heightmap: A heightmap based on a 2d grayscale image.
    """

    class Meta:
        name = "geometry"

    box: Optional["Geometry.Box"] = field(
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
    cylinder: Optional["Geometry.Cylinder"] = field(
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
    image: Optional["Geometry.Image"] = field(
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
                "required": True,
                "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
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
                "required": True,
            },
        )

    @dataclass
    class Cylinder:
        """
        Cylinder shape.

        Parameters
        ----------
        radius: Radius of the cylinder
        length: Length of the cylinder
        """

        radius: float = field(
            default=1.0,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        length: float = field(
            default=1.0,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )

    @dataclass
    class Mesh:
        """
        Mesh shape.

        Parameters
        ----------
        filename: Mesh filename. DEPRECATED
        uri: Mesh uri
        scale: Scaling factor applied to the mesh
        """

        filename: str = field(
            default="__default__",
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        uri: str = field(
            default="__default__",
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        scale: str = field(
            default="1 1 1",
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
                "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
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
                "required": True,
                "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
            },
        )
        size: str = field(
            default="1 1",
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
                "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+)((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
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
                "required": True,
            },
        )
        scale: float = field(
            default=1.0,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        threshold: int = field(
            default=200,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        height: float = field(
            default=1.0,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        granularity: int = field(
            default=1,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )

    @dataclass
    class Heightmap:
        """
        A heightmap based on a 2d grayscale image.

        Parameters
        ----------
        uri: URI to a grayscale image file
        size: The size of the heightmap in world units
        pos: A position offset.
        texture: The heightmap can contain multiple textures. The order
            of the texture matters. The first texture will appear at the
            lowest height, and the last texture at the highest height.
            Use blend to control the height thresholds and fade between
            textures.
        blend: The blend tag controls how two adjacent textures are
            mixed. The number of blend elements should equal one less
            than the number of textures.
        """

        uri: str = field(
            default="__default__",
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        size: str = field(
            default="1 1 1",
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
                "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
            },
        )
        pos: str = field(
            default="0 0 0",
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
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
                    "required": True,
                },
            )
            diffuse: str = field(
                default="__default__",
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            normal: str = field(
                default="__default__",
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
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
                    "required": True,
                },
            )
            fade_dist: float = field(
                default=0.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
