"""Diagnostic tool for a shipyard instance running in a container."""
import inspect
import os
import socket
from typing import Dict, List, Union

from shipyard import config
from shipyard.constants import DEFAULT_VOLUME_DIR
from shipyard.services.lambda_.invocation.docker_runtime_executor import IMAGE_PREFIX
from shipyard.services.lambda_.runtimes import IMAGE_MAPPING
from shipyard.utils import bootstrap
from shipyard.utils.analytics import usage
from shipyard.utils.container_networking import get_main_container_name
from shipyard.utils.container_utils.container_client import NoSuchImage
from shipyard.utils.docker_utils import DOCKER_CLIENT
from shipyard.utils.files import load_file

LAMBDA_IMAGES = (f"{IMAGE_PREFIX}{postfix}" for postfix in IMAGE_MAPPING.values())


DIAGNOSE_IMAGES = [
    "shipyard/bigdata",
    "mongo",
    *LAMBDA_IMAGES,
]

EXCLUDE_CONFIG_KEYS = {
    "CONFIG_ENV_VARS",
    "copyright",
    "__builtins__",
    "__cached__",
    "__doc__",
    "__file__",
    "__loader__",
    "__name__",
    "__package__",
    "__spec__",
}
ENDPOINT_RESOLVE_LIST = ["localhost.shipyard.khulnasoft.com", "api.shipyard.khulnasoft.com"]
INSPECT_DIRECTORIES = [DEFAULT_VOLUME_DIR, "/tmp"]


def get_shipyard_logs() -> Dict:
    try:
        result = DOCKER_CLIENT.get_container_logs(get_main_container_name())
    except Exception as e:
        result = f"error getting docker logs for container: {e}"

    return {"docker": result}


def get_shipyard_config() -> Dict:
    result = {}
    for k, v in inspect.getmembers(config):
        if k in EXCLUDE_CONFIG_KEYS:
            continue
        if inspect.isbuiltin(v):
            continue
        if inspect.isfunction(v):
            continue
        if inspect.ismodule(v):
            continue
        if inspect.isclass(v):
            continue
        if "typing." in str(type(v)):
            continue
        if k == "GATEWAY_LISTEN":
            result[k] = config.GATEWAY_LISTEN
            continue

        if hasattr(v, "__dict__"):
            result[k] = v.__dict__
        else:
            result[k] = v

    return result


def inspect_main_container() -> Union[str, Dict]:
    try:
        return DOCKER_CLIENT.inspect_container(get_main_container_name())
    except Exception as e:
        return f"inspect failed: {e}"


def get_shipyard_version() -> Dict[str, str]:
    return {
        "build-date": os.environ.get("SHIPYARD_BUILD_DATE"),
        "build-git-hash": os.environ.get("SHIPYARD_BUILD_GIT_HASH"),
        "build-version": os.environ.get("SHIPYARD_BUILD_VERSION"),
    }


def resolve_endpoints() -> Dict[str, str]:
    result = {}
    for endpoint in ENDPOINT_RESOLVE_LIST:
        try:
            resolved_endpoint = socket.gethostbyname(endpoint)
        except Exception as e:
            resolved_endpoint = f"unable_to_resolve {e}"
        result[endpoint] = resolved_endpoint
    return result


def get_important_image_hashes() -> Dict[str, str]:
    result = {}
    for image in DIAGNOSE_IMAGES:
        try:
            image_version = DOCKER_CLIENT.inspect_image(image, pull=False)["RepoDigests"]
        except NoSuchImage:
            image_version = "not_present"
        except Exception as e:
            image_version = f"error: {e}"
        result[image] = image_version
    return result


def get_service_stats() -> Dict[str, str]:
    from shipyard.services.plugins import SERVICE_PLUGINS

    return {service: state.value for service, state in SERVICE_PLUGINS.get_states().items()}


def get_file_tree() -> Dict[str, List[str]]:
    return {d: traverse_file_tree(d) for d in INSPECT_DIRECTORIES}


def traverse_file_tree(root: str) -> List[str]:
    try:
        result = []
        if config.in_docker():
            for root, _, _ in os.walk(root):
                result.append(root)
        return result
    except Exception as e:
        return ["traversing files failed %s" % e]


def get_docker_image_details() -> Dict[str, str]:
    return bootstrap.get_docker_image_details()


def get_host_kernel_version() -> str:
    return load_file("/proc/version", "failed").strip()


def get_usage():
    return usage.aggregate()
