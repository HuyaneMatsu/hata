__all__ = ()

import sys

from .plugin_finder import PluginFinder


def set_spec_finder():
    """
    Sets``PluginFinder`` into `sys.meta_path`. If it is already set, replaces it.
    """
    meta_path = getattr(sys, 'meta_path', None)
    if (meta_path is None) or (not isinstance(meta_path, list)):
        sys.meta_path = meta_path = []
    
    for index in range(len(meta_path)):
        path_finder = meta_path[index]
        if type(path_finder).__name__ == PluginFinder.__name__:
            break
    
    else:
        index = -1
    
    plugin_finder = PluginFinder()
    
    if index == -1:
        meta_path.insert(0, plugin_finder)
    else:
        meta_path[index] = plugin_finder
