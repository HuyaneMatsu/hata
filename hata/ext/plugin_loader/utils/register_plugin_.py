__all__ = ('register_plugin',)

from scarletio import copy_docs

from ..plugin_loader import PLUGIN_LOADER


@copy_docs(PLUGIN_LOADER.register)
def register_plugin(name, *positional_parameters, **keyword_parameters):
    return PLUGIN_LOADER.register(name, *positional_parameters, **keyword_parameters)
