from itertools import chain
from typing import List, Any, Dict, Tuple
import warnings
from itertools import chain


from .base import (
    BoolElement,
    ElementBase,
    NamedPoseBearing,
    PoseBearing,
    Pose,
    StringElement,
)
from .link import Link
from .include import Include
from .frame import Frame
from .joint import Joint
from .plugin import Plugin
from .gripper import Gripper
from .actor import Actor
from .light import Light
from ..exceptions import ParseError
from .... import transform as tf
from .origin import Origin


class Model(ElementBase):
    """A physical object in the simulation

    The model element defines a complete robot or any other physical object.
    This includes (but is not limited to) its appearance, collision,
    skeleton/kinematic chain.

    Parameters
    ----------
    name : str
        A unique name for the model. This name must not match another model in
        the world.
    canonical_link : str
        The name of the model's canonical link, to which the model's implicit
        coordinate frame is attached. If unset or set to an empty string,
        the first link element listed as a child of this model is chosen
        as the canonical link.

        .. versionadded:: SDFormat v1.7
    placement_frame : str
        The frame inside this model whose pose will be set by the pose element
        of the model. Defaults to  ``__model__`` (the implicit model frame).

        .. versionadded:: SDFormat v1.8
    static : bool
        If True (default), the model is immovable. Otherwise the model is
        simulated in the dynamics engine.
    self_collide : bool
        If True, all links in the model will collide with each other
        (except those connected by a joint). Can be overridden by the link or
        collision element self_collide property. Two links within a model will
        collide if link1.self_collide OR link2.self_collide. Links connected by
        a joint will never collide. The default is ``False``.

        .. versionadded:: SDFormat v1.5
    allow_auto_disable : bool
        Allows a model to auto-disable, which is means the physics engine can
        skip updating the model when the model is at rest. This parameter is
        only used by models with no joints.

        .. versionadded:: SDFormat v1.2
    frames : List[Frame]
        A list of frames of reference in which poses may be expressed.

        .. versionadded:: SDFormat v1.5
    pose : Pose
        The model's initial position (x,y,z) and orientation (roll, pitch, yaw).

        .. versionadded:: SDFormat v1.2
    links : List[Link]
        A list of links. Each link represents a rigid body with inertia,
        collision, and visual properties.

        .. versionchanged:: SDFormat v1.5
            A model may now have 0 links.
    joints : List[Joint]
        A list of joints. Each joint specifies a kinematic and/or dynamic
        constraints between two links.
    plugins : List[Plugin]
        A list of plugins used to customize the runtime behavior of the
        simulation.
    grippers: List[Gripper],
        A list of grippers.
    includes : List[Include]
        A list of references to other SDF files that contain :class:`Model`s to
        include as nested models.

        .. versionadded:: SDFormat v1.5
    models : List[Model]
        A list of models nested within this model.

        .. versionadded:: SDFormat v1.5
    enable_wind : bool
        If set to true, all links in the model will be affected by the wind. Can
        be overriden by the link wind property.

        .. versionadded:: SDFormat v1.6
    sdf_version : str
        The SDFormat version to use when constructing this element.
    origin : Origin
        The model's origin.

        .. deprecated:: SDFormat v1.2
            Use ``Model.pose`` instead.


    Attributes
    ----------
    name : str
        See ``Parameters`` section.
    canonical_link : str
        See ``Parameters`` section.
    placement_frame : str
        See ``Parameters`` section.
    static : bool
        See ``Parameters`` section.
    self_collide : bool
        See ``Parameters`` section.
    allow_auto_disable : bool
        See ``Parameters`` section.
    frames : List[Frame]
        See ``Parameters`` section.
    pose : Pose
        See ``Parameters`` section.
    links : List[Link]
        See ``Parameters`` section.
    joints : List[Joint]
        See ``Parameters`` section.
    plugins : List[Plugin]
        See ``Parameters`` section.
    grippers: List[Gripper],
        See ``Parameters`` section.
    includes : List[Include]
        See ``Parameters`` section.
    models : List[Model]
        See ``Parameters`` section.
    enable_wind : bool
        See ``Parameters`` section.

    """

    def __init__(
        self,
        *,
        name: str,
        canonical_link: str = None,
        placement_frame: str = "__model__",
        static: bool = False,
        self_collide: bool = False,
        allow_auto_disable: bool = True,
        frames: List[Frame] = None,
        pose: Pose = None,
        links: List[Link],
        joints: List[Joint],
        plugins: List[Plugin],
        grippers: List[Gripper],
        includes: List[Include] = None,
        models: List["Model"] = None,
        enable_wind: bool = False,
        sdf_version: str,
        origin: Origin = None,
    ) -> None:
        super().__init__(sdf_version=sdf_version)

        self.name = name

        if placement_frame == "":
            placement_frame = None
        if placement_frame is None:
            placement_frame = "__model__"
        self.placement_frame = placement_frame
        self.static = static
        self.self_collide = self_collide
        self.allow_auto_disable = allow_auto_disable
        self.frames = [] if frames is None else frames

        if origin is None:
            self._origin = Origin(sdf_version=sdf_version)
        elif sdf_version == "1.0":
            self._origin = origin
        else:
            warnings.warn("`origin` is deprecated. Use `Model.pose` instead.")
            self._origin = origin

        if len(links) == 0 and sdf_version in ["1.0", "1.2", "1.3", "1.4"]:
            raise ValueError("A `Model` must specify at least one `Link`.")
        else:
            self.links = links

        if sdf_version == "1.0":
            self.pose = self._origin.pose
        elif pose is None:
            self.pose = Pose(sdf_version=sdf_version)
        else:
            self.pose = pose
        self._origin.pose = self.pose

        self.joints = joints
        self.plugins = plugins
        self.grippers = grippers
        self.models = [] if models is None else models
        self.enable_wind = enable_wind

        for include in includes:
            fragment = include.resolve()
            if isinstance(fragment, Model):
                self.models.append(fragment)
            else:
                raise ValueError("`Model.include` can only be used to include models.")

        if canonical_link == "":
            canonical_link = None
        if self.static:
            self.canonical_link = "world"
        elif canonical_link is not None:
            self.canonical_link = canonical_link
        elif len(self.links) > 0:
            self.canonical_link = links[0].name
        elif len(self.models) > 0:
            model_name = self.models[0].name
            self.canonical_link = f"{model_name}"
        else:
            raise ValueError(
                "`Model` must specify `canonical_link` or have at least one `link`."
            )

        for el in chain(
            self.models,
            self.frames,
            self.links,
            self.joints
            # lights
        ):
            if el.pose.relative_to is None:
                el.pose.relative_to = "__model__"

        for frame in self.frames:
            if frame.attached_to is None:
                frame.attached_to = "__model__"

    @property
    def origin(self):
        warnings.warn(
            "`Model.origin` is deprecated since SDFormat v1.2. Use `Model.pose` instead."
        )
        return self._origin

    @classmethod
    def from_specific(cls, specific: Any, *, version: str) -> "Model":
        model_args = {"name": specific.name, "sdf_version": version}

        elements_with_default = {
            "canonical_link": StringElement,
            "placement_frame": StringElement,
            "static": BoolElement,
            "self_collide": BoolElement,
            "allow_auto_disable": BoolElement,
            "origin": Origin,
            "pose": Pose,
            "enable_wind": BoolElement,
        }
        list_elements = {
            "frame": ("frames", Frame),
            "link": ("links", Link),
            "joint": ("joints", Joint),
            "plugin": ("plugins", Plugin),
            "gripper": ("grippers", Gripper),
            "include": ("includes", Include),
            "model": ("models", Model),
        }

        standard_args = cls._prepare_standard_args(
            specific, elements_with_default, list_elements, version=version
        )
        model_args.update(standard_args)

        # if hasattr(specific, "placement_frame") and :
        #     model_args["placement_frame"]

        return Model(**model_args)

    def declared_frames(self) -> Dict[str, tf.Frame]:
        declared_frames = {"__model__": tf.Frame(3, name=self.name)}

        for el in chain(self.frames, self.links, self.joints):
            declared_frames.update(el.declared_frames())

        for model in self.models:
            model_frames = model.declared_frames()
            declared_frames[model.name] = model_frames["__model__"]
            for name, frame in model_frames.items():
                declared_frames[f"{model.name}::{name}"] = frame

        return declared_frames

    def to_static_graph(
        self,
        declared_frames: Dict[str, tf.Frame],
        *,
        seed: int = None,
        shape: Tuple,
        axis: int = -1,
    ) -> tf.Frame:
        for model in self.models:
            scope = {
                name.split("::", 1)[1]: frame
                for name, frame in declared_frames.items()
                if name.startswith(f"{model.name}::")
            }
            scope["world"] = declared_frames["world"]
            model.to_static_graph(scope, seed=seed, shape=shape, axis=axis)

        for model in self.models:
            link = model.pose.to_tf_link()
            parent_name = model.pose.relative_to
            child_name = f"{model.name}::{model.placement_frame}"

            parent = declared_frames[parent_name]
            child = declared_frames[child_name]
            link(child, parent)

        for el in chain(self.frames, self.links, self.joints):
            el.to_static_graph(declared_frames, seed=seed, shape=shape, axis=axis)
            el.pose.to_static_graph(declared_frames, el.name, shape=shape, axis=axis)

        return declared_frames["__model__"]

    def to_dynamic_graph(
        self,
        declared_frames: Dict[str, tf.Frame],
        *,
        seed: int = None,
        shape: Tuple[int] = ...,
        axis: int = -1,
        apply_state: bool = True,
        _scaffolding: Dict[str, tf.Frame],
    ) -> tf.Frame:
        for model in self.models:
            scaffold_scope = {
                name.split("::", 1)[1]: frame
                for name, frame in _scaffolding.items()
                if name.startswith(f"{model.name}::")
            }
            scaffold_scope["world"] = _scaffolding["world"]

            scope = {
                name.split("::", 1)[1]: frame
                for name, frame in declared_frames.items()
                if name.startswith(f"{model.name}::")
            }
            scope["world"] = declared_frames["world"]
            model.to_dynamic_graph(
                scope,
                seed=seed,
                shape=shape,
                axis=axis,
                apply_state=apply_state,
                _scaffolding=scaffold_scope,
            )

        if self.static:
            parent = declared_frames["world"]
            parent_static = _scaffolding["world"]
        else:
            parent = declared_frames[self.canonical_link]
            parent_static = _scaffolding[self.canonical_link]
        child = declared_frames["__model__"]
        child_static = _scaffolding["__model__"]
        tf.CompundLink(parent_static.links_between(child_static))(parent, child)

        for el in chain(self.frames, self.links, self.joints):
            el.to_dynamic_graph(
                declared_frames,
                seed=seed,
                shape=shape,
                axis=axis,
                apply_state=apply_state,
                _scaffolding=_scaffolding,
            )

        return declared_frames["__model__"]
