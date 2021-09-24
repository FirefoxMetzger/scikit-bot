from typing import List, Any, Tuple, Union

from .base import ElementBase, Pose
from .plugin import Plugin
from ..exceptions import ParseError
from ... import fuel
from .. import sdformat


class Include(ElementBase):
    def __init__(
        self,
        *,
        uri: str,
        name: str = None,
        static: bool = None,
        pose: Pose = None,
        plugins: List["Plugin"] = None,
        placement_frame: str = None,
        sdf_version: str,
    ) -> None:
        super().__init__(sdf_version=sdf_version)
        self.uri = uri
        self.name = name
        self.static = static
        self.pose = pose
        self.plugins = [] if plugins is None else plugins
        self.placement_frame = placement_frame

        if self.placement_frame is not None:
            if self.pose is None:
                raise ParseError(
                    "`Include`s that specify `Include.placement_frame`"
                    " must also specify `Include.pose`."
                )

    @classmethod
    def from_specific(cls, specific: Any, *, version: str) -> "Include":
        include_args = {
            "uri": specific.uri,
            "static": specific.static,
            "pose": Pose.from_specific(specific.pose, version=version),
            "plugins": [Plugin.from_specific(x, version=version) for x in specific.plugin],
        }

        if version not in ["1.0", "1.2", "1.3", "1.4", "1.5", "1.6", "1.7"]:
            include_args["placement_frame"] = specific.placement_frame


        return Include(
            **include_args,
            sdf_version=version,
        )

    def resolve(self, *, priority: Tuple[str, str, str] = ("model", "actor", "light")):
        """Resolve the include.

        This function loads the included fragment as a generic :class:`Actor`,
        :class:`Model`, or :class:`Light`.

        Parameters
        ----------
        priority : str
            The order in which to check the included SDF for fragments. If
            multiple fragments are defined in the same SDF only the first
            fragment is returned. It is a 3-tuple with values `model`,
            `actor`, `light` in any order.

        Returns
        -------
        generic_sdf : Union["Model", "Light", "Actor"]
            The included fragment.

        """

        # avoid circular import while keeping resolve
        # as a method of include
        from .actor import Actor
        from .model import Model
        from .light import Light

        sdf_string = fuel.get_fuel_model(self.uri)
        specific_sdf = sdformat.loads(sdf_string)

        for el in priority:
            fragment = getattr(specific_sdf, el)

            if fragment is None:
                continue

            if isinstance(fragment, list):
                if len(fragment) == 0:
                    continue
                fragment = fragment[0]

            break
        else:
            raise ParseError(f"No fragments found at  `{self.uri}`.")

        if el == "model":
            model = Model.from_specific(fragment, version=specific_sdf.version)
            if self.name is not None:
                model.name = self.name
            if self.static is not None:
                model.static = self.static
            if self.pose is not None:
                model.pose = self.pose
            if self.placement_frame is not None:
                model.placement_frame = (self.placement_frame,)
            # model.plugins.extend(self.plugins)
            return model
        elif el == "actor":
            actor = Actor.from_specific(fragment, version=specific_sdf.version)
            raise NotImplementedError()
        else:
            light = Light.from_specific(fragment, version=specific_sdf.version)
            raise NotImplementedError()
