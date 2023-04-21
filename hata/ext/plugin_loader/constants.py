__all__ = ('PLUGINS',)

import re
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


IGNORED_DIRECTORY_NAMES = frozenset((
    '__pycache__',
    'tests',
))


ABSOLUTE_PATH_PLUGIN_NAME_PREFIX = '<unknown>.'

IN_DIRECTORY_PLUGIN_RP = re.compile('\\.[^.]+')


PLUGIN_ACTION_FLAG_NONE = 0
PLUGIN_ACTION_FLAG_LOAD = 1 << 0
PLUGIN_ACTION_FLAG_UNLOAD = 1 << 1
PLUGIN_ACTION_FLAG_NAME_LOOKUP = 1 << 2
PLUGIN_ACTION_FLAG_SYNTAX_CHECK = 1 << 3
PLUGIN_ACTION_FLAG_UNLINK = 1 << 4
