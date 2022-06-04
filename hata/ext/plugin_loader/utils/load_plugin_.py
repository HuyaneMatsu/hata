__all__ = ('load_plugin',)

from scarletio import copy_docs

from ..plugin_loader import PLUGIN_LOADER


@copy_docs(PLUGIN_LOADER.load)
def load_plugin(name, *, blocking=True, deep=True):
    return PLUGIN_LOADER.load(name, blocking=blocking, deep=deep)
