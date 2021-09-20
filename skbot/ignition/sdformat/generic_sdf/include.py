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
    def from_specific(cls, include: Any, *, version: str) -> "Include":
        return Include(
            uri=include.uri,
            name=include.name,
            static=include.static,
            pose=Pose.from_specific(include.pose, version=version),
            plugins=[Plugin.from_specific(x, version=version) for x in include.plugin],
            placement_frame=include.placement_frame,
            sdf_version=version,
        )


    def resolve(
        self, *, priority: Tuple[str, str, str] = ("model", "actor", "light")
    ):
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
            collection:List = getattr(specific_sdf, el)
            if len(collection) > 0:
                break
        else:
            raise ParseError(f"No fragments found at  `{self.uri}`.")

        if el == "model":
            model = Model.from_specific(collection[0], version=specific_sdf.version)
            if self.name is not None:
                model.name = self.name
            if self.static is not None:
                model.static = self.static
            if self.pose is not None:
                model.pose = self.pose
            if self.placement_frame is not None:
                model.placement_frame=self.placement_frame,
            # model.plugins.extend(self.plugins)
            return model
        elif el == "actor":
            actor = Actor.from_specific(collection[0], version=specific_sdf.version)
            raise NotImplementedError()
        else:
            light = Light.from_specific(collection[0], version=specific_sdf.version)
            raise NotImplementedError()