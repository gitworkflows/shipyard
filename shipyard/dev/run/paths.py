"""Utilities to resolve important paths on the host and in the container."""
import os
from pathlib import Path
from typing import Optional, Union


class HostPaths:
    workspace_dir: Path
    """We assume all repositories live in a workspace directory, e.g., ``~/workspace/ls/shipyard``,
    ``~/workspace/ls/shipyard-ext``, ..."""

    shipyard_project_dir: Path
    shipyard_ext_project_dir: Path
    moto_project_dir: Path
    volume_dir: Path
    venv_dir: Path

    def __init__(
        self,
        workspace_dir: Union[os.PathLike, str] = None,
        volume_dir: Union[os.PathLike, str] = None,
        venv_dir: Union[os.PathLike, str] = None,
    ):
        self.workspace_dir = Path(workspace_dir or os.path.abspath(os.path.join(os.getcwd(), "..")))
        self.shipyard_project_dir = self.workspace_dir / "shipyard"
        self.shipyard_ext_project_dir = self.workspace_dir / "shipyard-ext"
        self.moto_project_dir = self.workspace_dir / "moto"
        self.postgresql_proxy = self.workspace_dir / "postgresql-proxy"
        self.volume_dir = Path(volume_dir or "/tmp/shipyard")
        self.venv_dir = Path(
            venv_dir
            or os.getenv("VIRTUAL_ENV")
            or os.getenv("VENV_DIR")
            or os.path.join(os.getcwd(), ".venv")
        )


class ContainerPaths:
    """Important paths in the container"""

    project_dir: str = "/opt/code/shipyard"
    site_packages_target_dir: str = "/opt/code/shipyard/.venv/lib/python3.11/site-packages"
    docker_entrypoint: str = "/usr/local/bin/docker-entrypoint.sh"
    shipyard_supervisor: str = "/usr/local/bin/shipyard-supervisor"
    shipyard_source_dir: str
    shipyard_ext_source_dir: Optional[str]

    def dependency_source(self, name: str) -> str:
        """Returns path of the given source dependency in the site-packages directory."""
        return self.site_packages_target_dir + f"/{name}"


class CommunityContainerPaths(ContainerPaths):
    """In the community image, code is copied into /opt/code/shipyard"""

    def __init__(self):
        self.shipyard_source_dir = f"{self.project_dir}/shipyard"


class ProContainerPaths(ContainerPaths):
    """In the pro image, shipyard and ext are installed into the venv as dependency"""

    def __init__(self):
        self.shipyard_source_dir = self.dependency_source("shipyard")
        self.shipyard_ext_source_dir = self.dependency_source("shipyard_ext")
