import pytest
from requests.exceptions import HTTPError
import hashlib
import cachetools

import ropy.ignition as ign


def test_get_fuel_model_info(model_params, fuel_url):
    owner, name, version = model_params
    metadata = ign.get_fuel_model_info(fuel_url)
    assert metadata.name == name
    assert metadata.owner == owner


def test_nonexistant_object():
    url = "https://fuel.ignitionrobotics.org/1.0/FirefoxMetzger/models/nonexistant"
    with pytest.raises(HTTPError):
        ign.get_fuel_model_info(url)


def test_download(fuel_url, model_md5):
    model_file = ign.download_fuel_model(fuel_url)

    hash_md5 = hashlib.md5()
    hash_md5.update(model_file)
    computed_md5 = hash_md5.hexdigest()

    assert computed_md5 == model_md5


def test_get_model(fuel_url, model_sdf, mock_download):
    sdf_string = ign.get_fuel_model(fuel_url)
    assert sdf_string == model_sdf


def test_get_model_file(fuel_url, model_config, mock_download):
    xml_string = ign.get_fuel_model(fuel_url, file_path="./model.config")
    assert xml_string == model_config


def test_get_model_no_cache(
    fuel_url, model_sdf, invalid_model_cache, invalid_file_cache
):
    sdf_string = ign.get_fuel_model(
        fuel_url,
        use_internal_cache=False,
        update_internal_cache=False,
        use_file_cache=False,
        update_file_cache=False,
        file_cache_dir=invalid_file_cache,
    )

    assert sdf_string == model_sdf


def test_get_model_file_cache_hit(
    fuel_url, model_sdf, invalid_model_cache, populated_file_cache, mock_download_raise
):
    sdf_string = ign.get_fuel_model(
        fuel_url,
        use_internal_cache=False,
        update_internal_cache=False,
        file_cache_dir=populated_file_cache,
    )

    assert sdf_string == model_sdf


def test_get_model_file_cache_miss(
    fuel_url, model_sdf, invalid_model_cache, empty_file_cache, mock_download
):
    sdf_string = ign.get_fuel_model(
        fuel_url,
        use_internal_cache=False,
        update_internal_cache=False,
        file_cache_dir=empty_file_cache,
    )

    assert sdf_string == model_sdf


def test_get_model_file_cache_heal(
    fuel_url, model_sdf, invalid_model_cache, invalid_file_cache, mock_download
):
    # ensure that cache is broken
    sdf_string = ign.get_fuel_model(
        fuel_url,
        use_internal_cache=False,
        update_internal_cache=False,
        use_file_cache=True,
        update_file_cache=False,
        file_cache_dir=invalid_file_cache,
    )
    with pytest.raises(AssertionError):
        assert sdf_string == model_sdf

    # this will heal the cache
    sdf_string = ign.get_fuel_model(
        fuel_url,
        use_internal_cache=False,
        update_internal_cache=False,
        use_file_cache=False,
        update_file_cache=True,
        file_cache_dir=invalid_file_cache,
    )

    # and the next time around the cache is sane
    sdf_string = ign.get_fuel_model(
        fuel_url,
        use_internal_cache=False,
        update_internal_cache=False,
        use_file_cache=True,
        update_file_cache=True,
        file_cache_dir=invalid_file_cache,
    )
    assert sdf_string == model_sdf


def test_get_model_internal_cache_hit(
    fuel_url, model_sdf, populated_model_cache, invalid_file_cache, mock_download_raise
):
    sdf_string = ign.get_fuel_model(
        fuel_url,
        use_internal_cache=True,
        update_internal_cache=True,
        use_file_cache=False,
        update_file_cache=False,
        file_cache_dir=invalid_file_cache,
    )

    assert sdf_string == model_sdf


def test_get_model_internal_cache_heal(
    fuel_url, model_sdf, invalid_model_cache, invalid_file_cache, mock_download
):
    # ensure that cache is broken
    sdf_string = ign.get_fuel_model(
        fuel_url,
        use_internal_cache=True,
        update_internal_cache=False,
        use_file_cache=False,
        update_file_cache=False,
        file_cache_dir=invalid_file_cache,
    )
    with pytest.raises(AssertionError):
        assert sdf_string == model_sdf

    # this will heal the cache
    sdf_string = ign.get_fuel_model(
        fuel_url,
        use_internal_cache=False,
        update_internal_cache=True,
        use_file_cache=False,
        update_file_cache=False,
        file_cache_dir=invalid_file_cache,
    )

    # and the next time around the cache is sane
    sdf_string = ign.get_fuel_model(
        fuel_url,
        use_internal_cache=True,
        update_internal_cache=True,
        use_file_cache=False,
        update_file_cache=False,
        file_cache_dir=invalid_file_cache,
    )
    assert sdf_string == model_sdf


def test_get_model_custom_cache_hit(
    fuel_url,
    model_sdf,
    populated_custom_cache,
    invalid_model_cache,
    invalid_file_cache,
    mock_download_raise,
):
    sdf_string = ign.get_fuel_model(
        fuel_url,
        user_cache=populated_custom_cache[0],
        update_user_cache=populated_custom_cache[1],
        use_internal_cache=False,
        update_internal_cache=False,
        use_file_cache=False,
        update_file_cache=False,
        file_cache_dir=invalid_file_cache,
    )

    assert sdf_string == model_sdf


def test_get_model_custom_cache_heal(
    fuel_url,
    model_sdf,
    invalid_custom_cache,
    invalid_model_cache,
    invalid_file_cache,
    mock_download,
):
    # ensure that cache is broken
    sdf_string = ign.get_fuel_model(
        fuel_url,
        user_cache=invalid_custom_cache[0],
        update_user_cache=None,
        use_internal_cache=False,
        update_internal_cache=False,
        use_file_cache=False,
        update_file_cache=False,
        file_cache_dir=invalid_file_cache,
    )
    with pytest.raises(AssertionError):
        assert sdf_string == model_sdf

    # this will heal the cache
    sdf_string = ign.get_fuel_model(
        fuel_url,
        user_cache=None,
        update_user_cache=invalid_custom_cache[1],
        use_internal_cache=False,
        update_internal_cache=False,
        use_file_cache=False,
        update_file_cache=False,
        file_cache_dir=invalid_file_cache,
    )

    # and the next time around the cache is sane
    sdf_string = ign.get_fuel_model(
        fuel_url,
        user_cache=invalid_custom_cache[0],
        update_user_cache=invalid_custom_cache[1],
        use_internal_cache=False,
        update_internal_cache=False,
        use_file_cache=False,
        update_file_cache=False,
        file_cache_dir=invalid_file_cache,
    )
    assert sdf_string == model_sdf


def test_clear_internal_cache(fake_internal_cache: ign.fuel.InternalCache):

    cache_val = fake_internal_cache.get("foo", "bar")
    assert cache_val == "baz"

    fake_internal_cache.clear()

    cache_val = fake_internal_cache.get("foo", "bar")
    assert cache_val == None
