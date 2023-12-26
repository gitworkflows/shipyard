import abc
import logging
import os

import click
from plugin import Plugin, PluginManager

LOG = logging.getLogger(__name__)


class ShipyardCli:
    group: click.Group

    def __call__(self, *args, **kwargs):
        self.group(*args, **kwargs)


class ShipyardCliPlugin(Plugin):
    namespace = "shipyard.plugins.cli"

    def load(self, cli) -> None:
        self.attach(cli)

    @abc.abstractmethod
    def attach(self, cli: ShipyardCli) -> None:
        """
        Attach commands to the `shipyard` CLI.

        :param cli: the cli object
        """


def load_cli_plugins(cli):
    if os.environ.get("DEBUG_PLUGINS", "0").lower() in ("true", "1"):
        # importing shipyard.config is still quite expensive...
        logging.basicConfig(level=logging.DEBUG)

    loader = PluginManager("shipyard.plugins.cli", load_args=(cli,))
    loader.load_all()
