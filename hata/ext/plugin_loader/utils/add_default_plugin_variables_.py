__all__ = ('remove_default_plugin_variables',)

from scarletio import copy_docs

from ..plugin_loader import PLUGIN_LOADER


@copy_docs(PLUGIN_LOADER.remove_default_variables)
def remove_default_plugin_variables(*names):
    return PLUGIN_LOADER.remove_default_variables(*names)
