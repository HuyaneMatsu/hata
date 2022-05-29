__all__ = ('PLUGINS',)

from scarletio import WeakValueDictionary


PLUGINS = WeakValueDictionary()

PLUGIN_STATE_UNDEFINED = 0
PLUGIN_STATE_LOADED = 1
PLUGIN_STATE_UNLOADED = 2
PLUGIN_STATE_UNSATISFIED = 3

PLUGIN_STATE_VALUE_TO_NAME = {
    PLUGIN_STATE_UNDEFINED: 'undefined',
    PLUGIN_STATE_LOADED: 'loaded',
    PLUGIN_STATE_UNLOADED: 'unloaded',
    PLUGIN_STATE_UNSATISFIED: 'unsatisfied',
}

LOADING_PLUGINS = set()

# Plugin roots define core part for plugins.
PLUGIN_ROOTS = set()


ABSOLUTE_PATH_PLUGIN_NAME_PREFIX = '<extension>.'
