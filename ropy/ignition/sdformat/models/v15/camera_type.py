from dataclasses import dataclass, field
from typing import List, Optional
from .frame_type import FrameType
from .pose_type import PoseType

__NAMESPACE__ = "sdformat/camera"


@dataclass
class CameraType:
    """
    Parameters
    ----------
    horizontal_fov: Horizontal field of view
    image: The image size in pixels and format.
    clip: The near and far clip planes. Objects closer or farther than
        these planes are not rendered.
    save: Enable or disable saving of camera frames.
    depth_camera: Depth camera parameters
    noise: The properties of the noise model that should be applied to
        generated images
    distortion: Lens distortion to be applied to camera images. See
        http://en.wikipedia.org/wiki/Distortion_(optics)#Software_correction
    lens: Lens projection description
    frame: A frame of reference to which a pose is relative.
    pose: A position(x,y,z) and orientation(roll, pitch yaw) with
        respect to the specified frame.
    name: An optional name for the camera.
    """
    class Meta:
        name = "cameraType"

    horizontal_fov: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    image: List["CameraType.Image"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    clip: List["CameraType.Clip"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    save: List["CameraType.Save"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    depth_camera: List["CameraType.DepthCamera"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    noise: List["CameraType.Noise"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    distortion: List["CameraType.Distortion"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    lens: List["CameraType.Lens"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    frame: List[FrameType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    pose: List[PoseType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    name: str = field(
        default="__default__",
        metadata={
            "type": "Attribute",
        }
    )

    @dataclass
    class Image:
        """
        Parameters
        ----------
        width: Width in pixels
        height: Height in pixels
        format:
            (L8|R8G8B8|B8G8R8|BAYER_RGGB8|BAYER_BGGR8|BAYER_GBRG8|BAYER_GRBG8)
        """
        width: List[int] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        height: List[int] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        format: List[str] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )

    @dataclass
    class Clip:
        """
        Parameters
        ----------
        near: Near clipping plane
        far: Far clipping plane
        """
        near: List[float] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        far: List[float] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )

    @dataclass
    class Save:
        """
        Parameters
        ----------
        path: The path name which will hold the frame data. If path name
            is relative, then directory is relative to current working
            directory.
        enabled: True = saving enabled
        """
        path: List[str] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        enabled: Optional[bool] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
            }
        )

    @dataclass
    class DepthCamera:
        """
        Parameters
        ----------
        output: Type of output
        """
        output: List[str] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )

    @dataclass
    class Noise:
        """
        Parameters
        ----------
        type: The type of noise.  Currently supported types are:
            "gaussian" (draw additive noise values independently for
            each pixel from a Gaussian distribution).
        mean: For type "gaussian," the mean of the Gaussian distribution
            from which noise values are drawn.
        stddev: For type "gaussian," the standard deviation of the
            Gaussian distribution from which noise values are drawn.
        """
        type: List[str] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        mean: List[float] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        stddev: List[float] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )

    @dataclass
    class Distortion:
        """
        Parameters
        ----------
        k1: The radial distortion coefficient k1
        k2: The radial distortion coefficient k2
        k3: The radial distortion coefficient k3
        p1: The tangential distortion coefficient p1
        p2: The tangential distortion coefficient p2
        center: The distortion center or principal point
        """
        k1: List[float] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        k2: List[float] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        k3: List[float] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        p1: List[float] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        p2: List[float] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        center: List[str] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
                "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+)((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
            }
        )

    @dataclass
    class Lens:
        """
        Parameters
        ----------
        type: Type of the lens mapping. Supported values are gnomonical,
            stereographic, equidistant, equisolid_angle, orthographic,
            custom. For gnomonical (perspective) projection, it is
            recommended to specify a horizontal_fov of less than or
            equal to 90°
        scale_to_hfov: If true the image will be scaled to fit
            horizontal FOV, otherwise it will be shown according to
            projection type parameters
        custom_function: Definition of custom mapping function in a form
            of r=c1*f*fun(theta/c2 + c3). See
            https://en.wikipedia.org/wiki/Fisheye_lens#Mapping_function
        cutoff_angle: Everything outside of the specified angle will be
            hidden, 90° by default
        env_texture_size: Resolution of the environment cube map used to
            draw the world
        """
        type: List[str] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        scale_to_hfov: List[bool] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        custom_function: List["CameraType.Lens.CustomFunction"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        cutoff_angle: List[float] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        env_texture_size: List[int] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )

        @dataclass
        class CustomFunction:
            """
            Parameters
            ----------
            c1: Linear scaling constant
            c2: Angle scaling constant
            c3: Angle offset constant
            f: Focal length of the optical system. Note: It's not a
                focal length of the lens in a common sense! This value
                is ignored if 'scale_to_fov' is set to true
            fun: Possible values are 'sin', 'tan' and 'id'
            """
            c1: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            c2: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            c3: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            f: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            fun: List[str] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
