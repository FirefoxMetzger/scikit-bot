from dataclasses import dataclass, field
from typing import List

__NAMESPACE__ = "sdformat/heightmap_shape"


@dataclass
class HeightmapType:
    """
    Parameters
    ----------
    uri: URI to a grayscale image file
    size: The size of the heightmap in world units. When loading an
        image: "size" is used if present, otherwise defaults to 1x1x1.
        When loading a DEM: "size" is used if present, otherwise
        defaults to true size of DEM.
    pos: A position offset.
    texture: The heightmap can contain multiple textures. The order of
        the texture matters. The first texture will appear at the lowest
        height, and the last texture at the highest height. Use blend to
        control the height thresholds and fade between textures.
    blend: The blend tag controls how two adjacent textures are mixed.
        The number of blend elements should equal one less than the
        number of textures.
    use_terrain_paging: Set if the rendering engine will use terrain
        paging
    sampling: Samples per heightmap datum. For rasterized heightmaps,
        this indicates the number of samples to take per pixel. Using a
        lower value, e.g. 1, will generally improve the performance of
        the heightmap but lower the heightmap quality.
    """

    class Meta:
        name = "heightmapType"

    uri: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    size: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
            "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
        },
    )
    pos: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
            "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
        },
    )
    texture: List["HeightmapType.Texture"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    blend: List["HeightmapType.Blend"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    use_terrain_paging: List[bool] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    sampling: List[int] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )

    @dataclass
    class Texture:
        """
        Parameters
        ----------
        size: Size of the applied texture in meters.
        diffuse: Diffuse texture image filename
        normal: Normalmap texture image filename
        """

        size: List[float] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        diffuse: List[str] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        normal: List[str] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

    @dataclass
    class Blend:
        """
        Parameters
        ----------
        min_height: Min height of a blend layer
        fade_dist: Distance over which the blend occurs
        """

        min_height: List[float] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        fade_dist: List[float] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
