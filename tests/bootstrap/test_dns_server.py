import logging

import pytest

from shipyard import constants
from shipyard.config import in_docker
from shipyard.constants import LOCALHOST_HOSTNAME
from shipyard.testing.pytest.container import ContainerFactory
from shipyard.utils.bootstrap import ContainerConfigurators
from shipyard.utils.strings import short_uid

LOG = logging.getLogger(__name__)

pytestmarks = pytest.mark.skipif(
    condition=in_docker(), reason="cannot run bootstrap tests in docker"
)


def test_default_network(
    container_factory: ContainerFactory,
    stream_container_logs,
    wait_for_shipyard_ready,
    dns_query_from_container,
):
    ls_container = container_factory(
        configurators=[
            ContainerConfigurators.debug,
            ContainerConfigurators.mount_docker_socket,
        ]
    )
    running_container = ls_container.start()
    stream_container_logs(ls_container)
    wait_for_shipyard_ready(running_container)

    container_ip = running_container.ip_address()

    stdout, _ = dns_query_from_container(name=LOCALHOST_HOSTNAME, ip_address=container_ip)
    assert container_ip in stdout.decode().splitlines()

    stdout, _ = dns_query_from_container(name=f"foo.{LOCALHOST_HOSTNAME}", ip_address=container_ip)
    assert container_ip in stdout.decode().splitlines()


def test_user_defined_network(
    docker_network,
    container_factory: ContainerFactory,
    stream_container_logs,
    wait_for_shipyard_ready,
    dns_query_from_container,
):
    ls_container = container_factory(
        configurators=[
            ContainerConfigurators.debug,
            ContainerConfigurators.mount_docker_socket,
            ContainerConfigurators.network(docker_network),
        ]
    )
    running_ls_container = ls_container.start()
    stream_container_logs(ls_container)
    wait_for_shipyard_ready(running_ls_container)

    container_ip = running_ls_container.ip_address(docker_network=docker_network)
    stdout, _ = dns_query_from_container(
        name=LOCALHOST_HOSTNAME, ip_address=container_ip, network=docker_network
    )
    assert container_ip in stdout.decode().splitlines()

    stdout, _ = dns_query_from_container(
        name=f"foo.{LOCALHOST_HOSTNAME}", ip_address=container_ip, network=docker_network
    )
    assert container_ip in stdout.decode().splitlines()


def test_skip_pattern(
    docker_network,
    container_factory: ContainerFactory,
    stream_container_logs,
    wait_for_shipyard_ready,
    dns_query_from_container,
):
    """
    Add a skip pattern of localhost.shipyard.khulnasoft.com to ensure that we prioritise skips before
    local name resolution
    """
    ls_container = container_factory(
        configurators=[
            ContainerConfigurators.debug,
            ContainerConfigurators.mount_docker_socket,
            ContainerConfigurators.network(docker_network),
            ContainerConfigurators.env_vars(
                {
                    "DNS_NAME_PATTERNS_TO_RESOLVE_UPSTREAM": r".*localhost.shipyard.khulnasoft.com",
                }
            ),
        ]
    )
    running_ls_container = ls_container.start()
    stream_container_logs(ls_container)
    wait_for_shipyard_ready(running_ls_container)

    container_ip = running_ls_container.ip_address(docker_network=docker_network)
    stdout, _ = dns_query_from_container(
        name=LOCALHOST_HOSTNAME, ip_address=container_ip, network=docker_network
    )
    assert container_ip not in stdout.decode().splitlines()
    assert constants.LOCALHOST_IP in stdout.decode().splitlines()

    stdout, _ = dns_query_from_container(
        name=f"foo.{LOCALHOST_HOSTNAME}", ip_address=container_ip, network=docker_network
    )
    assert container_ip not in stdout.decode().splitlines()
    assert constants.LOCALHOST_IP in stdout.decode().splitlines()


def test_resolve_shipyard_host(
    container_factory: ContainerFactory,
    stream_container_logs,
    wait_for_shipyard_ready,
    dns_query_from_container,
):
    shipyard_host = f"host-{short_uid()}"
    ls_container = container_factory(
        configurators=[
            ContainerConfigurators.debug,
            ContainerConfigurators.mount_docker_socket,
            ContainerConfigurators.env_vars(
                {
                    "SHIPYARD_HOST": shipyard_host,
                },
            ),
        ],
    )
    running_container = ls_container.start()
    stream_container_logs(ls_container)
    wait_for_shipyard_ready(running_container)

    container_ip = running_container.ip_address()

    stdout, _ = dns_query_from_container(name=LOCALHOST_HOSTNAME, ip_address=container_ip)
    assert container_ip in stdout.decode().splitlines()

    stdout, _ = dns_query_from_container(name=f"foo.{LOCALHOST_HOSTNAME}", ip_address=container_ip)
    assert container_ip in stdout.decode().splitlines()

    stdout, _ = dns_query_from_container(name=shipyard_host, ip_address=container_ip)
    assert container_ip in stdout.decode().splitlines()

    stdout, _ = dns_query_from_container(name=f"foo.{shipyard_host}", ip_address=container_ip)
    assert container_ip in stdout.decode().splitlines()
