from typing import Optional

from shipyard import config
from shipyard.config import HostAndPort


def path_from_url(url: str) -> str:
    return f'/{url.partition("://")[2].partition("/")[2]}' if "://" in url else url


def hostname_from_url(url: str) -> str:
    return url.split("://")[-1].split("/")[0].split(":")[0]


def shipyard_host(custom_port: Optional[int] = None) -> HostAndPort:
    """
    Determine the host and port to return to the user based on:
    - the user's configuration (e.g environment variable overrides)
    - the defaults of the system
    """
    port = custom_port or config.SHIPYARD_HOST.port
    host = config.SHIPYARD_HOST.host
    return HostAndPort(host=host, port=port)
