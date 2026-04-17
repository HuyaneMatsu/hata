__all__ = ()

import sys
from os import sep as PATH_SEPARATOR
from os.path import (
    basename as get_file_name, commonpath as _get_common_path, isabs as is_absolute_path, split as split_path
)
from sys import path as system_paths

from scarletio import any_to_any, get_short_executable

from ... import __package__ as PACKAGE_NAME

from .constants import PACKAGE_MAIN_FILE, UPPER_DIRECTORY, WORKING_DIRECTORY


# Conditional imports
if sys.platform == 'linux':
    from os import geteuid as get_effective_user_id
else:
    get_effective_user_id = None


def get_main_call(with_parameters = False):
    """
    Returns how the library main was called.
    
    Parameters
    ----------
    with_parameters : `bool` = `False`, Optional
        Whether call parameters should also be rendered.
    
    Returns
    -------
    main_call : `str`
    """
    return ''.join(render_main_call_into([], with_parameters = with_parameters))


def _render_default_main_call_into(into):
    """
    Renders the the default call way into the given list.
    
    Parameters
    ----------
    into : `list` of `str`
        List to extend.
    
    Returns
    -------
    into : `list` of `str`
    """
    into.append(get_short_executable())
    into.append(' -m ')
    into.append(PACKAGE_NAME)
    return into


def _render_parameters_into(into, parameters):
    """
    Parameters
    ----------
    into : `list` of `str`
        List to extend.
    parameters : `list` of `str`
        The parameters to render.
    
    Returns
    -------
    into : `list` of `str`
    """
    for parameter in parameters:
        into.append(' ')
        if not parameter:
            into.append('""')
            continue
        
        if not any_to_any(parameter, (' ', '"')):
            into.append(parameter)
            continue
        
        into.append('"')
        into.append(parameter.replace('"', '\\"'))
        into.append('"')
        continue

    return into


def get_common_path(paths):
    """
    Returns the longest common path.
    
    Parameters
    ----------
    paths : `iterable<str>`
        Paths.
    
    Returns
    -------
    sub_path : `str`
    """
    try:
        return _get_common_path(paths)
    except ValueError as e:
        # Ignore if the paths are on a different drive lol.
        if e.args and e.args[0] == 'Paths don\'t have the same drive':
            return ''
        
        raise


def normalize_executed_file(executed_file):
    """
    Normalizes the executed file.
    
    Parameters
    ----------
    executed_file : `str`
        File name or path to normalize.
    
    Returns
    -------
    executed_file : `str`
        The executed file normalized.
    library_mode : `bool`
        Whether the executed file was probably ran as a library.
    """
    if not is_absolute_path(executed_file):
        return executed_file, False
    
    directory_name, file_name = split_path(executed_file)
    if file_name == '__main__.py':
        executed_file = directory_name
    
    longest_common_path = max(
        (get_common_path((executed_file, system_path),) for system_path in system_paths),
        default = None,
        key = (lambda path: len(path)),
    )
    if longest_common_path is None:
        return executed_file, True
    
    executed_file = executed_file[len(longest_common_path):]
    if executed_file.startswith(PATH_SEPARATOR):
        executed_file = executed_file[len(PATH_SEPARATOR):]
    
    if not executed_file:
        executed_file = '.'
    
    return executed_file, True


def render_main_call_into(into, with_parameters = False):
    """
    Renders how the library was called into the given list.
    
    Parameters
    ----------
    into : `list` of `str`
        List to extend.
    with_parameters : `bool` = `False`, Optional
        Whether call parameters should also be rendered.
    
    Returns
    -------
    into : `list` of `str`
    """
    if (get_effective_user_id is not None) and (get_effective_user_id() == 0):
        into.append('sudo ')
    
    system_parameters = sys.argv
    
    while True:
        if len(system_parameters) < 1:
            into = _render_default_main_call_into(into)
            with_parameters = False
            break
        
        executed_file = system_parameters[0]
        if executed_file == PACKAGE_MAIN_FILE:
            into = _render_default_main_call_into(into)
            break
            
        if (UPPER_DIRECTORY != WORKING_DIRECTORY):
            executed_file_name = get_file_name(executed_file)
            if'.' not in executed_file_name:
                into.append(executed_file_name)
                break
        
        into.append(get_short_executable())
        into.append(' ')
        executed_file, library_mode = normalize_executed_file(executed_file)
        if library_mode:
            into.append('-m ')
        into.append(executed_file)
        break
        
    if with_parameters:
        into = _render_parameters_into(into, system_parameters[1:])
    
    return into
