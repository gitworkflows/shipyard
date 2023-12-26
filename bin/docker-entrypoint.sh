#!/bin/bash

set -eo pipefail
shopt -s nullglob

# the Dockerfile creates .pro-version file for the pro image and .bigdata-pro-version for the bigdata image.
# When trying to activate pro features with any other version, a warning is printed.
if [[ $SHIPYARD_API_KEY ]] && ! compgen -G /usr/lib/shipyard/.*pro-version >/dev/null; then
    echo "WARNING"
    echo "============================================================================"
    echo "  It seems you are trying to use the Shipyard Pro version without using "
    echo "  the dedicated Pro image."
    echo "  Shipyard will only start with community services enabled."
    echo "  To fix this warning, use khulnasoft/shipyard-pro instead."
    echo ""
    echo "  See: https://github.com/khulnasoft/shipyard/issues/7882"
    echo "============================================================================"
    echo ""
fi

# Strip `SHIPYARD_` prefix in environment variables name; except SHIPYARD_HOST and SHIPYARD_HOSTNAME (deprecated)
source <(
  env |
  grep -v -e '^SHIPYARD_HOSTNAME' |
  grep -v -e '^SHIPYARD_HOST' |
  grep -v -e '^SHIPYARD_[[:digit:]]' | # See issue #1387
  sed -ne 's/^SHIPYARD_\([^=]\+\)=.*/export \1=${SHIPYARD_\1}/p'
)

LOG_DIR=/var/lib/shipyard/logs
test -d ${LOG_DIR} || mkdir -p ${LOG_DIR}

# activate the virtual environment
source /opt/code/shipyard/.venv/bin/activate

# run runtime init hooks BOOT stage before starting shipyard
test -d /etc/shipyard/init/boot.d && python3 -m shipyard.runtime.init BOOT

# run the shipyard supervisor. it's important to run with `exec` and don't use pipes so signals are handled correctly
exec shipyard-supervisor
