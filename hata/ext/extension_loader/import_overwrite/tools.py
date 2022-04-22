__all__ = ()

import sys

from .extension_finder import ExtensionFinder


def set_spec_finder():
    """
    Sets``ExtensionFinder`` into `sys.meta_path`. If it is already set, replaces it.
    """
    meta_path = getattr(sys, 'meta_path', None)
    if (meta_path is None) or (not isinstance(meta_path, list)):
        sys.meta_path = meta_path = []
    
    for index in range(len(meta_path)):
        path_finder = meta_path[index]
        if type(path_finder).__name__ == ExtensionFinder.__name__:
            break
    
    else:
        index = -1
    
    extension_finder = ExtensionFinder()
    
    if index == -1:
        meta_path.insert(0, extension_finder)
    else:
        meta_path[index] = extension_finder
