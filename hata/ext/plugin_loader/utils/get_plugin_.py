__all__ = ('get_plugin',)

from scarletio import copy_docs

from ..plugin_loader import PLUGIN_LOADER


@copy_docs(PLUGIN_LOADER.get_plugin)
def get_plugin(name):
    return PLUGIN_LOADER.get_plugin(name)
