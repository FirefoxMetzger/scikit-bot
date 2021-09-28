from pathlib import Path
import pytest
import hashlib
from urllib.parse import quote
from zipfile import ZipFile
from io import BytesIO

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
        "robots/double_pendulum/model.sdf",
        "sdformat/audio_14.sdf",
        "sdformat/bad_syntax_double.sdf",
        "sdformat/bad_syntax_pose.sdf",
        "sdformat/bad_syntax_vector.sdf",
        "sdformat/box_bad_test.sdf",
        "sdformat/box_plane_low_friction_test.sdf",
        "sdformat/double_pendulum.sdf",
        "sdformat/empty_axis.sdf",
        "sdformat/empty_road_sph_coords.sdf",
        "sdformat/empty.sdf",
        "sdformat/ignore_sdf_in_plugin.sdf",
        "sdformat/include_with_interface_api_frame_semantics.sdf",
        "sdformat/include_with_interface_api_reposture.sdf",
        "sdformat/includes_1.5.sdf",
        "sdformat/includes_missing_model.sdf",
        "sdformat/includes_missing_uri.sdf",
        "sdformat/includes_model_without_sdf.sdf",
        "sdformat/includes_without_top_level.sdf",
        "sdformat/includes.sdf",
        "sdformat/inertial_complete.sdf",
        "sdformat/inertial_invalid.sdf",
        "sdformat/joint_axis_infinite_limits.sdf",
        "sdformat/joint_axis_xyz_normalization.sdf",
        "sdformat/joint_child_frame.sdf",
        "sdformat/joint_child_world.sdf",
        "sdformat/joint_complete.sdf",
        "sdformat/joint_invalid_child.sdf",
        "sdformat/joint_invalid_parent_same_as_child.sdf",
        "sdformat/joint_invalid_parent.sdf",
        "sdformat/joint_invalid_resolved_parent_same_as_child.sdf",
        "sdformat/joint_invalid_self_child.sdf",
        "sdformat/joint_invalid_self_parent.sdf",
        "sdformat/joint_nested_parent_child.sdf",
        "sdformat/joint_parent_frame.sdf",
        "sdformat/joint_parent_world.sdf",
        "sdformat/joint_sensors.sdf",
        "sdformat/light.sdf",
        "sdformat/link_duplicate_cousin_collisions.sdf",
        "sdformat/link_duplicate_cousin_visuals.sdf",
        "sdformat/link_duplicate_sibling_collisions.sdf",
        "sdformat/link_duplicate_sibling_visuals.sdf",
        "sdformat/material_invalid.sdf",
        "sdformat/material_normal_map_missing.sdf",
        "sdformat/material_script_no_uri.sdf",
        "sdformat/material_valid.sdf",
        "sdformat/material.sdf",
        "sdformat/model_canonical_link.sdf",
        "sdformat/model_duplicate_joints.sdf",
        "sdformat/model_duplicate_links.sdf",
        "sdformat/model_frame_attached_to_joint.sdf",
        "sdformat/model_frame_attached_to_nested_model.sdf",
        "sdformat/model_frame_attached_to.sdf",
        "sdformat/model_frame_invalid_attached_to_cycle.sdf",
        "sdformat/model_frame_invalid_attached_to.sdf",
        "sdformat/model_frame_relative_to_joint.sdf",
        "sdformat/model_frame_relative_to.sdf",
        "sdformat/model_invalid_canonical_link.sdf",
        "sdformat/model_invalid_frame_relative_to_cycle.sdf",
        "sdformat/model_invalid_frame_relative_to.sdf",
        "sdformat/model_invalid_joint_relative_to.sdf",
        "sdformat/model_invalid_link_relative_to.sdf",
        "sdformat/model_invalid_placement_frame.sdf",
        "sdformat/model_invalid_root_reference.sdf",
        "sdformat/model_joint_axis_expressed_in.sdf",
        "sdformat/model_joint_relative_to.sdf",
        "sdformat/model_link_joint_same_name.sdf",
        "sdformat/model_link_relative_to.sdf",
        "sdformat/model_multi_nested_model.sdf",
        "sdformat/model_nested_frame_attached_to.sdf",
        "sdformat/model_nested_model_relative_to.sdf",
        "sdformat/model_nested_static_model.sdf",
        "sdformat/model_relative_to_nested_reference.sdf",
        "sdformat/model_with_placement_frame_attribute.sdf",
        "sdformat/model_without_links.sdf",
        "sdformat/nested_canonical_link.sdf",
        "sdformat/nested_explicit_canonical_link.sdf",
        "sdformat/nested_model_cross_references.sdf",
        "sdformat/nested_model.sdf",
        "sdformat/nested_multiple_elements_error_world.sdf",
        "sdformat/nested_without_links_invalid.sdf",
        "sdformat/placement_frame_missing_pose.sdf",
        "sdformat/root_duplicate_models.sdf",
        "sdformat/root_multiple_models.sdf",
        "sdformat/scene_with_sky.sdf",
        "sdformat/sensors.sdf",
        "sdformat/shapes_world.sdf",
        "sdformat/whitespace.sdf",
        "sdformat/world_complete.sdf",
        "sdformat/world_duplicate.sdf",
        "sdformat/world_frame_attached_to.sdf",
        "sdformat/world_frame_invalid_attached_to_scope.sdf",
        "sdformat/world_frame_invalid_attached_to.sdf",
        "sdformat/world_frame_invalid_relative_to.sdf",
        "sdformat/world_frame_relative_to.sdf",
        "sdformat/world_invalid_root_reference.sdf",
        "sdformat/world_model_frame_same_name.sdf",
        "sdformat/world_nested_frame_attached_to.sdf",
        "sdformat/world_nested_frame.sdf",
        "sdformat/world_nested_model.sdf",
        "sdformat/world_noname.sdf",
        "sdformat/world_relative_to_nested_reference.sdf",
        "sdformat/world_sibling_same_names.sdf",
        "sdformat/world_with_state.sdf",
        "v15/camera.sdf",
        "v15/force_torque.sdf",
        "v15/frames.sdf",
        "v15/joint_attached_to_parent.sdf",
        "v15/light_only.sdf",
        "v15/population.sdf",
        "v15/pose_testing.sdf",
        "v15/projector.sdf",
        "v17/crooked_double_pendulum.sdf",
        "v17/fuel_include.sdf",
        "v17/light_only.sdf",
        "v17/population.sdf",
        "v18/complete_world.sdf",
        "v18/fuel_include_world.sdf",
        "v18/perspective_transform.sdf",
        "v18/population.sdf",
        "v18/pose_testing.sdf",
    ]
)
def valid_sdf_string(request):
    filename = request.param
    return (sdf_folder / filename).read_text()


@pytest.fixture(
    params=[
        "sdformat/material_pbr.sdf",
        "sdformat/empty_invalid.sdf",
        "sdformat/ignore_sdf_in_namespaced_elements.sdf",
        "sdformat/model_include_with_interface_api.sdf",
        "sdformat/stricter_semantics_desc.sdf",
        "sdformat/custom_and_unknown_elements.sdf",
        "sdformat/unrecognized_elements.sdf",
        "sdformat/unrecognized_elements_with_namespace.sdf",
        "sdformat/world_include_with_interface_api.sdf",
        "sdformat/shapes.sdf",
        "sdformat/invalid_version.sdf",
        "sdformat/empty_noversion.sdf",
    ]
)
def invalid_sdf_string(request):
    filename = request.param
    return (sdf_folder / filename).read_text()


@pytest.fixture(
    params=[
        "robots/double_pendulum/model.sdf",
        "sdformat/audio_14.sdf",
        "sdformat/bad_syntax_double.sdf",
        "sdformat/bad_syntax_pose.sdf",
        "sdformat/bad_syntax_vector.sdf",
        "sdformat/box_bad_test.sdf",
        "sdformat/box_plane_low_friction_test.sdf",
        "sdformat/double_pendulum.sdf",
        "sdformat/empty_axis.sdf",
        "sdformat/empty_road_sph_coords.sdf",
        "sdformat/empty.sdf",
        "sdformat/ignore_sdf_in_plugin.sdf",
        "sdformat/inertial_complete.sdf",
        "sdformat/inertial_invalid.sdf",
        "sdformat/joint_axis_infinite_limits.sdf",
        "sdformat/joint_axis_xyz_normalization.sdf",
        "sdformat/joint_child_frame.sdf",
        "sdformat/joint_child_world.sdf",
        "sdformat/joint_complete.sdf",
        "sdformat/joint_invalid_child.sdf",
        "sdformat/joint_invalid_parent_same_as_child.sdf",
        "sdformat/joint_invalid_parent.sdf",
        "sdformat/joint_invalid_resolved_parent_same_as_child.sdf",
        "sdformat/joint_invalid_self_child.sdf",
        "sdformat/joint_invalid_self_parent.sdf",
        "sdformat/joint_nested_parent_child.sdf",
        "sdformat/joint_parent_frame.sdf",
        "sdformat/joint_parent_world.sdf",
        "sdformat/joint_sensors.sdf",
        "sdformat/light.sdf",
        "sdformat/link_duplicate_cousin_collisions.sdf",
        "sdformat/link_duplicate_cousin_visuals.sdf",
        "sdformat/link_duplicate_sibling_collisions.sdf",
        "sdformat/link_duplicate_sibling_visuals.sdf",
        "sdformat/material_invalid.sdf",
        "sdformat/material_normal_map_missing.sdf",
        "sdformat/material_script_no_uri.sdf",
        "sdformat/material_valid.sdf",
        "sdformat/material.sdf",
        "sdformat/model_canonical_link.sdf",
        "sdformat/model_duplicate_joints.sdf",
        "sdformat/model_duplicate_links.sdf",
        "sdformat/model_frame_attached_to_joint.sdf",
        "sdformat/model_frame_attached_to_nested_model.sdf",
        "sdformat/model_frame_attached_to.sdf",
        "sdformat/model_frame_invalid_attached_to_cycle.sdf",
        "sdformat/model_frame_invalid_attached_to.sdf",
        "sdformat/model_frame_relative_to_joint.sdf",
        "sdformat/model_frame_relative_to.sdf",
        "sdformat/model_invalid_canonical_link.sdf",
        "sdformat/model_invalid_frame_relative_to_cycle.sdf",
        "sdformat/model_invalid_frame_relative_to.sdf",
        "sdformat/model_invalid_joint_relative_to.sdf",
        "sdformat/model_invalid_link_relative_to.sdf",
        "sdformat/model_invalid_placement_frame.sdf",
        "sdformat/model_invalid_root_reference.sdf",
        "sdformat/model_joint_axis_expressed_in.sdf",
        "sdformat/model_joint_relative_to.sdf",
        "sdformat/model_link_joint_same_name.sdf",
        "sdformat/model_link_relative_to.sdf",
        "sdformat/model_multi_nested_model.sdf",
        "sdformat/model_nested_frame_attached_to.sdf",
        "sdformat/model_nested_model_relative_to.sdf",

        # potentially faulty. Tracking Issue:
        # https://github.com/ignitionrobotics/sdformat/issues/718
        # "sdformat/model_nested_static_model.sdf",
        
        "sdformat/model_relative_to_nested_reference.sdf",
        "sdformat/model_with_placement_frame_attribute.sdf",
        "sdformat/nested_canonical_link.sdf",
        "sdformat/nested_explicit_canonical_link.sdf",
        "sdformat/nested_model_cross_references.sdf",
        "sdformat/nested_model.sdf",
        "sdformat/root_duplicate_models.sdf",

        # potentially faulty SDF. Tracking Issue
        # https://github.com/ignitionrobotics/sdformat/issues/718
        # "sdformat/root_multiple_models.sdf",
        
        "sdformat/scene_with_sky.sdf",
        "sdformat/sensors.sdf",
        "sdformat/shapes_world.sdf",
        "sdformat/world_complete.sdf",
        "sdformat/world_duplicate.sdf",
        "sdformat/world_frame_attached_to.sdf",
        "sdformat/world_frame_invalid_attached_to_scope.sdf",
        "sdformat/world_frame_invalid_attached_to.sdf",
        "sdformat/world_frame_invalid_relative_to.sdf",
        "sdformat/world_frame_relative_to.sdf",
        "sdformat/world_model_frame_same_name.sdf",
        "sdformat/world_nested_frame_attached_to.sdf",
        "sdformat/world_nested_frame.sdf",
        "sdformat/world_nested_model.sdf",
        "sdformat/world_noname.sdf",
        "sdformat/world_relative_to_nested_reference.sdf",
        "sdformat/world_sibling_same_names.sdf",
        "sdformat/world_with_state.sdf",
        "v15/camera.sdf",
        "v15/force_torque.sdf",
        "v15/frames.sdf",
        "v15/joint_attached_to_parent.sdf",
        "v15/light_only.sdf",
        "v15/population.sdf",
        "v15/pose_testing.sdf",
        "v15/projector.sdf",
        "v17/crooked_double_pendulum.sdf",
        "v17/fuel_include.sdf",
        "v17/light_only.sdf",
        "v17/population.sdf",
        "v18/complete_world.sdf",
        "v18/fuel_include_world.sdf",
        "v18/perspective_transform.sdf",
        "v18/population.sdf",
        "v18/pose_testing.sdf",
    ]
)
def verifiable_sdf_string(request):
    filename = request.param
    return (sdf_folder / filename).read_text()


@pytest.fixture(
    params=[
        "sdformat/placement_frame_missing_pose.sdf",
        "sdformat/whitespace.sdf",
        "sdformat/world_invalid_root_reference.sdf",
        "sdformat/nested_without_links_invalid.sdf",
        "sdformat/nested_multiple_elements_error_world.sdf",
        "sdformat/model_without_links.sdf",
        "sdformat/includes_missing_uri.sdf",
        "sdformat/includes_model_without_sdf.sdf",
        "sdformat/includes_without_top_level.sdf",
        "sdformat/includes.sdf",
        "sdformat/include_with_interface_api_frame_semantics.sdf",
        "sdformat/include_with_interface_api_reposture.sdf",
        "sdformat/includes_1.5.sdf",
        "sdformat/includes_missing_model.sdf",
        "v18/fuel_include_unknown_server.sdf",
        "v18/invalid_joint_type.sdf",
        "v18/invalid_same_scope_twice.sdf",
        "v18/invalid_sensor_type.sdf",
    ]
)
def unverifiable_sdf_string(request):
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
