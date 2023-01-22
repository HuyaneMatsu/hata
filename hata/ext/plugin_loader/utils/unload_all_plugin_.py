__all__ = ('unload_all_plugin',)

from scarletio import copy_docs

from ..plugin_loader import PLUGIN_LOADER


@copy_docs(PLUGIN_LOADER.load)
def unload_all_plugin(*, blocking = True):
    return PLUGIN_LOADER.unload_all(blocking = blocking)
