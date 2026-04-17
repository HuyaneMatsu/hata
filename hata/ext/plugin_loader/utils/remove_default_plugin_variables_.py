__all__ = ('add_default_plugin_variables',)

from scarletio import copy_docs

from ..plugin_loader import PLUGIN_LOADER


@copy_docs(PLUGIN_LOADER.add_default_variables)
def add_default_plugin_variables(**variables):
    return PLUGIN_LOADER.add_default_variables(**variables)
