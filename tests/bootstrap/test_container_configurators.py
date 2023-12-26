import textwrap

import requests

from shipyard.utils.bootstrap import (
    Container,
    ContainerConfigurators,
    configure_container,
    get_gateway_url,
)
from shipyard.utils.common import external_service_ports
from shipyard.utils.container_utils.container_client import VolumeBind


def test_common_container_fixture_configurators(
    container_factory, wait_for_shipyard_ready, tmp_path
):
    volume = tmp_path / "shipyard-volume"
    volume.mkdir(parents=True)

    container: Container = container_factory(
        configurators=[
            ContainerConfigurators.random_container_name,
            ContainerConfigurators.random_gateway_port,
            ContainerConfigurators.random_service_port_range(20),
            ContainerConfigurators.debug,
            ContainerConfigurators.mount_docker_socket,
            ContainerConfigurators.mount_shipyard_volume(volume),
            ContainerConfigurators.env_vars(
                {
                    "FOOBAR": "foobar",
                    "MY_TEST_ENV": "test",
                }
            ),
        ]
    )

    running_container = container.start()
    wait_for_shipyard_ready(running_container)
    url = get_gateway_url(container)

    # port was exposed correctly
    response = requests.get(f"{url}/_shipyard/health")
    assert response.ok

    # volume was mounted and directories were created correctly
    assert (volume / "cache" / "machine.json").exists()

    inspect = running_container.inspect()
    # volume was mounted correctly
    assert {
        "Type": "bind",
        "Source": str(volume),
        "Destination": "/var/lib/shipyard",
        "Mode": "",
        "RW": True,
        "Propagation": "rprivate",
    } in inspect["Mounts"]
    # docker socket was mounted correctly
    assert {
        "Type": "bind",
        "Source": "/var/run/docker.sock",
        "Destination": "/var/run/docker.sock",
        "Mode": "",
        "RW": True,
        "Propagation": "rprivate",
    } in inspect["Mounts"]

    # debug was set
    assert "DEBUG=1" in inspect["Config"]["Env"]
    # environment variables were set
    assert "FOOBAR=foobar" in inspect["Config"]["Env"]
    assert "MY_TEST_ENV=test" in inspect["Config"]["Env"]
    # container name was set
    assert f"MAIN_CONTAINER_NAME={container.config.name}" in inspect["Config"]["Env"]


def test_custom_command_configurator(container_factory, tmp_path, stream_container_logs):
    tmp_dir = tmp_path

    script = tmp_dir / "my-command.sh"
    script.write_text(
        textwrap.dedent(
            """
            #!/bin/bash
            echo "foobar"
            echo "$@"
            """
        ).strip()
    )
    script.chmod(0o777)

    container: Container = container_factory(
        configurators=[
            ContainerConfigurators.random_container_name,
            ContainerConfigurators.custom_command(
                ["/tmp/pytest-tmp-path/my-command.sh", "hello", "world"]
            ),
            ContainerConfigurators.volume(VolumeBind(str(tmp_path), "/tmp/pytest-tmp-path")),
        ],
        remove=False,
    )

    running_container = container.start()
    assert running_container.wait_until_ready(timeout=5)
    assert running_container.get_logs().strip() == "foobar\nhello world"


def test_default_shipyard_container_configurator(
    container_factory, wait_for_shipyard_ready, tmp_path, monkeypatch, stream_container_logs
):
    volume = tmp_path / "shipyard-volume"
    volume.mkdir(parents=True)

    # overwrite a few config variables
    from shipyard import config

    monkeypatch.setenv("DEBUG", "1")
    monkeypatch.setenv("SHIPYARD_API_KEY", "")
    monkeypatch.setenv("ACTIVATE_PRO", "0")
    monkeypatch.setattr(config, "DEBUG", True)
    monkeypatch.setattr(config, "VOLUME_DIR", str(volume))
    monkeypatch.setattr(config, "DOCKER_FLAGS", "-p 23456:4566 -e MY_TEST_VAR=foobar")

    container: Container = container_factory()
    configure_container(container)

    stream_container_logs(container)
    wait_for_shipyard_ready(container.start())

    # check startup works correctly
    response = requests.get("http://localhost:4566/_shipyard/health")
    assert response.ok

    # check docker-flags was created correctly
    response = requests.get("http://localhost:23456/_shipyard/health")
    assert response.ok, "couldn't reach shipyard on port 23456 - does DOCKER_FLAGS work?"

    response = requests.get("http://localhost:4566/_shipyard/diagnose")
    assert response.ok, "couldn't reach diagnose endpoint. is DEBUG=1 set?"
    diagnose = response.json()

    # a few smoke tests of important configs
    assert diagnose["config"]["GATEWAY_LISTEN"] == ["0.0.0.0:4566"]
    # check that docker-socket was mounted correctly
    assert diagnose["docker-inspect"], "was the docker socket mounted?"
    assert diagnose["docker-inspect"]["Config"]["Image"] == "khulnasoft/shipyard"
    assert diagnose["docker-inspect"]["Path"] == "docker-entrypoint.sh"
    assert {
        "Type": "bind",
        "Source": str(volume),
        "Destination": "/var/lib/shipyard",
        "Mode": "",
        "RW": True,
        "Propagation": "rprivate",
    } in diagnose["docker-inspect"]["Mounts"]

    # from DOCKER_FLAGS
    assert "MY_TEST_VAR=foobar" in diagnose["docker-inspect"]["Config"]["Env"]

    # check that external service ports were mapped correctly
    ports = diagnose["docker-inspect"]["NetworkSettings"]["Ports"]
    for port in external_service_ports:
        assert ports[f"{port}/tcp"] == [{"HostIp": "127.0.0.1", "HostPort": f"{port}"}]
