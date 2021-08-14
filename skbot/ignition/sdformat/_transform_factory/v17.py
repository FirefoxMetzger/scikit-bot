import numpy as np
from urllib.parse import urlparse
from typing import List, Union
from pathlib import Path

from .graph import Graph
from .factory import graph_factory
from .. import sdformat
from ..bindings import v17
from ...fuel import get_fuel_model
from .... import transform as tf


IncludeElement = Union[v17.ModelModel.Include, v17.World.Include]
PoseOnlyElement = Union[
    v17.Collision,
    v17.Visual
]


def resolve_include(
    include: IncludeElement, graph: Graph, *, root_uri: str = None
) -> Graph:
    """"""

    # there is only one fuel server
    fuel_server = "fuel.ignitionrobotics.org"

    uri_parts = urlparse(include.uri)
    if uri_parts.scheme == "https" and uri_parts.netloc == fuel_server:
        sdf = get_fuel_model(include.uri)
    elif uri_parts.scheme == "model" and uri_parts.netloc == fuel_server:
        raise NotImplementedError("Unsure how to resolve model://.")
    elif uri_parts.scheme == "":
        if root_uri is None:
            raise sdformat.ParseError("Can't resolve relative include without root_uri.")
        root_parts = urlparse(root_uri)
        if root_parts.scheme == "https" and root_parts.netloc == fuel_server:
            sdf = get_fuel_model(root_uri, file_path=include.uri)
        else:
            sdf = (Path(root_uri) / include.uri).read_text()
    else:
        raise sdformat.ParseError(f"Failed to include: {include.uri}")

    subgraph = graph_factory(sdf)
    if include.name is not None:
        model_name = include.name
        subgraph.rename_root(include.name)
    else:
        model_name = subgraph.root_node
    graph.extend(subgraph)

    if include.placement_frame is not None:
        child_frame = model_name + "/" + include.placement_frame
    else:
        child_frame = subgraph.root_node

    tf_link, parent = graph.pose_to_transform(include.pose)
    graph.connect_sdf(parent, child_frame, tf_link)

    return graph


def convert_world(world: v17.World, root_uri: str = None) -> Graph:
    graph = Graph()
    graph.add_node(world.name, tf.Frame(3, name=world.name))
    with graph.scope(world.name), graph.set_root():
        for include in world.include:
            resolve_include(include, graph, root_uri=root_uri)

        # TODO: GUI
        # TODO: scene

        for light in world.light:
            subgraph = convert_light(light)
            graph.extend(subgraph)

        for frame in world.frame:
            graph.add_pose(frame.name, frame.pose)

        for model in world.model:
            convert_model(model, graph=graph)

        # TODO: actor
        # TODO: road
        # TODO: spherical coords
        # TODO: state
        # TODO: population

    return graph
    # # convert population
    # for population in world.population:
    #     tf_frame = tf.Frame(3, name=population.name)
    #     offset = _pose_to_numpy(population.pose.value)
    #     tf_link = tf.Translation(offset)

    #     if population.pose.relative_to is not None:
    #         parent = population.pose.relative_to
    #         unresolved_poses.append((parent, tf_frame, tf_link))
    #     else:
    #         tf_link(tf_frame, world_frame)

    #     num_defined = 0
    #     if population.box is not None:
    #         num_defined += 1
    #     if population.cylinder is not None:
    #         num_defined += 1
    #     num_defined += len(population.model)

    #     if len(population.model) > 1:
    #         raise NotImplementedError("Multiple models defined for population..")
    #     elif num_defined == 0:
    #         raise sdformat.ParseError("No models defined for population.")

    #     if population.box:
    #         model_gen = lambda: tf.Frame(3)
    #     elif population.cylinder:
    #         model_gen = lambda: tf.Frame(3)
    #     else:
    #         model_gen = lambda: _convert_model(population.model[0])

    #     step = np.array(population.distribution.step.split(" "), dtype=float)
    #     rows = np.arange(population.distribution.rows)[:, -1, -1]
    #     cols = np.array(population.distribution.cols)[-1, :, -1]

    #     dist_kind = population.distribution.type
    #     if dist_kind == "random":
    #         for _ in range(population.model_count):
    #             tf_frame = model_gen()
    #             # TODO: randomize me
    #             tf_link = tf.Translation((0, 0, 0))
    #             tf_link(tf_frame, world_frame)
    #     elif dist_kind == "uniform":
    #         pass
    #     elif dist_kind == "grid":
    #         row_step, col_step, _ = [
    #             float(x) for x in population.distribution.step.split(" ")
    #         ]
    #         for row in range(population.distribution.rows):
    #             row_pos = row_step * row
    #             for col in range(population.distribution.cols):
    #                 col_pos = col_step * col
    #                 tf_frame = model_gen()
    #                 tf_frame.name = tf_frame.name + f"_clone_{col*population.distribution.rows + row}"
    #                 tf_link = tf.Translation((row_pos, col_pos, 0))
    #     elif dist_kind == "linear-x":
    #         raise NotImplementedError("Linear placement not implemented yet.")
    #     elif dist_kind == "linear-y":
    #         raise NotImplementedError("Linear placement not implemented yet.")
    #     elif dist_kind == "linear-z":
    #         raise NotImplementedError("Linear placement not implemented yet.")

    #     for model_idx in range(population.model_count):
    #         pass

def convert_state(state: v17.State) -> Graph:
    raise NotImplementedError()

def convert_light(light: v17.Light, *, graph: Graph = None) -> Graph:
    if graph is None:
        graph = Graph()

    raise NotImplementedError()

def convert_actor() -> Graph:
    raise NotImplementedError()

def convert_model(model: v17.ModelModel, *, graph: Graph = None, root_uri: str = None) -> Graph:
    if graph is None:
        graph = Graph()
        graph.add_node(model.name, tf.Frame(3, name=model.name))
    else:
        graph.add_pose(model.name, model.pose)

    with graph.scope(model.name), graph.set_root():
        for include in model.include:
            resolve_include(include, graph, root_uri=root_uri)

        for nested_model in model.model:
            convert_model(nested_model, graph=graph)

        for frame in model.frame:
            graph.add_pose(frame.name, frame.pose)

        for link in model.link:
            convert_link(link, graph)

        for joint in model.joint:
            convert_joint(joint, graph)

        for gripper in model.gripper:
            raise NotImplementedError(
                "Gripper not implemented yet (lacking upstream docs)."
            )

    return graph

def convert_link(link: v17.Link, graph: Graph) -> Graph:
    if link.must_be_base_link:
        link.pose.relative_to = "world"

    graph.add_pose(link.name, link.pose)

    with graph.scope(link.name):
        if link.inertial:
            graph.add_pose("inertial", link.inertial.pose)

        for collision in link.collision:
            convert_pose_only(collision, graph)

        for visual in link.visual:
            convert_pose_only(visual, graph)

        for sensor in link.sensor:
            convert_sensor(sensor, graph)

        if link.projector:
            graph.add_pose(link.projector.name, link.projector.pose)
            # TODO: there might be a link into the projected frame missing
            # here I don't exactly know how projector works and didn't find
            # docs

        for idx, source in enumerate(link.audio_source):
            graph.add_pose(f"audio_source_{idx}", source.pose)
            if source.contact is not None:
                with graph.scope(f"audio_source_{idx}"):
                    for collision in source.contact.collision:
                        raise NotImplementedError()

        for light in link.light:
            convert_light(light, graph=graph)

    return graph

def convert_sensor(sensor: v17.Sensor, graph: Graph) -> Graph:
    graph.add_pose(sensor.name, sensor.pose)

    with graph.scope(sensor.name):
        if sensor.type == "air_pressure":
            raise NotImplementedError()
        elif sensor.type == "alimeter":
            raise NotImplementedError()
        elif sensor.type == "camera":
            if sensor.camera.noise is not None:
                raise NotImplementedError()
            if sensor.camera.distortion is not None:
                raise NotImplementedError()
            if sensor.camera.lense is not None:
                raise NotImplementedError()

            graph.add_pose(sensor.camera.name, sensor.camera.pose)
            with graph.scope(sensor.camera.name):
                graph.add_sdf_element(
                    tf.Frame(2, name="pixel_space"),
                    tf.FrustumProjection(
                        sensor.camera.horizontal_fov,
                        (sensor.camera.image.height, sensor.camera.image.width),
                    ),
                )
        elif sensor.type == "contact":
            raise NotImplementedError()
        elif sensor.type == "depth_camera":
            raise NotImplementedError()
        elif sensor.type == "force_torque":
            raise NotImplementedError()
        elif sensor.type == "gps":
            raise NotImplementedError()
        elif sensor.type == "gpu_lidar":
            raise NotImplementedError()
        elif sensor.type == "gpu_ray":
            raise NotImplementedError()
        elif sensor.type == "imu":
            raise NotImplementedError()
        elif sensor.type == "lidar":
            raise NotImplementedError()
        elif sensor.type == "logica_camera":
            raise NotImplementedError()
        elif sensor.type == "magnetometer":
            raise NotImplementedError()
        elif sensor.type == "multicamera":
            raise NotImplementedError()
        elif sensor.type == "rfid":
            raise NotImplementedError()
        elif sensor.type == "rfidtag":
            raise NotImplementedError()
        elif sensor.type == "rgbd_camera":
            raise NotImplementedError()
        elif sensor.type == "sonar":
            raise NotImplementedError()
        elif sensor.type == "thermal_camera":
            raise NotImplementedError()
        elif sensor.type == "wireless_receiver":
            raise NotImplementedError()
        elif sensor.type == "wireless_transmitter":
            raise NotImplementedError()
        else:
            raise sdformat.ParseError(f"Unkown sensor type: {sensor.type}")

    return graph

def convert_joint(joint: v17.Joint, graph: Graph) -> Graph:
    if isinstance(joint.pose, str):
        # xsData bug
        joint.pose = v17.Joint.Pose(joint.pose)
    joint.pose.relative_to = joint.child
    graph.add_pose(joint.name, joint.pose)

    if joint.type == "revolute":
        normal = np.array(joint.axis.xyz.value.split(" "), dtype=float)
        if joint.axis.xyz.expressed_in is not None:
            raise NotImplementedError()
        tf_link = tf.RotvecRotation(normal)
        graph.connect_sdf(joint.parent, joint.name, tf_link)
    elif joint.type == "hinge":
        raise NotImplementedError("Hinge joints have not been added yet.")
    elif joint.type == "gearbox":
        raise NotImplementedError("Gearbox joints have not been added yet.")
    elif joint.type == "revolute2":
        raise NotImplementedError("Revolute2 type joint is not added yet.")
    elif joint.type == "prismatic":
        direction = np.array(joint.axis.xyz.value.split(" "), dtype=float)
        if joint.axis.xyz.expressed_in is not None:
            raise NotImplementedError()
        tf_link = tf.Translation(direction)
        graph.connect_sdf(joint.parent, joint.name, tf_link)
    elif joint.type == "ball":
        raise NotImplementedError("Ball joints have not been added yet.")
    elif joint.type == "screw":
        raise NotImplementedError("Screw joints have not been added yet.")
    elif joint.type == "universal":
        raise NotImplementedError("Universal joints have not been added yet.")
    elif joint.type == "fixed":
        tf_link = tf.Translation((0, 0, 0))
        graph.connect_sdf(joint.parent, joint.name, tf_link)

    for sensor in joint.sensor:
        convert_sensor(sensor, graph)

    return graph

def convert_pose_only(element: PoseOnlyElement, graph: Graph) -> Graph:
    graph.add_pose(element.name, element.pose)
    return graph


def converter(sdf: str, *, unwrap=True, root_uri: str = None) -> Graph:
    """Turn v1.8 SDF into a frame graph

    Parameters
    ----------
    sdf_in : Sdf
        A :class:`skbot.ignition.sdformat.bindings.v17.Sdf` element containing
        the world/model to turn into a frame graph.
    unwrap : bool
        If True (default) and the sdf only contains a single light, model, or
        world element return that element's frame. If the sdf contains multiple
        lights, models, or worlds a list of root frames is returned. If False,
        always return a list of frames.

    Returns
    -------
    graph : _graph.Graph
        A container storing the nodes and edges of the frame graph.

    links : Dict[str, Frames]
        A dict of (named) links in the graph.

    Notes
    -----
    It is necessary to split the parsers, since versions differ so heavily.
    """

    sdf_root: v17.Sdf = sdformat.loads(sdf)
    graph_list: List[Graph] = list()
    link_dict = dict()

    for world in sdf_root.world:
        graph = convert_world(world, root_uri=root_uri)
        graph.root_node = world.name
        graph_list.append(graph)

    for model in sdf_root.model:
        graph = convert_model(model, root_uri=root_uri)
        graph.root_node = model.name
        graph_list.append(graph)

    for light in sdf_root.light:
        graph = convert_light(light)
        graph.root_node = light.name
        graph_list.append(graph)

    if unwrap and len(graph_list) == 1:
        return graph_list[0]
    else:
        return graph_list
