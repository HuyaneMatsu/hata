__all__ = ()

import warnings

from scarletio import KeepType

from ...discord.client import Client

from .plugin import PLUGINS, PLUGIN_STATE_LOADED


@KeepType(Client)
class Client:
    
    @property
    def extensions(self):
        """
        Drops a deprecation warning and returns ``.plugins``.
        """
        warnings.warn(
            (
                f'`{self!r}.extensions` is deprecated and will be removed in 2022 December. '
                f'Please use `.plugins` instead.'
            ),
            FutureWarning,
            stacklevel = 2
        )
        return self.plugins
    
    
    @property
    def plugins(self):
        """
        Returns a list of plugins added to the client. Added by the `plugin_loader` plugin.
        
        Returns
        -------
        plugins : `list` of ``Plugin``
        """
        plugins = []
        for plugin in PLUGINS.values():
            if plugin._state == PLUGIN_STATE_LOADED:
                snapshot_difference = plugin._snapshot_difference
                if (snapshot_difference is not None):
                    for snapshot in snapshot_difference:
                        if (snapshot.client is self) and snapshot_difference:
                            plugins.append(plugin)
                            break
        
        return plugins
