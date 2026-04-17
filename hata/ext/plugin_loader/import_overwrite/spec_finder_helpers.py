__all__ = ()

import sys
from importlib.util import spec_from_file_location
from os.path import (
    exists, isdir as is_directory, isfile as is_file, join as join_paths, sep as PATH_SEPARATOR, split as split_path
)


def create_spec_if_exists(full_name, path):
    """
    Creates module spec if the path exists.
    
    Parameters
    ----------
    full_name : `str`
        The full name of the module to find.
    path : `str`
        A path to check whether it represents a python file / directory with `__init__.py`.
    
    Returns
    -------
    spec : `None`, `ModuleSpec`
    """
    if is_directory(path):
        path = join_paths(path, '__init__.py')
        if exists(path):
            return spec_from_file_location(full_name, path)
        
        return None
    
    path += '.py'
    
    if exists(path) and is_file(path):
        return spec_from_file_location(full_name, path)
    
    return None


def try_find_spec_in_system_paths(full_name, full_name_parts, path):
    """
    Tries to the find the spec in the given path. uses `sys.path` to default to when doing so.
    
    Parameters
    ----------
    full_name : `str`
        The full name of the module to find.
    full_name_parts : `list` of `str`
        `full_name` separated by `'.'`.
    path : `str`
        Path to find the module in.
    
    Returns
    -------
    spec : `None`, `ModuleSpec`
    """
    for system_path in sys.path:
        if system_path.endswith(PATH_SEPARATOR):
            compare_system_path = system_path
        else:
            compare_system_path = system_path + PATH_SEPARATOR
        
        if not path.startswith(compare_system_path):
            continue
        
        spec = create_spec_if_exists(full_name, join_paths(system_path, *full_name_parts))
        if (spec is not None):
            return spec
    
    return None


def try_find_spec_in_path_fallback(full_name, full_name_parts, path):
    """
    Tries to the find the spec in the given path.
    
    This is a fallback function and only called if every other way fails.
    
    Parameters
    ----------
    full_name : `str`
        The full name of the module to find.
    full_name_parts : `list` of `str`
        `full_name` separated by `'.'`.
    path : `str`
        Path to find the module in.
    
    Returns
    -------
    spec : `None`, `ModuleSpec`
    """
    first_name_part = full_name_parts[0]
    
    while True:
        parent_name, directory_name = split_path(path)
        if not directory_name:
            return None
        
        if directory_name == first_name_part:
            module_path = join_paths(parent_name, *full_name_parts)
            spec = create_spec_if_exists(full_name, module_path)
            if (spec is not None):
                return spec
        
        path = parent_name
        continue


def find_spec_in_paths(full_name, paths):
    """
    Tries to the find the spec in the given paths.
    
    Parameters
    ----------
    full_name : `str`
        The full name of the module to find.
    paths : `list` of `str`
        Path to find the module in.
    
    Returns
    -------
    spec : `None`, `ModuleSpec`
    """
    full_name_parts = full_name.split('.')
    if not full_name_parts:
        return None
    
    if paths is None:
        for system_path in sys.path:
            module_path = join_paths(system_path, *full_name_parts)
            spec = create_spec_if_exists(full_name, module_path)
            if (spec is not None):
                return spec
        
    else:
        for path in paths:
            spec = try_find_spec_in_system_paths(full_name, full_name_parts, path)
            if (spec is not None):
                return spec
        
        for path in paths:
            spec = try_find_spec_in_path_fallback(full_name, full_name_parts, path)
            if (spec is not None):
                return spec
    
    return None


def is_spec_in_test_directory(module_specification):
    """
    Returns whether the module specification is a test directory or is in a test directory.
    
    Parameters
    ----------
    module_specification : ``ModuleSpec``
        The module specification to check.
    
    Returns
    -------
    is_spec_in_test_directory : `bool`
    """
    parent = module_specification.parent
    if parent is None:
        return False
    
    for part in reversed(parent.split('.')):
        if (part == 'tests') or part.startswith(('test_', 'tests_')) or part.endswith('_tests'):
            return True
    
    return False
