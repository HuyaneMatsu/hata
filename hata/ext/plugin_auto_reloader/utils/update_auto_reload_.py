__all__ = ('update_auto_reload',)

from scarletio import copy_docs

from ..plugin_auto_reloader import PLUGIN_AUTO_RELOADER_MANAGER, PluginAutoReloaderManager


@copy_docs(PluginAutoReloaderManager.update)
def update_auto_reload():
    return PLUGIN_AUTO_RELOADER_MANAGER.update()
