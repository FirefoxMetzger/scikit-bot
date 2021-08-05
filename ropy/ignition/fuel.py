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

    def update(self, url: str, value: str) -> None:
        # metadata = fuel_model_metadata(url)
        self._cache[url] = value

    def get(self, url) -> Union[str, None]:
        return self._cache.get(url, None)

    def clear(self) -> None:
        self._cache.clear()


model_cache = InternalCache()
world_cache = InternalCache()
metadata_cache = cachetools.LRUCache(maxsize=100)
download_cache = cachetools.LRUCache(maxsize=5)


class FileCache:
    """A Fuel Model cache on the local filesystem"""

    def __init__(self, location: str):
        self._base = Path(location) / "fuel.ignitionrobotics.org"
        self._base.mkdir(exist_ok=True, parents=True)

    def _model_loc(self, url: str) -> Path:
        cache_loc = self._base
        metadata = get_fuel_model_info(url)

        username = metadata.owner.lower()
        model_name = quote(metadata.name)
        version = metadata.version

        model_loc: Path = cache_loc / username / "models" / model_name / str(version)

        return model_loc.expanduser()

    def get(self, url: str) -> Union[str, None]:
        """Load the SDF from the file cache"""
        file_loc = self._model_loc(url) / "model.sdf"

        if file_loc.exists():
            return file_loc.read_text()
        else:
            return None

    def update(self, url: str, sdf_string: str) -> str:
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
def get_fuel_model_info(uri: str) -> ModelMetadata:
    """Fetch a Fuel model's metadata.

    Parameters
    ----------
    uri : str
        The URI of the fuel artifact (typically a model). This matches the URI
        used in SDFormat's include tags.

    Returns
    -------
    info : Metadata
        A python dict of metadata.

    Notes
    -----
    The function caches the most recent 100 calls in an effort to ease the
    burden on the Fuel servers and to improve performance. To manually reset
    this cache call ``ropy.ignition.fuel.metadata_cache.clear()``. You can
    further also this behavior by changing ``ropy.ignition.fuel.metadata_cache``
    to a different cache instance. Check the `cachetools docs
    <https://cachetools.readthedocs.io/en/stable/#>`_ for more information.
    """

    result = requests.get(uri, headers={"accept": "application/json"})
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
    this cache call ``ropy.ignition.fuel.download_cache.clear()``. You can
    further also this behavior by changing ``ropy.ignition.fuel.download_cache``
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
    user_cache: Callable[[str], Union[str, None]] = None,
    use_internal_cache: bool = True,
    use_file_cache: bool = True,
    update_file_cache: bool = True,
    update_internal_cache: bool = True,
    update_user_cache: Callable[[str, str], None] = None,
    file_cache_dir: str = "~/.ignition/fuel",
) -> str:
    """Get the primary SDF of a model from the Fuel server.

    Parameters
    ----------
    url : str
        The URL of the model. This is the same as the URL used for
        include elements in SDF files.
    user_cache : Callable[[str], Union[str, None]]
        User supplied caching logic. It is a callable that expects a string (the
        url) and returns either a string (the sdf) or None. If user_cache
        returns a string, that string is returned; if user_cache returns None
        this is interpreted as a cache miss. If ``user_cache is None`` it always
        misses.
    use_internal_cache : bool
        If True (default), use ropy's internal cache. This is a module-level
        in-memory cache located at ropy.ignition.fuel.memcache. Models are
        evicted after 24 hours, or when ropy is unloaded. If False, the
        internal_cache always misses.
    use_file_cache : bool
        If True (default), check the local filesystem for a copy of the model.
    update_file_cache : str
        If not None, update the file cache the the given location if file_cache misses.
        The default is ``~/.igition/fuel``, which is the default location for ignition.
    update_internal_cache : bool
        If True (default) update the internal cache if it missed.
    update_user_cache : Callable[[str, str], None]
        If not None and user_cache missed, update_user_cache is called with the
        signature ``update_user_cache(url, sdf_string)``. The expected behavior
        is that this call will update the user supplied caching mechanism.
    file_cache_dir : str
        The folder to use for the file cache. It follows the same layout as ignition's
        fuel-tools; see the Notes for more information. The default is
        ``~/.ignition/fuel``, which is the default location for ignition. If
        ``file_cache is None`` it always misses.


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

    You can manually reset the internal cache by calling
    ``ropy.ignition.fuel.model_cache.clear()``.

    The file_cache stores models on your local filesystem. It never evicts, so
    you should manually delete outdated models. The format of the cache
    is::

        file_cache_dir/fuel.ignitionrobotics.org/{owner}/models/{model_name}/{version}



    """

    def cache(get_fn: Optional[Callable], update_fn: Optional[Callable]):
        def decorator(download_sdf: Callable):
            def inner(url):
                sdf_string = None

                if get_fn:
                    sdf_string = get_fn(url)

                if sdf_string is None:
                    sdf_string = download_sdf(url)

                    if update_fn is not None:
                        update_fn(url, sdf_string)

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
    def _fetch_online(url: str) -> str:
        """Download the model and extract primary SDF"""
        blob = download_fuel_model(url)
        with ZipFile(BytesIO(blob)) as model_file:
            with model_file.open("model.sdf", "r") as sdf_file:
                sdf_string = sdf_file.read().decode("utf-8")

        return sdf_string

    return _fetch_online(url)