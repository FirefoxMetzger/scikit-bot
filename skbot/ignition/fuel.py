from urllib.parse import quote
import cachetools
import requests
from cachetools import TTLCache
from zipfile import ZipFile
from io import BytesIO
from pathlib import Path

from dataclasses import dataclass, field
from typing import List, Optional, Callable, Union


class InternalCache:
    """Simple Caching structure"""

    def __init__(self, maxsize=float("inf"), time_to_live=24 * 60 * 60) -> None:
        self._cache = TTLCache(maxsize=maxsize, ttl=time_to_live)

    def update(self, url: str, file_path: str, value: str) -> None:
        key = hash((url, file_path))
        self._cache[key] = value

    def get(self, url: str, file_path: str) -> Union[str, None]:
        key = hash((url, file_path))
        return self._cache.get(key, None)

    def clear(self) -> None:
        self._cache.clear()


model_cache = InternalCache()
world_cache = InternalCache()
metadata_cache = cachetools.LRUCache(maxsize=100)
download_cache = cachetools.LRUCache(maxsize=5)


class FileCache:
    """A Fuel Model cache on the local filesystem"""

    def __init__(self, location: str):
        self._base = Path(location).expanduser()
        self._base = self._base / "fuel.ignitionrobotics.org"
        self._base.mkdir(exist_ok=True, parents=True)

    def _model_loc(self, url: str) -> Path:
        cache_loc = self._base
        metadata = get_fuel_model_info(url)

        username = metadata.owner.lower()
        model_name = quote(metadata.name)
        version = metadata.version

        model_loc = cache_loc / username / "models"
        model_loc = model_loc / model_name / str(version)

        return model_loc.expanduser()

    def get(self, url: str, file_path: str) -> Union[str, None]:
        """Load the SDF from the file cache"""
        file_loc = self._model_loc(url) / file_path

        if file_loc.exists():
            return file_loc.read_text()
        else:
            return None

    def update(self, url: str, file_path: str, sdf_string: str) -> str:
        """Update the file cache after a miss"""
        model_loc = self._model_loc(url)
        blob = download_fuel_model(url)
        with ZipFile(BytesIO(blob)) as model_file:
            model_file.extractall(model_loc)


@dataclass
class ModelMetadata:
    """Response object of the Fuel REST API"""

    createdAt: str
    updatedAt: str
    name: str
    owner: str
    description: str
    likes: int
    downloads: int
    filesize: int
    upload_date: str
    modify_date: str
    license_id: int
    license_name: str
    license_url: str
    license_image: str
    permission: int
    url_name: int
    thumbnail_url: int
    version: int
    private: bool
    tags: List[str] = field(default_factory=list)
    categories: List[str] = field(default_factory=list)


@cachetools.cached(metadata_cache)
def get_fuel_model_info(url: str) -> ModelMetadata:
    """Fetch a Fuel model's metadata.

    Parameters
    ----------
    uri : str
        The URI of the fuel model. This matches the URI
        used in SDFormat's include tags.

    Returns
    -------
    info : Metadata
        A python dataclass of metadata.

    Notes
    -----
    The function caches the most recent 100 calls in an effort to ease the
    burden on the Fuel servers and to improve performance. To manually reset
    this cache call ``skbot.ignition.fuel.metadata_cache.clear()``. You can
    further also this behavior by changing ``skbot.ignition.fuel.metadata_cache``
    to a different cache instance. Check the `cachetools docs
    <https://cachetools.readthedocs.io/en/stable/#>`_ for more information.

    Examples
    --------

    .. doctest::

        >>> import skbot.ignition as ign
        >>> foo = ign.get_fuel_model_info(
        ...     "https://fuel.ignitionrobotics.org/1.0/OpenRobotics/models/Construction%20Cone"
        ... )
        >>> # notice that the second call is almost instantaneous due to in-memory caching
        >>> foo = ign.get_fuel_model_info(
        ...     "https://fuel.ignitionrobotics.org/1.0/OpenRobotics/models/Construction%20Cone"
        ... )
        >>> foo.owner
        'OpenRobotics'
        >>> foo.version
        2
        >>> foo.filesize
        622427

    """

    result = requests.get(url, headers={"accept": "application/json"})
    result.raise_for_status()
    return ModelMetadata(**result.json())


@cachetools.cached(download_cache)
def download_fuel_model(url: str) -> bytes:
    """Download a model from the Fuel server.

    Parameters
    ----------
    url : str
        The URL of the model. This is the same as the URL used for
        include elements in SDF files.

    Returns
    -------
    blob : bytes
        A gzip compressed blob containing the model files.

    Notes
    -----
    The function caches the most recent 5 calls in an effort to ease the
    burden on the Fuel servers and to improve performance. To manually reset
    this cache call ``skbot.ignition.fuel.download_cache.clear()``. You can
    further also this behavior by changing ``skbot.ignition.fuel.download_cache``
    to a different cache instance. Check the `cachetools docs
    <https://cachetools.readthedocs.io/en/stable/#>`_ for more information.

    """

    metadata = get_fuel_model_info(url)
    username = metadata.owner.lower()
    model_name = quote(metadata.name)
    version = metadata.version

    base_url = f"https://fuel.ignitionrobotics.org/1.0/{username}/models/{model_name}/{version}/"
    zip_url = base_url + f"{model_name}.zip"

    result = requests.get(
        url=zip_url, stream=True, headers={"accept": "application/zip"}
    )
    result.raise_for_status()
    blob = result.content

    return blob


def get_fuel_model(
    url: str,
    *,
    file_path: str = "model.sdf",
    user_cache: Callable[[str, str], Union[str, None]] = None,
    use_internal_cache: bool = True,
    use_file_cache: bool = True,
    update_file_cache: bool = True,
    update_internal_cache: bool = True,
    update_user_cache: Callable[[str, str, str], None] = None,
    file_cache_dir: str = "~/.ignition/fuel",
) -> str:
    """Get a model file from the Fuel server.

    Parameters
    ----------
    url : str
        The URL of the model. This is the same as the URL used for
        include elements in SDF files.
    file_path : str
        The path - relative to model root - to the file that should be
        downloaded. Defaults to the model's primary SDF at "model.sdf".
    user_cache : Callable[[str, str], Union[str, None]]
        User supplied caching logic. It is a callable that expects two strings
        (url and file_path) and returns either a string (the file) or None. If
        user_cache returns a string it is considered a cache hit; if user_cache
        returns ``None`` this is interpreted as a cache miss. If ``user_cache is
        None`` it always misses.
    use_internal_cache : bool
        If ``True`` (default), use scikit-bot's internal cache. This is a in-memory
        cache that evicts files after 24 hours, or when scikit-bot is unloaded. If
        ``False``, the internal cache always misses.
    use_file_cache : bool
        If ``True`` (default), check the local filesystem for a copy of the
        model file.
    update_file_cache : str
        If not ``None``, update the file cache at ``file_cache_dir`` on file
        cache misses.
    update_internal_cache : bool
        If ``True`` (default) update the internal cache if it missed.
    update_user_cache : Callable[[str, str, str], None]
        If not ``None`` and user_cache missed (returns ``None`` or is ``None``),
        update_user_cache is called with the signature ``update_user_cache(url,
        file_path, sdf_string)``. The expected behavior is that this call will
        update the user supplied caching mechanism.
    file_cache_dir : str
        The folder to use for the file cache. It follows the same layout as
        ignition's fuel-tools; see the Notes for more information. The default
        is ``~/.ignition/fuel``, which is the default location for ignition.


    Returns
    -------
    sdf_string : str
        A string containing the content of the model's primary SDF (./model.sdf)

    Notes
    -----

    Caches are tiered and the order in which they are checked (from first to
    last) is: (1) user_cache, (2) internal_cache, (3) file_cache. Updates are
    done in reverse order. Further, a cache is only updated if it would have
    been used, i.e., if user_cache hits then neither the internal_cache nor the
    file_cache are updated since they are never evaluated, even if they would
    have produced a miss.

    You can manually reset the internal caches by calling::

        skbot.ignition.fuel.model_cache.clear()
        skbot.ignition.fuel.world_cache.clear()

    The file_cache stores models on your local filesystem. It never evicts, so
    you should manually delete outdated models. The format of the cache
    is::

        file_cache_dir/fuel.ignitionrobotics.org/{owner}/models/{model_name}/{version}

    Examples
    --------

    .. doctest::

        >>> import skbot.ignition as ign
        >>> sdf_string = ign.get_fuel_model(
        ...     "https://fuel.ignitionrobotics.org/1.0/OpenRobotics/models/Construction%20Cone"
        ... )
        >>> sdf_string[:75]+" ..."
        '<?xml version="1.0" ?>\\n<sdf version="1.5">\\n  <model name="Construction Cone ...'
        >>> # Notice that (by default) the entire model is cached. Subsequent calls to
        >>> # model files thus happen at least at filesystem speed
        >>> model_config = ign.get_fuel_model(
        ...     "https://fuel.ignitionrobotics.org/1.0/OpenRobotics/models/Construction%20Cone",
        ...     file_path="model.config"
        ... )
        >>> model_config[:75]+" ..."
        '<?xml version="1.0"?>\\n\\n<model>\\n  <name>Construction Cone</name>\\n  <version> ...'


    """

    def cache(get_fn: Optional[Callable], update_fn: Optional[Callable]):
        def decorator(download_sdf: Callable):
            def inner(url, file_path):
                sdf_string = None

                if get_fn:
                    # query cache
                    sdf_string = get_fn(url, file_path)

                if sdf_string is None:
                    # cache miss
                    sdf_string = download_sdf(url, file_path)

                    if update_fn is not None:
                        update_fn(url, file_path, sdf_string)

                return sdf_string

            return inner

        return decorator

    # set up file cache
    get_from_file = None
    update_file = None
    if use_file_cache or update_file_cache:
        file_cache = FileCache(file_cache_dir)
        if use_file_cache:
            get_from_file = file_cache.get
        if update_file_cache:
            update_file = file_cache.update
    file_cache_decorator = cache(get_from_file, update_file)

    # set up internal cache
    get_internal = model_cache.get if use_internal_cache else None
    update_internal = model_cache.update if update_internal_cache else None
    internal_cache_decorator = cache(get_internal, update_internal)

    # the wrapped loading function
    @cache(user_cache, update_user_cache)
    @internal_cache_decorator
    @file_cache_decorator
    def _fetch_online(url: str, file_path: str) -> str:
        """Download the model and extract primary SDF"""
        blob = download_fuel_model(url)
        with ZipFile(BytesIO(blob)) as model_file:
            with model_file.open(file_path, "r") as data_file:
                file_content = data_file.read().decode("utf-8")

        return file_content

    return _fetch_online(url, file_path)
