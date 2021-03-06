import pkg_resources
from typing import (
    Tuple,
)

from trinity.extensibility import (
    BasePlugin,
)
from trinity.plugins.builtin.attach.plugin import (
    AttachPlugin
)
from trinity.plugins.builtin.ethstats.plugin import (
    EthstatsPlugin,
)
from trinity.plugins.builtin.fix_unclean_shutdown.plugin import (
    FixUncleanShutdownPlugin
)
from trinity.plugins.builtin.json_rpc.plugin import (
    JsonRpcServerPlugin,
)
from trinity.plugins.builtin.tx_pool.plugin import (
    TxPlugin,
)
from trinity.plugins.builtin.light_peer_chain_bridge.plugin import (
    LightPeerChainBridgePlugin
)


def is_ipython_available() -> bool:
    try:
        pkg_resources.get_distribution('IPython')
    except pkg_resources.DistributionNotFound:
        return False
    else:
        return True


BUILTIN_PLUGINS = (
    AttachPlugin() if is_ipython_available() else AttachPlugin(use_ipython=False),
    EthstatsPlugin(),
    FixUncleanShutdownPlugin(),
    JsonRpcServerPlugin(),
    LightPeerChainBridgePlugin(),
    TxPlugin(),
)


def discover_plugins() -> Tuple[BasePlugin, ...]:
    # Plugins need to define entrypoints at 'trinity.plugins' to automatically get loaded
    # https://packaging.python.org/guides/creating-and-discovering-plugins/#using-package-metadata

    return tuple(
        entry_point.load()() for entry_point in pkg_resources.iter_entry_points('trinity.plugins')
    )


def get_all_plugins() -> Tuple[BasePlugin, ...]:
    return BUILTIN_PLUGINS + discover_plugins()
