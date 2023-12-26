"""This is the entrypoint used to start the shipyard runtime. It starts the infrastructure and also
manages the interaction with the operating system - mostly signal handlers for now."""
import signal
import sys

from shipyard.runtime.exceptions import ShipyardExit


def main():
    from shipyard.services import infra

    # signal handler to make sure SIGTERM properly shuts down shipyard
    def _terminate_shipyard(sig: int, frame):
        infra.exit_infra(0)

    # SIGINT is currently managed implicitly in start_infra via `except KeyboardInterrupt`
    signal.signal(signal.SIGTERM, _terminate_shipyard)

    try:
        infra.start_infra(asynchronous=False)
    except ShipyardExit as e:
        sys.exit(e.code)

    sys.exit(infra.EXIT_CODE.get())


if __name__ == "__main__":
    main()
