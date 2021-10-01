import warnings
from typing import DefaultDict, List, Dict, Any, Tuple, Union

from .base import ElementBase, FloatElement, IntegerElement, Pose, StringElement
from .frame import Frame
from .... import transform as tf
from ...transformations import FrustumProjection


class Camera(ElementBase):
    """A Camera Sensor.

    This element describes the parameters of a perspective camera system with
    optional lense, noise, and distortion effects. Contrary to common
    formulations the camera's direction of view is along the x-axis and the
    image plane runs parallel to the y-z-plane. If u and v describe the two axis
    of the of the image plane, then the u-axis runs along the negative y axis,
    and the v-axis runs along the negative z-axis. The origin of the image plane
    is along the top left corner of the viewing frustum.

    Parameters
    ----------
    name : str
        The name of the camera. Default: ``camera``

        .. versionadded:: SDFormat 1.3
    pose : Pose
        The camera's initial position (x,y,z) and orientation (roll, pitch, yaw).

        .. versionadded:: SDFormat 1.3
    horizontal_fov : Union[float, Camera.HorizontalFov]
        The viewing frustum's horizontal angle of view along the image's u-axis or world's y-axis.
        Default: ``1.047``.

        .. versionchanged:: SDFormat 1.2
            horizontal_fov is now a float instead of a class.
    image : Camera.Image
        Layout of the captured images (shape and color format).
    clip : Camera.Clip
        Near and Far clip plane of the camera.
    save : Camera.Save
        Configuration parameters related to saving rendered images.
    depth_camera : Camera.DepthCamera
        Configuration parameters related to the depth camera.
    noise : Camera.Noise
        Parameters for the noise model.

        .. versionadded:: SDFormat 1.4
    distortion : Camera.Distortion
        Parameters for the distortion model.

        .. versionadded:: SDFormat 1.5
    lense : Camera.Lense
        Parameters for the lense model.

        .. versionadded:: SDFormat 1.5
    visibility_mask: int
        Visibility mask of a camera. When (camera's visibility_mask & visual's
        visibility_flags) evaluates to non-zero, the visual will be visible to
        the camera.

        .. versionadded:: SDFormat 1.7
    sdf_version : str
        The SDFormat version to use when constructing this element.
    frames : List[Frame]
        A list of frames of reference in which poses may be expressed.

        .. deprecated:: SDFormat v1.7
            Use :attr:`Model.frame` instead.
        .. versionadded:: SDFormat v1.5

    Attributes
    ----------
    name : str
        See ``Parameters`` section.
    pose : Pose
        See ``Parameters`` section.
    horizontal_fov : Union[float, Camera.HorizontalFov]
        See ``Parameters`` section.
    image : Camera.Image
        See ``Parameters`` section.
    clip : Camera.Clip
        See ``Parameters`` section.
    save : Camera.Save
        See ``Parameters`` section.
    depth_camera : Camera.DepthCamera
        See ``Parameters`` section.
    noise : Camera.Noise
        See ``Parameters`` section.
    distortion : Camera.Distortion
        See ``Parameters`` section.
    lense : Camera.Lense
        See ``Parameters`` section.
    visibility_mask: int
        See ``Parameters`` section.


    Notes
    -----
    The frustum's vertical angle of view (along the v-axis / z-axis) chosen
    using ``horizontal_fov`` and the pixel dimension, i.e., the aspect ratio, of
    the image.

    """

    def __init__(
        self,
        *,
        name: str = "camera",
        pose: Pose = None,
        horizontal_fov: Union[float, "Camera.HorizontalFov"] = 1.047,
        image: "Camera.Image" = None,
        clip: "Camera.Clip" = None,
        save: "Camera.Save" = None,
        depth_camera: "Camera.DepthCamera" = None,
        noise: "Camera.Noise" = None,
        distortion: "Camera.Distortion" = None,
        lense: "Camera.Lense" = None,
        frames: List[Frame] = None,
        visibility_mask: int = 4294967295,
        sdf_version: str,
    ) -> None:
        warnings.warn("`Camera` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)

        self.name = name
        self.pose = Pose(sdf_version=sdf_version) if pose is None else pose
        if sdf_version == "1.0":
            self.horizontal_fov = (
                Camera.HorizontalFov(sdf_version=sdf_version)
                if horizontal_fov is None
                else horizontal_fov
            )
        else:
            self.horizontal_fov = horizontal_fov
        self.image = Camera.Image(sdf_version=sdf_version) if image is None else image
        self.clip = Camera.Clip(sdf_version=sdf_version) if clip is None else clip
        self.save = Camera.Save(sdf_version=sdf_version) if save is None else save
        self.depth_camera = (
            Camera.DepthCamera(sdf_version=sdf_version)
            if depth_camera is None
            else depth_camera
        )
        self.noise = Camera.Noise(sdf_version=sdf_version) if noise is None else noise
        self.distortion = (
            Camera.Distortion(sdf_version=sdf_version)
            if distortion is None
            else distortion
        )
        self.lense = Camera.Lense(sdf_version=sdf_version) if lense is None else lense
        self._frames = [] if frames is None else frames
        self.visibility_mask = visibility_mask

    @property
    def frames(self):
        warnings.warn(
            "`Sensor.frames` is deprecated since SDF v1.7."
            " Use `Model.frames` instead and set `Frame.attached_to` to the name of this link.",
            DeprecationWarning,
        )
        return self._frames

    @classmethod
    def from_specific(cls, specific: Any, *, version: str) -> "ElementBase":
        # camera_args = {"visibility_mask": specific.visibility_mask}

        default_args = {
            "name": StringElement,
            "pose": Pose,
            "image": Camera.Image,
            "clip": Camera.Clip,
            "save": Camera.Save,
            "depth_camera": Camera.DepthCamera,
            "noise": Camera.Noise,
            "distortion": Camera.Distortion,
            "lense": Camera.Lense,
            "visbility_mask": IntegerElement,
        }
        if version == "1.0":
            default_args["horizontal_fov"] = Camera.HorizontalFov
        else:
            default_args["horizontal_fov"] = FloatElement
        list_args = {"frame": ("frames", Frame)}
        standard_args = cls._prepare_standard_args(
            specific, default_args, list_args, version=version
        )

        return Camera(**standard_args, sdf_version=version)

    def declared_frames(self) -> Dict[str, tf.Frame]:
        declared_frames = {
            self.name: tf.Frame(3, name=self.name),
            "pixel_space": tf.Frame(2, name="pixel_space"),
        }

        for frame in self._frames:
            declared_frames.update(frame.declared_frames())

        return declared_frames

    def to_static_graph(
        self,
        declared_frames: Dict[str, tf.Frame],
        sensor_frame: str,
        *,
        seed: int = None,
        shape: Tuple,
        axis: int = -1,
    ) -> tf.Frame:
        self.pose.to_static_graph(
            declared_frames, sensor_frame + f"::{self.name}", shape=shape, axis=axis
        )

        if self.sdf_version == "1.0":
            hfov = self.horizontal_fov.angle
        else:
            hfov = self.horizontal_fov

        parent = declared_frames[sensor_frame + f"::{self.name}"]
        child = declared_frames[sensor_frame + "::pixel_space"]
        projection = FrustumProjection(hfov, (self.image.height, self.image.width))
        projection(parent, child)

        for frame in self._frames:
            frame.pose.to_static_graph(
                declared_frames,
                sensor_frame + f"::{frame.name}",
                shape=shape,
                axis=axis,
            )

        return declared_frames[sensor_frame + f"::{self.name}"]

    def to_dynamic_graph(
        self,
        declared_frames: Dict[str, tf.Frame],
        sensor_frame: str,
        *,
        seed: int = None,
        shape: Tuple,
        axis: int = -1,
        apply_state: bool = True,
        _scaffolding: Dict[str, tf.Frame],
    ) -> tf.Frame:
        parent_name = sensor_frame
        child_name = sensor_frame + f"::{self.name}"

        parent = declared_frames[parent_name]
        child = declared_frames[child_name]

        parent_static = _scaffolding[parent_name]
        child_static = _scaffolding[child_name]

        link = tf.CompundLink(parent_static.links_between(child_static))
        link(parent, child)

        if self.sdf_version == "1.0":
            hfov = self.horizontal_fov.angle
        else:
            hfov = self.horizontal_fov

        parent = declared_frames[sensor_frame + f"::{self.name}"]
        child = declared_frames[sensor_frame + "::pixel_space"]
        projection = FrustumProjection(hfov, (self.image.height, self.image.width))
        projection(parent, child)

        return declared_frames[sensor_frame + f"::{self.name}"]

    class HorizontalFov(ElementBase):
        def __init__(self, *, angle: float = 1.047, sdf_version: str) -> None:
            super().__init__(sdf_version=sdf_version)
            self.angle = angle

        @classmethod
        def from_specific(cls, specific: Any, *, version: str) -> "ElementBase":
            return Camera.HorizontalFov(angle=specific.angle, sdf_version=version)

    class Image(ElementBase):
        """Image shape and color format

        An image is a rectangular subset of a 2D plane measured in pixels.
        Coordinates on this plane are referred to using a two dimensional
        coordinate system with basis vectors u and v (the uv-plane).

        Parameters
        ----------
        width : int
            Number of pixels along the v-axis. Default: ``320``.
        height : int
            Number of pixels along the u-axis. Default: ``240``.
        format : str
            The data format of the color channel. This value determines the
            number of channels, their order, and their meaning. Possible values
            are: L8, L16, R_FLOAT16, R_FLOAT32, R8G8B8, B8G8R8, BAYER_RGGB8,
            BAYER_BGGR8, BAYER_GBRG8, BAYER_GRBG8. Default: ``R8G8B8``.

            .. versionadded:: SDFormat v1.7
                Formats: L16, R_FLOAT16, R_FLOAT32
        sdf_version : str
            The SDFormat version to use when constructing this element.

        Attributes
        ----------
        width : int
            See ``Parameters`` section.
        height : int
            See ``Parameters`` section.
        format : str
            See ``Parameters`` section.

        """

        def __init__(
            self,
            *,
            width: int = 320,
            height: int = 240,
            format: str = "R8G8B8",
            sdf_version: str,
        ) -> None:
            super().__init__(sdf_version=sdf_version)
            self.width = width
            self.height = height
            self.format = format

        @classmethod
        def from_specific(cls, specific: Any, *, version: str) -> "ElementBase":
            return Camera.Image(
                width=specific.width,
                height=specific.height,
                format=specific.format,
                sdf_version=version,
            )

    class Clip(ElementBase):
        """Near and Far Clipping distance.

        Parameters
        ----------
        near : float
            Near clip distance. Default: ``0.1``.
        far : float
            Far clip distance. Default: ``100``.
        sdf_version : str
            The SDFormat version to use when constructing this element.

        Attributes
        ----------
        near : float
            See ``Parameters`` section.
        far : float
            See ``Parameters`` section.

        """

        def __init__(
            self, *, near: float = 0.1, far: float = 100, sdf_version: str
        ) -> None:
            super().__init__(sdf_version=sdf_version)
            self.near = near
            self.far = far

        @classmethod
        def from_specific(cls, specific: Any, *, version: str) -> "ElementBase":
            return Camera.Clip(
                near=specific.near, far=specific.far, sdf_version=version
            )

    class Save(ElementBase):
        """Save/Export frames as images.

        Parameters
        ----------
        enabled : bool
            Enable export as images. Default: ``False``.
        path : str
            The path name which will hold the frame data. If path name is
            relative, then directory is relative to current working directory.
            Default: None
        sdf_version : str
            The SDFormat version to use when constructing this element.

        Attributes
        ----------
        enabled : bool
            See ``Parameters`` section.
        path : str
            See ``Parameters`` section.

        """

        def __init__(
            self, *, enabled: bool = False, path: str = None, sdf_version: str
        ) -> None:
            super().__init__(sdf_version=sdf_version)
            self.enabled = enabled
            self.path = path

        @classmethod
        def from_specific(cls, specific: Any, *, version: str) -> "ElementBase":
            return Camera.Save(
                enabled=specific.enabled, path=specific.path, sdf_version=version
            )

    class DepthCamera(ElementBase):
        """Depth Camera configuration

        Parameters
        ----------
        output : str
            The type of data to output. Default: ``depths``.
        clip: Camera.Clip
            Depth camera clipping distance.
        sdf_version : str
            The SDFormat version to use when constructing this element.

        Attributes
        ----------
        output : str
            See ``Parameters`` section.
        clip: Camera.Clip
            See ``Parameters`` section.

        """

        def __init__(
            self,
            *,
            output: str = "depths",
            clip: "Camera.Clip" = None,
            sdf_version: str,
        ) -> None:
            super().__init__(sdf_version=sdf_version)
            self.output = output
            self.clip = clip

        @classmethod
        def from_specific(cls, specific: Any, *, version: str) -> "ElementBase":
            args_with_default = {"clip": Camera.Clip}
            standard_args = cls._prepare_standard_args(
                specific, args_with_default, version=version
            )
            return Camera.DepthCamera(
                output=specific.output, **standard_args, sdf_version=version
            )

    class Noise(ElementBase):
        """The camera's noise model.

        Parameters
        ----------
        type : str
            The shape of the random noise distribution. Currently supported
            types are: "gaussian" (draw additive noise values independently for
            each pixel from a Gaussian distribution). Default: ``gaussian``.
        mean : float
            The distribution mean. Default: ``0``.
        stddev : float
            The distribution's standard deviation. Default: ``0``.
        sdf_version : str
            The SDFormat version to use when constructing this element.

        Attributes
        ----------
        type : str
            See ``Parameters`` section.
        mean : float
            See ``Parameters`` section.
        stddev : float
            See ``Parameters`` section.

        """

        def __init__(
            self,
            *,
            type: str = "gaussian",
            mean: float = 0,
            stddev: float = 0,
            sdf_version: str,
        ) -> None:
            super().__init__(sdf_version=sdf_version)
            self.type = type
            self.mean = (mean,)
            self.stddev = stddev

        @classmethod
        def from_specific(cls, specific: Any, *, version: str) -> "ElementBase":
            return Camera.Noise(
                type=specific.type,
                mean=specific.mean,
                stddev=specific.stddev,
                sdf_version=version,
            )

    class Distortion(ElementBase):
        """The camera's distortion model

        Lens distortion to be applied to camera images. See
        http://en.wikipedia.org/wiki/Distortion_(optics)#Software_correction

        Parameters
        ----------
        k1 : float
            The first radial distortion coefficient. Default: ``0``.
        k2 : float
            The second radial distortion coefficient. Default: ``0``.
        k3 : float
            The third radial distortion coefficient. Default: ``0``.
        p1 : float
            The first tangential distortion coefficient. Default: ``0``
        p2 : float
            The second tangential distortion coefficient. Default: ``0``.
        center : str
            The distortion center or principal point. Default: ``0.5, 0.5``.
        sdf_version : str
            The SDFormat version to use when constructing this element.

        Attributes
        ----------
        k1 : float
            See ``Parameters`` section.
        k2 : float
            See ``Parameters`` section.
        k3 : float
            See ``Parameters`` section.
        p1 : float
            See ``Parameters`` section.
        p2 : float
            See ``Parameters`` section.
        center : str
            See ``Parameters`` section.

        """

        def __init__(
            self,
            *,
            k1: float = 0,
            k2: float = 0,
            k3: float = 0,
            p1: float = 0,
            p2: float = 0,
            center: str = "0.5, 0.5",
            sdf_version: str,
        ) -> None:
            super().__init__(sdf_version=sdf_version)
            self.k1 = k1
            self.k2 = k2
            self.k3 = k3
            self.p1 = p1
            self.p2 = p2
            self.center = center

        @classmethod
        def from_specific(cls, specific: Any, *, version: str) -> "ElementBase":
            return Camera.Distortion(
                k1=specific.k1,
                k2=specific.k2,
                k3=specific.k3,
                p1=specific.p1,
                p2=specific.p2,
                center=specific.center,
                sdf_version=version,
            )

    class Lense(ElementBase):
        """A Camera's lense properties.

        Parameters
        ----------
        type : str
            Type of the lens mapping. Supported values are gnomonical,
            stereographic, equidistant, equisolid_angle, orthographic, custom.
            For gnomonical (perspective) projection, it is recommended to
            specify a horizontal_fov of less than or equal to 90°. Default:
            ``stereographic``.
        scale_to_hfov : bool
            If true the image will be scaled to fit horizontal FOV, otherwise it
            will be shown according to projection type parameters. Default:
            ``True``.
        custom_function : Camera.Lense.CustomFunction
            A custom lense map.
        cuttoff_angle : float
            Everything outside of the specified angle will be hidden. Default:
            ``.5707``.
        env_texture_size : int
            Resolution of the environment cube map used to draw the world.
            Default: ``56``.
        intrinsics : Camera.Lense.Intrinsics
            Parameters of a custom perspective matrix.
        sdf_version : str
            The SDFormat version to use when constructing this element.

        Attributes
        ----------
        type : str
            See ``Parameters`` section.
        scale_to_hfov : bool
            See ``Parameters`` section.
        custom_function : Camera.Lense.CustomFunction
            See ``Parameters`` section.
        cuttoff_angle : float
            See ``Parameters`` section.
        env_texture_size : int
            See ``Parameters`` section.
        intrinsics : Camera.Lense.Intrinsics
            See ``Parameters`` section.

        """

        def __init__(
            self,
            *,
            type: str = "stereographic",
            scale_to_hfov: bool = True,
            custom_function: "Camera.Lense.CustomFunction" = None,
            cuttoff_angle: float = 1.5707,
            env_texture_size: int = 256,
            intrinsics: "Camera.Lense.Intrinsics" = None,
            sdf_version: str,
        ) -> None:
            super().__init__(sdf_version=sdf_version)
            self.type = type
            self.scale_to_hfov = scale_to_hfov
            self.custom_function = (
                Camera.Lense.CustomFunction(sdf_version=sdf_version)
                if custom_function is None
                else custom_function
            )
            self.cuttoff_angle = cuttoff_angle
            self.env_texture_size = env_texture_size
            self.intrinsics = (
                Camera.Lense.Intrinsics(sdf_version=sdf_version)
                if intrinsics is None
                else intrinsics
            )

        @classmethod
        def from_specific(cls, specific: Any, *, version: str) -> "ElementBase":
            lense_args = {
                "type": specific.type,
                "scale_to_hfov": specific.scale_to_hfov,
                "custom_function": specific.custom_function,
                "cuttoff_angle": specific.cuttoff_angle,
                "env_texture_size": specific.env_texture_size,
            }
            args_with_default = {
                "custom_function": Camera.Lense.CustomFunction,
                "intrinsics": Camera.Lense.Intrinsics,
            }
            standard_args = cls._prepare_standard_args(
                specific, args_with_default, version=version
            )

            return Camera.Lense(**lense_args, **standard_args)

        class CustomFunction(ElementBase):
            """A custom lense map.

            Definition of custom mapping function in a form of
            r=c1*f*fun(theta/c2 + c3). See
            https://en.wikipedia.org/wiki/Fisheye_lens#Mapping_function

            Parameters
            ----------
            c1 : float
                Linear scaling constant. Default: ``1``.
            c2 : float
                Angle scaling constant. Default: ``1``.
            c3 : float
                Angle offset constant. Default: ``0``.
            f : float
                Focal length of the optical system. Note: It's not a focal
                length of the lens in a common sense! This value is ignored if
                'scale_to_fov' is set to true. Default: ``1``.
            fun : str
                The non-linear element to use. Possible values are 'sin', 'tan'
                and 'id'. Default: ``tan``.
            sdf_version : str
                The SDFormat version to use when constructing this element.

            Attributes
            ----------
            c1 : float
                See ``Parameters`` section.
            c2 : float
                See ``Parameters`` section.
            c3 : float
                See ``Parameters`` section.
            f : float
                See ``Parameters`` section.
            fun : str
                See ``Parameters`` section.

            """

            def __init__(
                self,
                *,
                c1: float = 1,
                c2: float = 1,
                c3: float = 0,
                f: float = 1,
                fun: str = "tan",
                sdf_version: str,
            ) -> None:
                super().__init__(sdf_version=sdf_version)
                self.c1 = (c1,)
                self.c2 = (c2,)
                self.c3 = (c3,)
                self.f = (f,)
                self.fun = fun

            @classmethod
            def from_specific(cls, specific: Any, *, version: str) -> "ElementBase":
                return Camera.Lense.CustomFunction(
                    c1=specific.c1,
                    c2=specific.c2,
                    c3=specific.c3,
                    f=specific.f,
                    fun=specific.fun,
                    sdf_version=version,
                )

        class Intrinsics(ElementBase):
            """Custom projection matrix.

            Camera intrinsic parameters for setting a custom perspective
            projection matrix (cannot be used with WideAngleCamera since this
            class uses image stitching from 6 different cameras for achieving a
            wide field of view). The focal lengths can be computed using
            focal_length_in_pixels = (image_width_in_pixels * 0.5) /
            tan(field_of_view_in_degrees * 0.5 * PI/180)

            Parameters
            ----------
            fx : float
                X focal length (in pixels, overrides horizontal_fov). Default: ``277``.
            fy : float
                Y focal length (in pixels, overrides horizontal_fov). Default: ``277``.
            cx : float
                X principal point (in pixels). Default: ``160``.
            cy : float
                Y principal point (in pixels). Default: ``120``.
            s : float
                XY axis skew. Default: ``0``.
            sdf_version : str
                The SDFormat version to use when constructing this element.

            Attributes
            ----------
            fx : float
                See ``Parameters`` section.
            fy : float
                See ``Parameters`` section.
            cx : float
                See ``Parameters`` section.
            cy : float
                See ``Parameters`` section.
            s : float
                See ``Parameters`` section.

            """

            def __init__(
                self,
                *,
                fx: float = 277,
                fy: float = 277,
                cx: float = 160,
                cy: float = 120,
                s: float = 0,
                sdf_version: str,
            ) -> None:
                super().__init__(sdf_version=sdf_version)
                self.fx = fx
                self.fy = fy
                self.cx = cx
                self.cy = cy
                self.s = s

            @classmethod
            def from_specific(cls, specific: Any, *, version: str) -> "ElementBase":
                return Camera.Intrinsics(
                    fx=specific.fx,
                    fy=specific.fy,
                    cx=specific.cx,
                    cy=specific.cy,
                    s=specific.s,
                    sdf_version=version,
                )
