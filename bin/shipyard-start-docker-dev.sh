#!/usr/bin/env bash

source ${VENV_DIR=.venv}/bin/activate

export SHIPYARD_VOLUME_DIR=$(pwd)/.filesystem/var/lib/shipyard
export DOCKER_FLAGS="${DOCKER_FLAGS}
-v $(pwd)/shipyard:/opt/code/khulnasoft/shipyard
-v $(pwd)/shipyard_core.egg-info:/opt/code/khulnasoft/shipyard_core.egg-info
-v $(pwd)/.filesystem/etc/shipyard:/etc/shipyard
-v $(pwd)/bin/shipyard-supervisor:/opt/code/shipyard/bin/shipyard-supervisor
-v $(pwd)/bin/docker-entrypoint.sh:/usr/local/bin/docker-entrypoint.sh"

exec python -m shipyard.cli.main start "$@"
