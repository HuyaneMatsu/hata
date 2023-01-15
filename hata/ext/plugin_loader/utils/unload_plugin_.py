__all__ = ('unload_plugin',)

from scarletio import copy_docs

from ..plugin_loader import PLUGIN_LOADER


@copy_docs(PLUGIN_LOADER.unload)
def unload_plugin(name, *, blocking = True, deep = True):
    return PLUGIN_LOADER.unload(name, blocking = blocking, deep = deep)
