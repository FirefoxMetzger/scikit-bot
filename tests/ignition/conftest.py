from pathlib import Path
from skbot.ignition.sdformat.bindings.v13 import sdf
from skbot.ignition import fuel
import pytest
import hashlib
from urllib.parse import quote
from zipfile import ZipFile
from io import BytesIO
import cachetools

import skbot.ignition as ign

sdf_folder = Path(__file__).parent / "sdf"

"""
SDF Fixtures
------------

"""


@pytest.fixture
def light_sdf():
    return (sdf_folder / "light.sdf").read_text()


@pytest.fixture(params=[p.name for p in sdf_folder.iterdir()])
def sdf_string(request):
    filename = request.param
    return (sdf_folder / filename).read_text()


@pytest.fixture(
    params=[
        "link_duplicate_cousin_visuals.sdf",
        "world_sibling_same_names.sdf",
        "root_multiple_models.sdf",
        "joint_sensors.sdf",
        "scene_with_sky.sdf",
        "material_script_no_uri.sdf",
        "double_pendulum.sdf",
        "bad_syntax_pose.sdf",
        "joint_invalid_resolved_parent_same_as_child.sdf",
        "model_link_relative_to.sdf",
        "light.sdf",
        "model_invalid_frame_relative_to_cycle.sdf",
        "model_relative_to_nested_reference.sdf",
        "model_nested_static_model.sdf",
        "inertial_complete.sdf",
        "model_multi_nested_model.sdf",
        # "world_with_state.sdf",  # disabled. See: https://github.com/ignitionrobotics/sdformat/issues/653
        "material_normal_map_missing.sdf",
        "model_without_links.sdf",
        "model_frame_relative_to.sdf",
        "joint_parent_frame.sdf",
        "includes_missing_uri.sdf",
        "includes_missing_model.sdf",
        "joint_invalid_parent_same_as_child.sdf",
        "world_frame_relative_to.sdf",
        "whitespace.sdf",
        "flattened_test_nested_model_with_frames.sdf",
        "empty_road_sph_coords.sdf",
        "world_nested_frame.sdf",
        "joint_complete.sdf",
        "world_frame_attached_to.sdf",
        "world_frame_invalid_attached_to_scope.sdf",
        "bad_syntax_double.sdf",
        "material_valid.sdf",
        "joint_invalid_self_parent.sdf",
        "world_nested_model.sdf",
        "model_frame_attached_to.sdf",
        "placement_frame.sdf",
        "empty.sdf",
        "joint_axis_xyz_normalization.sdf",
        "joint_child_world.sdf",
        "includes_model_without_sdf.sdf",
        "world_invalid_root_reference.sdf",
        "model_invalid_joint_relative_to.sdf",
        "world_frame_invalid_attached_to.sdf",
        "link_duplicate_sibling_visuals.sdf",
        "inertial_invalid.sdf",
        "model_nested_model_relative_to.sdf",
        "material.sdf",
        "includes_without_top_level.sdf",
        "include_with_interface_api_reposture.sdf",
        "joint_axis_infinite_limits.sdf",
        "nested_model_cross_references.sdf",
        "model_frame_relative_to_joint.sdf",
        "link_duplicate_sibling_collisions.sdf",
        "bad_syntax_vector.sdf",
        "world_duplicate.sdf",
        "model_invalid_reserved_names.sdf",
        "model_invalid_link_relative_to.sdf",
        "box_plane_low_friction_test.sdf",
        "model_joint_axis_expressed_in.sdf",
        "nested_explicit_canonical_link.sdf",
        "model_frame_attached_to_joint.sdf",
        "nested_canonical_link.sdf",
        "root_duplicate_models.sdf",
        "material_invalid.sdf",
        "link_duplicate_cousin_collisions.sdf",
        "joint_invalid_parent.sdf",
        "model_frame_invalid_attached_to.sdf",
        "joint_invalid_self_child.sdf",
        "model_invalid_root_reference.sdf",
        "joint_invalid_child.sdf",
        "joint_nested_parent_child.sdf",
        "world_relative_to_nested_reference.sdf",
        # "sensors.sdf",  # disabled. See: https://github.com/ignitionrobotics/sdformat/issues/653
        "joint_child_frame.sdf",
        "ignore_sdf_in_plugin.sdf",
        "model_nested_frame_attached_to.sdf",
        "model_with_placement_frame_attribute.sdf",
        "model_canonical_link.sdf",
        "include_with_interface_api_frame_semantics.sdf",
        "model_invalid_frame_relative_to.sdf",
        "world_noname.sdf",
        "model_duplicate_joints.sdf",
        "shapes_world.sdf",
        "world_model_frame_same_name.sdf",
        "box_bad_test.sdf",
        "model_frame_attached_to_nested_model.sdf",
        "model_invalid_canonical_link.sdf",
        "panda_world.sdf",
        "includes_1.5.sdf",
        "model_duplicate_links.sdf",
        "joint_parent_world.sdf",
        "world_frame_invalid_relative_to.sdf",
        "model_invalid_placement_frame.sdf",
        "model_frame_invalid_attached_to_cycle.sdf",
        "model_joint_relative_to.sdf",
        "nested_without_links_invalid.sdf",
        "world_nested_frame_attached_to.sdf",
        "model_link_joint_same_name.sdf",
        "nested_model.sdf",
        "empty_axis.sdf",
        "placement_frame_missing_pose.sdf",
        "nested_multiple_elements_error_world.sdf",
        "audio_14.sdf",
    ]
)
def valid_sdf_string(request):
    filename = request.param
    return (sdf_folder / filename).read_text()


@pytest.fixture(
    params=[
        "material_pbr.sdf",
        "empty_invalid.sdf",
        "ignore_sdf_in_namespaced_elements.sdf",
        "model_include_with_interface_api.sdf",
        "stricter_semantics_desc.sdf",
        "custom_and_unknown_elements.sdf",
        "unrecognized_elements.sdf",
        "unrecognized_elements_with_namespace.sdf",
        "world_include_with_interface_api.sdf",
        "world_valid_root_reference.sdf",
        "world_complete.sdf",
        "shapes.sdf",
        "includes.sdf",
        "invalid_version.sdf",
        "empty_noversion.sdf",
    ]
)
def invalid_sdf_string(request):
    filename = request.param
    return (sdf_folder / filename).read_text()


"""
Fuel Fixtures
-------------

"""


@pytest.fixture(
    scope="module",
    params=[("Gambit", "Lemon", None), ("OpenRobotics", "Construction Cone", None)],
)
def model_params(request):
    owner, name, version = request.param
    return owner, name, version


@pytest.fixture(scope="module")
def fuel_url(model_params):
    owner, name, version = model_params

    url = "https://fuel.ignitionrobotics.org/1.0/"
    url += f"{owner}/models/{quote(name)}"

    if version:
        url += f"/{version}/{quote(name)}"

    return url


@pytest.fixture(scope="module")
def fuel_blob(fuel_url):
    blob = ign.download_fuel_model(fuel_url)
    return blob


@pytest.fixture(scope="module")
def model_md5(fuel_blob):
    hash_md5 = hashlib.md5()
    hash_md5.update(fuel_blob)
    return hash_md5.hexdigest()


@pytest.fixture(scope="module")
def model_sdf(fuel_blob):
    with ZipFile(BytesIO(fuel_blob)) as model_file:
        with model_file.open("model.sdf", "r") as sdf_file:
            sdf_string = sdf_file.read().decode("utf-8")

    return sdf_string


@pytest.fixture(scope="module")
def model_config(fuel_blob):
    with ZipFile(BytesIO(fuel_blob)) as model_file:
        with model_file.open("model.config", "r") as sdf_file:
            xml_string = sdf_file.read().decode("utf-8")

    return xml_string


@pytest.fixture()
def single_fuel_url():
    """Used for tests where testing all fuel_urls is too expensive"""

    return (
        "https://fuel.ignitionrobotics.org/1.0/OpenRobotics/models/Construction%20Cone"
    )


@pytest.fixture()
def mock_download(fuel_blob, monkeypatch):
    def monkey_download(url: str) -> bytes:
        return fuel_blob

    with monkeypatch.context() as monkey:
        monkey.setattr(ign, "download_fuel_model", monkey_download)
        yield


@pytest.fixture()
def mock_download_raise(monkeypatch):
    def monkey_download(url: str) -> bytes:
        raise RuntimeError("Should not call download.")

    with monkeypatch.context() as monkey:
        monkey.setattr(ign, "download_fuel_model", monkey_download)
        yield


@pytest.fixture
def empty_custom_cache():
    cache = dict()

    def update(url, file_path, sdf_string):
        key = hash((url, file_path))
        cache[key] = sdf_string

    return lambda x, y: cache.get(hash((x, y)), None), update


@pytest.fixture
def populated_custom_cache(fuel_url, model_sdf):
    key = hash((fuel_url, "model.sdf"))
    cache = {key: model_sdf}

    def update(url, file_path, sdf_string):
        key = hash((url, file_path))
        cache[key] = sdf_string

    return lambda x, y: cache.get(hash((x, y)), None), update


@pytest.fixture
def invalid_custom_cache(fuel_url, model_sdf):
    key = hash((fuel_url, "model.sdf"))
    cache = {key: "Not a SDF string."}

    def update(url, file_path, sdf_string):
        key = hash((url, file_path))
        cache[key] = sdf_string

    return lambda x, y: cache.get(hash((x, y)), None), update


@pytest.fixture()
def empty_model_cache(monkeypatch):
    tmp_cache = ign.fuel.InternalCache(maxsize=5)

    with monkeypatch.context() as monkey:
        monkey.setattr(ign.fuel, "model_cache", tmp_cache)
        yield


@pytest.fixture()
def populated_model_cache(fuel_url, model_sdf, empty_model_cache):
    ign.fuel.model_cache.update(fuel_url, "model.sdf", model_sdf)


@pytest.fixture()
def invalid_model_cache(fuel_url, empty_model_cache):
    ign.fuel.model_cache.update(fuel_url, "model.sdf", "incorrect SDF from model cache")


@pytest.fixture()
def empty_file_cache(tmp_path, mock_download):
    return tmp_path


@pytest.fixture()
def populated_file_cache(fuel_url, empty_file_cache):
    cache = ign.fuel.FileCache(empty_file_cache)
    cache.update(fuel_url, "model.sdf", "unused arg to match signature")

    return empty_file_cache


@pytest.fixture()
def invalid_file_cache(fuel_url, populated_file_cache):
    cache = ign.fuel.FileCache(populated_file_cache)
    loc = cache._model_loc(fuel_url)
    with open(loc / "model.sdf", "w") as file:
        file.write("Invalid SDF file")

    return populated_file_cache


@pytest.fixture()
def fake_internal_cache():
    fake_cache = ign.fuel.InternalCache()
    fake_cache.update("foo", "bar", "baz")
    return fake_cache
