__all__ = ('reload_all_plugin',)

from scarletio import copy_docs

from ..plugin_loader import PLUGIN_LOADER


@copy_docs(PLUGIN_LOADER.load)
def reload_all_plugin(*, blocking=True):
    return PLUGIN_LOADER.reload_all(blocking=blocking)
