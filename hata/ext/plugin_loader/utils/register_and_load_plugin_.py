__all__ = ('register_and_load_plugin',)

from scarletio import copy_docs

from ..plugin_loader import PLUGIN_LOADER


@copy_docs(PLUGIN_LOADER.register_and_load)
def register_and_load_plugin(name, *parameters, blocking = True, **keyword_parameters):
    return PLUGIN_LOADER.register_and_load(name, *parameters, blocking = blocking, **keyword_parameters)
