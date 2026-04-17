__all__ = ()

import sys
from os import listdir as list_directory
from os.path import join as join_paths, isdir as is_directory, exists

from ..plugin_loader.constants import IGNORED_DIRECTORY_NAMES, PLUGIN_ROOTS


def _iter_sub_directories(directories):
    """
    Iterates over the sub directories of the given ones.
    
    Parameters
    ----------
    directories : `iterable` of `str`
        Directories to look sub directories for in. These directories are also yielded.
    
    Yields
    ------
    directory : `str`
    """
    directories = [*directories]
    
    while directories:
        directory = directories.pop()
        yield directory
        
        for name in list_directory(directory):
            if name in IGNORED_DIRECTORY_NAMES:
                continue
            
            path = join_paths(directory, name)
            if not is_directory(path):
                continue
            
            directories.append(path)
            continue


def _iter_plugin_root_paths():
    """
    Iterates over the plugin root paths.
    
    This function is an iterable generator.
    
    Yields
    ------
    directory : `str`
    """
    for plugin_root in PLUGIN_ROOTS:
        for path_base in sys.path:
            path = join_paths(path_base, *plugin_root)
            if exists(path):
                yield path
                break
