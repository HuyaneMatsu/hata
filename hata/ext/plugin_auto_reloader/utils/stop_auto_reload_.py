__all__ = ('stop_auto_reload',)

from scarletio import copy_docs

from ..plugin_auto_reloader import PLUGIN_AUTO_RELOADER_MANAGER, PluginAutoReloaderManager


@copy_docs(PluginAutoReloaderManager.stop)
def stop_auto_reload():
    return PLUGIN_AUTO_RELOADER_MANAGER.stop()
