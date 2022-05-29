__all__ = ('reload_plugin',)

from scarletio import copy_docs

from ..plugin_loader import PLUGIN_LOADER


@copy_docs(PLUGIN_LOADER.reload)
def reload_plugin(name, *, blocking=True, deep=True):
    return PLUGIN_LOADER.reload(name, blocking=blocking, deep=deep)
