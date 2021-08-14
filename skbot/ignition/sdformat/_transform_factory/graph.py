from typing import Callable, Dict, Tuple, List, Any
from dataclasses import dataclass
from contextlib import contextmanager
import numpy as np
from scipy.spatial.transform import Rotation as ScipyRotation

from .... import transform as tf
from .. import sdformat


@dataclass
class PoseData:
    parent: str
    child: str
    pose: np.ndarray
    relative_to: str
    parent_frame: tf.Frame = None
    child_frame: tf.Frame = None
    relative_frame: tf.Frame = None
    link: tf.Link = None

@dataclass
class LinkData:
    parent: str
    child: str
    link: tf.Link
    parent_frame: tf.Frame = None
    child_frame: tf.Frame = None


class Scope:
    def __init__(self, name, implicit_frame, *, parent:"Scope"=None) -> None:
        self.nested_scopes: Dict[str,"Scope"] = dict()

        self.frames: Dict[str, tf.Frame] = dict()
        self.poses: List[PoseData] = list()
        self.links: List[LinkData] = list()

        self.declare_frame(implicit_frame)
        self.parent = parent

    def declare_frame(self, name:str) -> None:
        if name in self.frames.keys():
            raise IndexError("Frame already declared.")

        frame = tf.Frame(3, name=name)
        self.frames[name] = frame

    def declare_link(self, parent:str, child:str, link:tf.Link):
        self.links.append(LinkData(
            parent,
            child,
            link
        ))

    def declare_pose(self, parent:str, child:str, pose:np.ndarray, relative_to:str):
        self.poses.append(PoseData(
            parent,
            child,
            pose,
            relative_to
        ))

    def get(self, frame:str):
        """Find the frame from a (namespaced) SDFormat name"""

        if frame == "world":
            if self.parent is None:
                return self.frames[frame]
            else:
                return self.parent.get(frame)

        if "::" in frame:
            elements = frame.split("::")
            scope = elements.pop(0)
            frame = "::".join(elements)
            return self.nested_scopes[scope].get(frame)
        else:
            return self.frames[frame]

    def resolve_names(self):
        for el in self.links:
            el.parent_frame = self.get(el.parent)
            el.child_frame = self.get(el.child)

        for el in self.poses:
            el.parent_frame = self.get(el.parent)
            el.child_frame = self.get(el.child)
            el.relative_frame = self.get(el.relative_frame)

        for scope in self.nested_scopes.values():
            scope.resolve_names()

    def resolve_links(self):
        for el in self.links:
            el.link(el.parent_frame, el.child_frame)

        for scope in self.nested_scopes.values():
            scope.resolve_links()

    def resolve_poses(self):
        for scope in self.nested_scopes.values():
            scope.resolve_poses()

        for el in self.poses:
            offset = el.relative_frame.transform(el.pose[:3], el.parent_frame)
            translation = tf.Translation(offset)

            rot_matrix = list()
            for basis in np.eye(3):
                vec = el.relative_frame.transform(basis, el.parent_frame)
                rot_matrix.append(vec)
            rot_matrix = np.stack(rot_matrix, axis=1)
            rot_matrix -= offset[:, None]
            angles = ScipyRotation.from_matrix(rot_matrix).as_euler("xyz")
            
            if np.any(np.abs(angles) > 1e-12):
                rotation = tf.EulerRotation("xyz", angles)
                tf_pose = tf.CompundLink([rotation, translation])
            else:
                tf_pose = translation

            tf_pose(el.parent_frame, el.child_frame)



class Graph:
    def __init__(self) -> None:
        self.nodes: Dict[str, tf.Frame] = dict()
        self.edges: List[Tuple(str, str, tf.Link)] = list()
        self._scope: List[str] = list()
        self._root: List[str] = list()

        self.world_edges: List[Tuple(str, tf.Link)] = list()

        # Typically a SDF's model or world frame
        self.root_node: str = None

    @property
    def prefix(self):
        return "/".join(self._root + self._scope)

    def _abs_path(self, name: str) -> str:
        return "/".join(self._root + self._scope + [name])

    def add_node(self, path: str, frame: tf.Frame) -> str:
        """Adds a frame under the current scope"""

        path = self._abs_path(path)
        self.nodes[path] = frame
        return path

    def add_link(self, parent: str, child: str, link: tf.Link) -> None:
        """Connects two frames under the current root"""

        elements = child.split("/")
        child_path = "/".join(self._root + elements)

        parent_elements = parent.split("/")
        parent_path = "/".join(self._root + parent_elements)

        self.edges.append((parent_path, child_path, link))

    def _convert_sdf_path(self, sdf_name: str, use_scope=True):
        """Converts a SDF path into a transform path"""

        if sdf_name == "world":
            # special value, handle downstream
            return "world"

        elements = self._root

        if use_scope:
            elements = elements + self._scope

        if sdf_name is None:
            elements = elements + list()
        elif sdf_name == "":
            elements = elements + list()
        elif "::" in sdf_name:
            elements = elements + sdf_name.split("::")
        else:
            elements = elements + [sdf_name]

        return "/".join(elements)

    def add_sdf_element(
        self, frame: tf.Frame, link: tf.Link, *, relative_to: str = None
    ) -> str:
        """Adds a frame under the current scope and connects it

        The connection is either to the element at the current scope
        (relative_to == None) or relative to the current root.
        """

        path = self._abs_path(frame.name)
        self.nodes[path] = frame

        if relative_to == "world":
            self.world_edges.append((path, link))
            return path

        parent = self._convert_sdf_path(relative_to)
        self.edges.append((parent, path, link))

        return path

    def pose_to_transform(self, pose: Any) -> Tuple[tf.Link, str]:
        def _pose_to_numpy(pose: Any) -> np.ndarray:
            """Pose Value to Numpy Array"""
            pose_str: str
            if isinstance(pose, str):
                # fix binding/xsdata bug
                pose_str = "0 0 0 0 0 0"
            elif pose.value == "":
                # fix binding/xsdata bug
                pose_str = "0 0 0 0 0 0"
            else:
                pose_str = pose.value

            return np.array(pose_str.split(" "), dtype=float)

        if isinstance(pose, str):
            # fix binding/xsdata bug
            offset = _pose_to_numpy(pose)
            parent = None
        else:
            offset = _pose_to_numpy(pose.value)
            parent = pose.relative_to

        translation = tf.Translation(offset[:3])
        if np.any(offset[3:] != 0):
            rotation = tf.EulerRotation("xyz", offset[3:])
            tf_pose = tf.CompundLink([rotation, translation])
        else:
            tf_pose = translation

        return tf_pose, parent

    def add_pose(self, name: str, pose: Any) -> str:
        """Add a SDF //pose element to the graph"""

        tf_frame = tf.Frame(3, name=name)
        tf_link, parent = self.pose_to_transform(pose)
        path = self.add_sdf_element(tf_frame, tf_link, relative_to=parent)

        return path

    def connect_sdf(self, parent: str, child: str, link: tf.Link) -> None:
        """Connect nodes (relative to root)"""
        child_path = self._convert_sdf_path(child)
        parent_path = self._convert_sdf_path(parent)

        if parent_path == "world":
            self.world_edges.append((child_path, link))
            return

        self.edges.append((parent_path, child_path, link))

    @contextmanager
    def scope(self, name: str) -> None:
        """Declares a scope under the current root."""
        self._scope.append(name)
        yield
        self._scope.pop()

    @contextmanager
    def set_root(self) -> None:
        """Temporarily change root.

        This temporarily resets ``scope`` and instead prepends ``root`` to every
        path that is added to the graph. This is useful while parsing models or
        includes, as they represent the root element for any children, i.e., an
        element inside a nested model can not refer to a frame outside of it,
        while an outside element can refer to the frame of a nested model.

        If root is None it will be set to the current prefix
        """

        old_scope = self._scope
        old_root = self._root
        self._root = self._root + self._scope
        self._scope = list()

        yield

        self._scope = old_scope
        self._root = old_root

    def resolve(self, world_name=None) -> tf.Frame:
        """Connect frames with defined links"""

        for parent, child, link in self.edges:
            try:
                parent_frame = self.nodes[parent]
                child_frame = self.nodes[child]
            except KeyError:
                raise sdformat.ParseError(
                    f"Invalid SDF. Either '{parent}' or '{child}' does not exist."
                ) from None
            else:
                link(child_frame, parent_frame)

        if len(self.world_edges) == 0:
            return  # done

        if world_name is None:
            raise sdformat.ParseError(
                "Need explicit world frame to resolve edges connected to world."
            )

        world_frame = self.nodes[world_name]
        for child, link in self.world_edges:
            child_frame = self.nodes[child]
            link(child_frame, world_frame)

    def extend(self, other: "Graph") -> None:
        """Add the nodes of the other graph under the current scope.

        Parameters
        ----------
        other : Graph
            A (unresolved) graph that should be added to this Graph.

        """

        for path, frame in other.nodes.items():
            self.add_node(path, frame)

        for parent, child, link in other.edges:
            self.add_link(parent, child, link)

        for child, link in other.world_edges:
            self.world_edges.append((child, link))

    def rename_root(self, new_name:str):
        """Changes the name of the current root node into a new name"""
        
        old_name = self.root_node
        self.nodes[self.root_node].name = new_name
        self.root_node = new_name

        for path in [key for key in self.nodes.keys()]:
            frame = self.nodes.pop(path)
            path = path.replace(old_name, new_name, 1)
            self.nodes[path] = frame

        for idx in range(len(self.edges)):
            parent, child, link = self.edges[idx]
            parent = parent.replace(old_name, new_name, 1)
            child = child.replace(old_name, new_name, 1)
            self.edges[idx] = (parent, child, link)

        for idx in range(len(self.world_edges)):
            child, link = self.world_edges[idx]
            child = child.replace(old_name, new_name, 1)
            self.world_edges[idx] = (child, link)