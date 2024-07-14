__all__ = ()

import sys
from os import listdir as list_directory, system as execute
from os.path import (
    abspath as absolute_path, getctime as get_creation_time, isdir as is_directory, isfile as is_file,
    join as join_paths, splitext as split_extension
)
from shlex import quote

from scarletio import get_short_executable

from ...core import LIBRARY_CALLED_DIRECTLY, register
from ...core.helpers import render_main_call_into

# Conditional imports
if sys.platform == 'linux':
    from os import geteuid as get_effective_user_id
else:
    get_effective_user_id = None


PYTHON_EXTENSIONS = frozenset(('.py', '.pyd', '.pyc', '.so'))


def get_profile_names():
    """
    Gets the profiling results' names.
    
    Returns
    -------
    names : `list<str>`
    """
    directory_path = absolute_path('.profiles')
    
    if not is_directory(directory_path):
        return []
    
    results = []
    for name in list_directory(directory_path):
        name_no_extension, extension = split_extension(name)
        if extension != '.prof':
            continue
        
        file_path = join_paths(directory_path, name)
        if not is_file(file_path):
            continue
        
        key = get_creation_time(file_path)
        results.append((key, name_no_extension))
    
    results.sort(reverse = True)
    return [item[1] for item in results]


def get_profile_path(name):
    """
    Get the profile's path for the given name.
    
    Parameters
    ----------
    name : `str`
        Profile name.
    
    Returns
    -------
    path : `None | str`
    """
    directory_path = absolute_path('.profiles')
    path = join_paths(directory_path, name + '.prof')
    if is_file(path):
        return path
    
    return None


def build_profile_listing(names):
    """
    Builds profile listing.
    
    Parameters
    ----------
    names : `list<str>`
        The names of profiles.
    
    Returns
    -------
    output : `str`
    """
    output_parts = []
    for name in names:
        output_parts.append('- ')
        output_parts.append(name)
        output_parts.append('\n')
    
    return ''.join(output_parts)


def has_package(name):
    """
    Returns whether the package with the given name exists.
    
    Parameters
    ----------
    name : `str`
        The name of the package to look up.
    
    Returns
    -------
    has_package : `bool`
    """
    for path in sys.path:
        package_path = join_paths(path, name)
        if is_directory(package_path):
            return True
        
        for extension in PYTHON_EXTENSIONS:
            if is_file(package_path + extension):
                return True
    
    return False


def build_profile_path_not_found(name):
    """
    Builds a profile path not found message.
    
    Parameters
    ----------
    name : `str`
        The profile's name.
    
    Returns
    -------
    output : `str`
    """
    output_parts = []
    output_parts.append('Profile file with name: ')
    output_parts.append(repr(name))
    output_parts.append(' not found.\nTry using "$ ')
    render_main_call_into(output_parts)
    output_parts.append(' profile list" to list the available profiling results.\n')
    return ''.join(output_parts)


def build_package_not_installed(name):
    """
    Builds a package not installed message.
    
    Parameters
    ----------
    name : `str`
        Package name.
    
    Returns
    -------
    output : `str`
    """
    output_parts = []
    output_parts.append('Required package: ')
    output_parts.append(repr(name))
    output_parts.append(' is not installed, cannot show profiling result.\n\nTo install it do:\n\n```\n$ ')
    
    if (get_effective_user_id is not None) and (get_effective_user_id() == 0):
        output_parts.append('sudo ')
    
    output_parts.append(quote(get_short_executable()))
    output_parts.append(' -m pip install ')
    output_parts.append(quote(name))
    output_parts.append('\n```\n')
    return ''.join(output_parts)


PROFILING_CATEGORY = register(
    None,
    available = (not LIBRARY_CALLED_DIRECTLY),
    name = 'profiling',
)


@register(
    into = PROFILING_CATEGORY,
)
def list_():
    """
    Lists the available profiling results.
    """
    names = get_profile_names()
    if not names:
        return 'No profiling results available\n'
    
    return build_profile_listing(names)


@register(
    into = PROFILING_CATEGORY,
)
def show(
    name : str = 'latest',
):
    """
    Shows the given or the latest profiling result.
    """
    path = get_profile_path(name)
    if name is None:
        return build_profile_path_not_found(name)
    
    if not has_package('snakeviz'):
        return build_package_not_installed('snakeviz')
    
    execute(f'{quote(get_short_executable())!s} -m snakeviz {quote(path)!s}')
