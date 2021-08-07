from typing import Dict, List, Tuple
from xml.etree import ElementTree
import numpy as np
from dataclasses import dataclass
from typing import List, Dict
import requests
from urllib.parse import urlparse
from pathlib import Path

from ... import transform as rtf


def _xpath_from_elements(elements: List[ElementTree.Element]) -> str:
    return ("/" if len(elements) > 0 else "") + "/".join(
        el.attrib["name"] if "name" in el.attrib else el.tag for el in elements
    )


def _fetch_include_uri(
    include_element: List[ElementTree.Element], *, fuel_download_path: str = None
) -> str:
    """Convert an include element into the full sdf.

    Includes Fuel support.

    Parameters
    ----------
    fuel_download_path : str
        If specified, download the full model from the fuel database into the
        specified directory. If None, only fetch the relevant model.sdf
        (in-memory).

    """
    uri = include_element.find("uri").text
    uri_parts = urlparse(uri)

    # include fuel model
    if uri_parts.scheme == "https" and uri_parts.netloc == "fuel.ignitionrobotics.org":
        # I reverse engineered this from the ign_fuel_tools C++ project
        # and from https://app.ignitionrobotics.org/api If you know a
        # cleaner way that doesn't involve adding a C++ to the codebase
        # just to download files please open an issue :)

        file_list: requests.Response = requests.get(uri + "/files")
        if file_list.status_code != 200:
            # Note: I would like to discover the latest version if
            # it isn't specified explicitly, but didn't manage to
            # work this out yet
            uri = uri + "/1"
            file_list: requests.Response = requests.get(uri + "/files")

        if file_list.status_code != 200:
            raise IOError(f"Could not download element from: {uri}")

        for item in file_list.json()["file_tree"]:
            if item["name"] == "model.sdf":
                location = uri + "/files" + item["path"]
                sdf_string = requests.get(location).content.decode("utf-8")
                break
        else:
            raise IOError(f"Could not get sdf from: {uri}")

        if fuel_download_path is not None:
            # tree all files
            full_file_list = list()
            file_queue = file_list.json()["file_tree"]
            while len(file_queue) > 0:
                element = file_queue.pop(0)
                if "children" in element.keys():
                    file_queue += element["children"]
                else:
                    full_file_list.append(element["path"])

            # TODO: figure out the default naming scheme for fuel downloads
            # to match the official fuel cache.
            base_dir = fuel_download_path / file_list.json()["name"]
            for file in full_file_list:
                location: Path = base_dir / file[1:]
                location.parent.mkdir(exist_ok=True, parents=True)
                file_request = requests.get(uri + "/files" + file)

                with open(location, "wb") as file_on_disk:
                    file_on_disk.write(file_request.content)

    elif uri_parts.scheme == "" or uri_parts.scheme == "file":
        with open(uri, "r") as sdf_file:
            sdf_string = sdf_file.read()

    else:
        raise IOError(f"Could not get sdf from: {uri}")

    return sdf_string


def create_frame_graph(sdf: str) -> Tuple[Dict[str, rtf.Frame], Dict[str, rtf.Link]]:
    """Create a frame graph from a sdformat string.

    Parameters
    ----------
    sdformat: TextIO
        A text buffer containing the SDFormat XML.

    Returns
    -------
    frames : Dict[str, Frames]
        A dict of named frames. Keys and frame names correspond to each
        element's xpath. An xpath is a string representing the position of the
        element in the tree it is constructed from concatenating element tags
        using ``/`` except for elements that have a ``name`` attribute. In this
        case, the respective name is used instead of the tag. Examples:
        `/sdf/spot_light/pose` or `/sdf/world_1/my_robot/joint_1`

    links : Dict[str, Frames]
        A dict of (named) links in the graph.

    See Also
    --------
    :mod:`skbot.transform`

    """

    root = ElementTree.fromstring(sdf)
    tree = ElementTree.ElementTree(root)

    @dataclass
    class SdfQueueItem:
        element: ElementTree.Element
        parents: List[ElementTree.Element]

    @dataclass
    class PoseQueueItem:
        pose: np.ndarray
        parents: List[ElementTree.Element]
        relative_to: str = ""

    xpaths = dict()
    links = dict()
    pose_list: List[PoseQueueItem] = list()

    queue = [SdfQueueItem(root, list())]
    while len(queue) > 0:
        item: SdfQueueItem = queue.pop(0)

        for child in item.element:
            queue.append(SdfQueueItem(child, item.parents + [item.element]))

        # each elements gets an accompanying frame based on its xPath
        # if the element has a name, the frame will get that name, too
        name = item.element.attrib["name"] if "name" in item.element.attrib else None
        xpath_str = item.element.tag if name is None else name
        xpath = _xpath_from_elements(item.parents) + "/" + xpath_str

        if xpath in xpaths.keys():
            Warning(
                "non-unique xpaths found. Inspect the sdf file for errors and tread carefully."
            )

        xpaths[xpath] = rtf.Frame(3, name=xpath)

        # element specific graph modifications
        if item.element.tag == "pose":
            pose_tag = item.element
            pose = np.array(pose_tag.text.split(" "), dtype=np.float_)

            parent = _xpath_from_elements(item.parents[:-1])
            child = _xpath_from_elements(item.parents)
            pose_item = PoseQueueItem(pose, item.parents)
            if "relative_to" in pose_tag.keys():
                pose_item.relative_to = pose_tag.attrib["relative_to"]

            # we construct links at the end, because the "relative_to"
            # frame may not have been defined yet.
            pose_list.append(pose_item)

        elif item.element.tag == "include":
            # included sdf contains _exactly_ one child
            include_sdf_string = _fetch_include_uri(item.element)
            sdf_element = ElementTree.fromstring(include_sdf_string)[0]

            name_element = item.element.find("name")
            if name_element is not None:
                sdf_element.set("name", name_element.text)

            static_element = item.element.find("static")
            if name_element is not None:
                sdf_element.find("static").text = static_element.text

            # TODO: add support for pose and reference_frame

            queue.append(SdfQueueItem(sdf_element, item.parents))

    # all frames exist, add links
    # add pose-based (static) links to graph
    for item in pose_list:
        parent = _xpath_from_elements(item.parents[:-1])
        child = _xpath_from_elements(item.parents)

        if item.relative_to:
            # resolve relative parent including grandparents
            for idx in range(len(item.parents), 1, -1):
                parent_xpath = _xpath_from_elements(item.parents[:idx])
                xpath = parent_xpath + "/" + item.relative_to
                if xpath in xpaths:
                    parent = xpath
                    break
            else:
                raise RuntimeError(
                    f"The Frame '{item.parent}' does not exist among the parents of {item.child}."
                )

        parent_frame = xpaths[parent]
        child_frame = xpaths[child]
        if np.any(pose[3:]) != 0:
            rotated = rtf.EulerRotation("xyz", pose[3:])(child_frame)
            rtf.Translation(pose[:3])(rotated, parent_frame)
        else:
            rtf.Translation(pose[:3])(child_frame, parent_frame)

    return xpaths, links
