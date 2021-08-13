import numpy as np
from urllib.parse import urlparse
from typing import Callable, Tuple, List, Any

from . import ConverterReturn, LinkDict
from .graph import Graph
from ...fuel import get_fuel_model
from .. import sdformat
from .... import transform as tf


def resolve_include(include:Any, graph:Graph) -> Tuple[Graph, LinkDict]:
    uri_parts = urlparse(include.uri)
    if uri_parts.scheme == "fuel":
        sdf = get_fuel_model(include.uri)
    else:
        raise sdformat.ParseError(f"Unknown include scheme for URI: {include.uri}")

    version = sdformat.get_version(sdf)
    converter: Callable[[str], ConverterReturn]
    converter = {
        "1.0": None,
        "1.2": None,
        "1.3": None,
        "1.4": None,
        "1.5": None,
        "1.6": None,
        "1.7": None,
        "1.8": _v18_parser,
    }[version]

    if converter is None:
        raise NotImplementedError(f"Including SDFormat v{version} is not supported yet.")

    subgraph, link_dict  = converter(sdf)
    graph.extend(subgraph)

    included_root = subgraph.nodes[subgraph.root_node]
    if include.name is not None:
        included_root.name = include.name

    if include.placement_frame is not None:
        child_frame = include.placement_frame
    else:
        child_frame = subgraph.root_node

    tf_link, parent = graph.pose_to_transform(include.pose)
    graph.connect_sdf(parent, child_frame, tf_link)

    return graph, link_dict


def _v18_parser(sdf: str, *, unwrap=True) -> ConverterReturn:
    """Turn v1.8 SDF into a frame graph

    Parameters
    ----------
    sdf_in : Sdf
        A :class:`skbot.ignition.sdformat.bindings.v18.Sdf` element containing
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

    import skbot.ignition.sdformat.bindings.v18 as v18

    def _convert_model(model: v18.ModelModel, *, graph:Graph=None) -> Graph:
        if graph is None:
            graph = Graph()
            graph.add_node(model.name, tf.Frame(3, name=model.name))
        else:
            graph.add_pose(model.name, model.pose)

        with graph.scope(model.name), graph.set_root():
            # TODO: include

            for nested_model in model.model:
                _convert_model(nested_model, graph=graph)

            for frame in model.frame:
                graph.add_pose(frame.name, frame.pose)

            for link in model.link:
                _convert_link(link, graph)

            for joint in model.joint:
                _convert_joint(joint, graph)

            for gripper in model.gripper:
                raise NotImplementedError(
                    "Gripper not implemented yet (lacking upstream docs)."
                )

        return graph

    def _convert_link(link: v18.Link, graph:Graph) -> Graph:
        if link.must_be_base_link:
            link.pose.relative_to = "world"

        graph.add_pose(link.name, link.pose)

        with graph.scope(link.name):
            if link.inertial:
                graph.add_pose("inertial", link.inertial.pose)

            for collision in link.collision:
                _convert_collision(collision, graph)
            
            for visual in link.visual:
                _convert_visual(visual, graph)

            for sensor in link.sensor:
                _convert_sensor(sensor, graph)
        
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
                _convert_light(light, graph=graph)

        return graph

    def _convert_sensor(sensor: v18.Sensor, graph:Graph) -> Graph:
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

    def _convert_joint(joint: v18.Joint, graph:Graph) -> Graph:
        if isinstance(joint.pose, str):
            # xsData bug
            joint.pose = v18.Joint.Pose(joint.pose)
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
            tf_link = tf.Translation((0,0,0))
            graph.connect_sdf(joint.parent, joint.name, tf_link)

        for sensor in joint.sensor:
            _convert_sensor(sensor, graph)

        return graph

    def _convert_collision(collision: v18.Collision, graph:Graph) -> Graph:
        graph.add_pose(collision.name, collision.pose)
        return graph

    def _convert_visual(visual: v18.Visual, graph:Graph) -> Graph:
        graph.add_pose(visual.name, visual.pose)
        return graph

    sdf_root: v18.Sdf = sdformat.loads(sdf)
    graph_list: List[Graph] = list()
    link_dict = dict()

    for world in sdf_root.world:
        graph = _convert_world(world)
        graph.root_node = world.name
        graph_list.append(graph)

    if sdf_root.model is not None:
        graph = _convert_model(sdf_root.model)
        graph.root_node = sdf_root.model.name
        graph_list.append(graph)

    if sdf_root.light is not None:
        graph = _convert_light(sdf_root.model)
        graph.root_node = sdf_root.light.name
        graph_list.append(graph)

    if unwrap and len(graph_list) == 1:
        return graph_list[0], link_dict
    else:
        return graph_list, link_dict
