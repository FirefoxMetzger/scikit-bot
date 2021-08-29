from typing import Dict, List, Union, Tuple
import numpy as np

from .... import transform as tf
from .. import sdformat


class SdfLink:
    """Base class for link factory."""

    def __init__(
        self, parent: Union[str, tf.Frame], child: Union[str, tf.Frame]
    ) -> None:
        self.parent: Union[str, tf.Frame] = parent
        self.child: Union[str, tf.Frame] = child

    def to_transform_link(self, scope: "Scope") -> tf.Link:
        raise NotImplementedError()


class ScaffoldPose(SdfLink):
    """Pose instance for constructing the pose scaffold."""

    def __init__(self, parent: str, child: Union[str, tf.Frame], pose: str) -> None:
        super().__init__(parent, child)
        self.pose = np.array(pose.split(), dtype=float)

    def to_transform_link(self, scope: "Scope") -> tf.Link:
        return tf.CompundLink(
            [tf.EulerRotation("xyz", self.pose[3:]), tf.Translation(self.pose[:3])]
        )


class Scope:
    """A scope within SDFormat.

    This class does most of the heavy lifting of sdformat.to_frame_graph. It
    collects frames that are (explicitly or implicitly) declared within a SDF
    scope and holds a scope's sub-scopes (if any).

    SDF positions objects using a <pose> element, which can be relative to
    another element or relative to the scope's implicit root frame. This class
    first collects all such definitions and uses them to construct a static
    graph referred to as scaffolding (self.build_scaffolding).

    Once the (static) position of all objects can be computed using the
    scaffolding this class then constructs a dynamic pose graph that reflects
    the actual dynamic links between frames (self.resolve_links). The root
    scope's dynamic frame graph is then returned by to_frame_graph.

    """

    def __init__(self, name, *, parent: "Scope" = None) -> None:
        self.nested_scopes: Dict[str, "Scope"] = dict()

        self.frames: Dict[str, tf.Frame] = dict()
        self.links: List[SdfLink] = list()

        self.scaffold_frames: Dict[str, tf.Frame] = dict()
        self.scaffold_links: List[ScaffoldPose] = list()

        # instantiated downstream
        self.default_frame: tf.Frame = None

        # might be able to remove this
        self.name = name

        self.parent = parent
        self.placement_frame: str = None

    def declare_frame(self, name: str) -> None:
        """Add a frame to the scaffolding and final frame graph.

        The declared frame can be found by dynamic links using the given name.

        """

        if name in self.frames.keys():
            raise sdformat.ParseError(f"Frame '{name}' already declared.")

        if name == "world":
            raise sdformat.ParseError(
                "Can not create a frame named 'world' (reserved name)."
            )

        self.frames[name] = tf.Frame(3, name=name)
        self.scaffold_frames[name] = tf.Frame(3, name=name)

    def add_scaffold(self, frame_name: str, pose: str, relative_to: str = None) -> None:
        """Add a pose to the scaffolding frame graph."""

        parent = self.default_frame.name
        if relative_to is not None and not relative_to == "":
            parent = relative_to

        self.scaffold_links.append(ScaffoldPose(parent, frame_name, pose))

    def declare_link(self, link: SdfLink) -> None:
        """Add a link to the final/dynamic frame graph."""
        self.links.append(link)

    def get(self, name: str, scaffolding: bool) -> tf.Frame:
        """Find the frame from a (namespaced) SDFormat name."""

        if "::" in name:
            scope, subscope_name = name.split("::", 1)

            try:
                frame = self.nested_scopes[scope].get(subscope_name, scaffolding)
            except sdformat.ParseError:
                raise sdformat.ParseError(
                    f"No frame named '{name}' in scope '{self.name}'"
                ) from None
        else:
            storage = self.frames
            if scaffolding:
                storage = self.scaffold_frames

            try:
                frame = storage[name]
            except KeyError:
                raise sdformat.ParseError(
                    f"No frame named '{name}' in scope '{self.name}'"
                ) from None

        return frame

    def build_scaffolding(self) -> None:
        """Construct the static frame graph.

        Connect declared scaffolding frames with declared scaffolding links.
        """
        for el in self.scaffold_links:
            tf_link = el.to_transform_link(self)

            parent = self.get(el.parent, scaffolding=True)

            child = el.child
            if isinstance(child, str):
                child = self.get(child, scaffolding=True)

            tf_link(parent, child)

        for scope in self.nested_scopes.values():
            scope.build_scaffolding()

    def resolve_links(self, *, shape: Tuple[int], axis: int) -> None:
        """Construct the dynamic frame graph.

        The success of this function depends on build_scaffolding. Links in the
        dynamic frame graph may have to be computed using the scaffolding and hence
        it needs to have been build prior to the execution of this function.

        """
        for el in self.links:
            if isinstance(el.parent, str):
                parent = self.get(el.parent, scaffolding=False)
            else:
                parent = el.parent

            if isinstance(el.child, str):
                child = self.get(el.child, scaffolding=False)
            else:
                child = el.child

            try:
                tf_link = el.to_transform_link(self, shape, axis)
            except RuntimeError:
                raise sdformat.ParseError(
                    f"Unable to express pose of '{child.name}' in frame '{parent.name}'."
                )
            tf_link(parent, child)

        for scope in self.nested_scopes.values():
            scope.resolve_links(shape=shape, axis=axis)

    def add_subscope(self, nested_scope: "Scope") -> None:
        """Add a scope nested within this scope."""

        if nested_scope.name in self.nested_scopes.keys():
            raise sdformat.ParseError(
                f"Nested Scope '{nested_scope.name}' already defined."
            )

        self.nested_scopes[nested_scope.name] = nested_scope
        nested_scope.parent = self


class ModelScope(Scope):
    """Specialization for scope declared by <model> elements."""

    def __init__(
        self,
        name,
        *,
        parent: "Scope" = None,
        placement_frame: str = None,
        canonical_link: str = None,
    ) -> None:
        super().__init__(name, parent=parent)

        self.placement_frame = placement_frame

        self.default_frame = tf.Frame(3, name="__model__")
        self.scaffold_frames["__model__"] = self.default_frame

        self.canonical_link = canonical_link

        self.pose = None

    def get(self, name: str, scaffolding: bool) -> tf.Frame:
        """Find the frame from a (namespaced) SDFormat name."""

        if name == "world":
            return self.parent.get(name, scaffolding)

        return super().get(name, scaffolding)


class WorldScope(Scope):
    """Specialization for scopes declared by <world> elements."""

    def __init__(self, name) -> None:
        super().__init__(name, parent=None)

        self.default_frame = tf.Frame(3, name="world")
        self.scaffold_frames["world"] = self.default_frame
        self.frames["world"] = tf.Frame(3, name=name)

    def get(self, name: str, scaffolding: bool) -> tf.Frame:
        """Find the frame from a (namespaced) SDFormat name"""

        if name == "world":
            if scaffolding:
                return self.default_frame
            else:
                return self.frames["world"]

        return super().get(name, scaffolding)


class LightScope(Scope):
    """Specialization for scopes declared by <light> elements."""

    def __init__(self, name) -> None:
        super().__init__(name, parent=None)

        self.default_frame = tf.Frame(3, name="__light__")
        self.scaffold_frames["__light__"] = self.default_frame
