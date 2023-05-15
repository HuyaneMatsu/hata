__all__ = ()

import sys
from os import getcwd as get_current_work_directory
from os.path import basename as get_file_name, dirname as get_directory_name, join as join_paths

from scarletio import any_to_any, get_short_executable

from ... import __file__ as PACKAGE_INIT_FILE, __package__ as PACKAGE_NAME


UPPER_DIRECTORY = get_directory_name(get_directory_name(PACKAGE_INIT_FILE))
PACKAGE_MAIN_FILE = join_paths(get_directory_name(PACKAGE_INIT_FILE), '__main__.py')
WORKING_DIRECTORY = get_current_work_directory()


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
    system_parameters = sys.argv
    if len(system_parameters) < 1:
        into = _render_default_main_call_into(into)
    
    else:
        executed_file = system_parameters[0]
        if executed_file == PACKAGE_MAIN_FILE:
            into = _render_default_main_call_into(into)
            if with_parameters:
                into = _render_parameters_into(into, system_parameters[1:])
        
        elif (UPPER_DIRECTORY != WORKING_DIRECTORY) and (get_file_name(executed_file) == PACKAGE_NAME):
            into.append(PACKAGE_NAME)
        
        else:
            into.append(get_short_executable())
            into.append(' ')
            into.append(executed_file)
            
        if with_parameters:
            into = _render_parameters_into(into, system_parameters[1:])
    
    return into
