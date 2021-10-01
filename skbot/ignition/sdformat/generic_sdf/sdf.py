"""<element name="sdf" required="1">
  <description>SDFormat base element that can include one model, actor, light, or worlds. A user of multiple worlds could run parallel instances of simulation, or offer selection of a world at runtime.</description>

  <attribute name="version" type="string" default="1.8" required="1">
    <description>Version number of the SDFormat specification.</description>
  </attribute>

  <include filename="world.sdf" required="*"/>
  <include filename="model.sdf" required="0"/>
  <include filename="actor.sdf" required="0"/>
  <include filename="light.sdf" required="0"/>

</element> <!-- End SDF -->"""

from typing import List, Union, Dict, Any, Tuple
import warnings

from .base import ElementBase
from .world import World
from .actor import Actor
from .model import Model
from .light import Light
from ..exceptions import ParseError
from .... import transform as tf


class Sdf(ElementBase):
    """SDFormat Root Element

    This element is a container for multiple simulation worlds (can be one) or
    for a single fragment of a world (Model, Actor, Light).

    Parameters
    ----------
    payload : Union[List[World], Model, Light, Actor]
        The element contained in this SDF. This can be one :class:`Model`, one :class`Actor`, one
        :class:`Light`, or a list of :class`Worlds`.
    version : str
        The SDFormat version.
    worlds : List[World]
        .. deprecated:: SDFormat v1.8
            Worlds, models, lights, and/or actors can no longer be combined. Use
            `payload` instead.
        The worlds contained in this SDF.
    models : List[Model]
        .. deprecated:: SDFormat v1.8
            Starting with SDFormat v1.8 only a single model is supported. Use the
            `model` kwarg instead.

        The models contained in this SDF.
    lights : List[Light]
        .. deprecated:: SDFormat v1.8
            Starting with SDFormat v1.8 only a single light is supported. Use the
            `light` kwarg instead.

        The lights contained in this SDF.
    actors : List[Actor]
        .. deprecated:: SDFormat v1.8
            Starting with SDFormat v1.8 only a single actor is supported. Use the
            `actor` kwarg instead.

        The actors contained in this SDF.

    Attributes
    ----------
    worlds : List[World]
        The worlds contained in the SDF file.
    model: Model
        The model contained in the SDF file.
    light: Light
        The light contained in the SDF file.
    actor: Actor
        The actor contained in the SDF file.
    version : str
        The SDFormat version.
    models : List[Model]
        .. deprecated:: SDFormat v1.8
            Use the `Sdf.model` instead.
    lights : List[Light]
        .. deprecated:: SDFormat v1.8
            Use the `Sdf.light` instead.
    actors : List[Actor]
        .. deprecated:: SDFormat v1.8
            Use the `Sdf.actor` instead.

    """

    def __init__(
        self,
        *,
        payload: Union[List[World], Model, Light, Actor] = None,
        version: str = "1.8",
        worlds: List[World] = None,
        models: List[Model] = None,
        lights: List[Light] = None,
        actors: List[Actor] = None,
    ) -> None:
        super().__init__(sdf_version=version)
        self.version = version
        self.worlds: List[World] = []
        self._actors: List[Actor] = []
        self._models: List[Model] = []
        self._lights: List[Light] = []

        if self.sdf_version == "1.8":
            if isinstance(payload, list) and all(
                [isinstance(x, World) for x in payload]
            ):
                self.worlds = payload
            elif isinstance(payload, Actor):
                self._actors.append(payload)
            elif isinstance(payload, Model):
                self._models.append(payload)
            elif isinstance(payload, Light):
                self._lights.append(payload)
            else:
                raise ParseError("Invalid `Sdf` element.")
        elif version in ["1.7", "1.6", "1.5", "1.4", "1.3"]:
            self.worlds.extend(worlds)
            self._models.extend(models)
            self._lights.extend(lights)
            self._actors.extend(actors)
        else:
            raise ParseError("`Sdf` does not exist prior to SDFormat v1.3.")

        for model in self._models:
            if model.pose.relative_to is None:
                model.pose.relative_to = "world"

    @property
    def actor(self) -> Actor:
        try:
            return self._actors[0]
        except IndexError:
            return None

    @property
    def model(self) -> Model:
        try:
            return self._models[0]
        except IndexError:
            return None

    @property
    def light(self) -> Light:
        try:
            return self._lights[0]
        except IndexError:
            return None

    # deprecated properties
    @property
    def actors(self) -> List[Actor]:
        warnings.warn(
            "`sdf.actors` is deprecated since SDFormat v1.8. Use `sdf.actor` instead.",
            DeprecationWarning,
        )
        return self._actors

    @property
    def models(self) -> List[Model]:
        warnings.warn(
            "`sdf.models` is deprecated since SDFormat v1.8. Use `sdf.models` instead.",
            DeprecationWarning,
        )
        return self._models

    @property
    def lights(self) -> List[Light]:
        warnings.warn(
            "`sdf.lights` is deprecated since SDFormat v1.8. Use `sdf.lights` instead.",
            DeprecationWarning,
        )
        return self._lights

    @classmethod
    def from_specific(cls, sdf: Any, *, version: str) -> "Sdf":
        """Create a generic Sdf object from a specific one.

        Parameters
        ----------
        sdf : Any
            The SDF object that should be turned into a generic object. It
            can come from any version of the specific SDFormat bindings
            provided by scikit-bot.
        version : str
            The version of the given SDF element.

        Returns
        -------
        generic_sdf : Sdf
            The generic equivalent of the provided specific Sdf object.
        """

        if version == "1.8":
            payload: Union[List[World], Model, Light, Actor]
            if sdf.world is not None and len(sdf.world) > 0:
                payload = [World.from_specific(x, version=version) for x in sdf.world]
            elif sdf.actor is not None:
                payload = Actor.from_specific(sdf.actor, version=version)
            elif sdf.model is not None:
                payload = Model.from_specific(sdf.model, version=version)
            elif sdf.light is not None:
                payload = Light.from_specific(sdf.light, version=version)
            else:
                raise ParseError("Can not convert `sdf` element without payload.")

            return Sdf(payload=payload, version=version)
        else:
            return Sdf(
                worlds=[World.from_specific(x, version=version) for x in sdf.world],
                actors=[Actor.from_specific(x, version=version) for x in sdf.actor],
                models=[Model.from_specific(x, version=version) for x in sdf.model],
                lights=[Light.from_specific(x, version=version) for x in sdf.light],
                version=version,
            )

    def declared_frames(
        self,
    ) -> Dict[str, Union[List[Dict[str, tf.Frame]], Dict[str, tf.Frame]]]:
        declared_frames = {
            "worlds": [x.declared_frames() for x in self.worlds],
            "models": [x.declared_frames() for x in self._models],
        }

        if self.model is not None:
            declared_frames["model"] = declared_frames["models"][0]

        return declared_frames

    def to_static_graph(
        self,
        declared_frames: Dict[str, List[tf.Frame]],
        *,
        seed: int = None,
        shape: Tuple[int] = (3,),
        axis: int = -1,
    ) -> Dict[str, List[tf.Frame]]:
        graphs = {
            "worlds": list(),
            "models": list(),
        }

        for idx, world in enumerate(self.worlds):
            try:
                static_frames = declared_frames["worlds"][idx]
            except IndexError:
                break

            root = world.to_static_graph(
                static_frames, seed=seed, shape=shape, axis=axis
            )
            graphs["worlds"].append(root)

        for idx, model in enumerate(self._models):
            try:
                static_frames = declared_frames["models"][idx]
            except IndexError:
                break

            if "world" not in static_frames:
                static_frames["world"] = tf.Frame(3, name="world")

            root = model.to_static_graph(
                static_frames, seed=seed, shape=shape, axis=axis
            )
            graphs["models"].append(root)

            model.pose.to_static_graph(
                static_frames, "__model__", shape=shape, axis=axis
            )

        return graphs

    def to_dynamic_graph(
        self,
        declared_frames: Dict[str, List[tf.Frame]],
        *,
        seed: int = None,
        shape: Tuple[int] = (3,),
        axis: int = -1,
        apply_state: bool = True,
    ) -> Dict[str, List[tf.Frame]]:
        graphs = {
            "worlds": list(),
            "models": list(),
        }
        scaffold = self.declared_frames()
        self.to_static_graph(scaffold, seed=seed, shape=shape, axis=axis)

        for idx, world in enumerate(self.worlds):
            try:
                frames = declared_frames["worlds"][idx]
            except IndexError:
                break

            root = world.to_dynamic_graph(frames, seed=seed, shape=shape, axis=axis)
            graphs["worlds"].append(root)

        for idx, model in enumerate(self._models):
            try:
                frames = declared_frames["models"][idx]
            except IndexError:
                break

            static_frames = scaffold["models"][idx]

            if "world" not in frames:
                frames["world"] = tf.Frame(3, name="world")

            root = model.to_dynamic_graph(
                frames, seed=seed, shape=shape, axis=axis, _scaffolding=static_frames
            )
            graphs["models"].append(root)

        return graphs
