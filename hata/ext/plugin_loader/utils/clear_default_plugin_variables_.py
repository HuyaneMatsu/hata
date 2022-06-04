__all__ = ('clear_default_plugin_variables',)

from scarletio import copy_docs

from ..plugin_loader import PLUGIN_LOADER


@copy_docs(PLUGIN_LOADER.clear_default_variables)
def clear_default_plugin_variables():
    return PLUGIN_LOADER.clear_default_variables()
