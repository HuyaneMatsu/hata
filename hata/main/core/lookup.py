__all__ = ('maybe_find_commands',)

import sys
from os import listdir as list_directory
from os.path import isdir as is_directory, isfile as is_file, join as join_paths

from scarletio import render_exception_into

from .constants import COMMAND_DIRECTORY, COMMAND_IMPORT_ROUTE, PYTHON_FILE_POSTFIX_NAMES
from .external import get_external_command_routes


def _ignore_import_frame(file_name, name, line_number, line):
    """
    Ignores the frame where the file is imported.
    
    Parameters
    ----------
    file_name : `str`
        The frame's respective file's name.
    name : `str`
        The frame's respective function's name.
    line_number : `int`
        The line's index where the exception occurred.
    line : `str`
        The frame's respective stripped line.
    
    Returns
    -------
    should_show_frame : `bool`
        Whether the frame should be shown.
    """
    should_show_frame = True
    
    if file_name == __file__:
        if name == '_import_route':
            if line == '__import__(import_route)':
                should_show_frame = False
    
    return should_show_frame


def _import_route(import_route):
    """
    Imports the given route.
    
    Parameters
    ----------
    import_route : `str`
        The import route to import.
    
    Returns
    -------
    success : `bool`
    """
    try:
        __import__(import_route)
    except (KeyboardInterrupt, SystemExit):
        raise
    
    except BaseException as err:
        sys.stderr.write(
            ''.join(
                render_exception_into(
                    err,
                    [
                        'Exception occurred while importing "',
                        import_route,
                        '".\n'
                    ],
                    filter = _ignore_import_frame,
                ),
            )
        )
        return False
    
    return True


def _find_internal_commands():
    """
    Finds the commands in the commands directory.
    """
    for file_name in list_directory(COMMAND_DIRECTORY):
        path = join_paths(COMMAND_DIRECTORY, file_name)
        
        if is_file(path):
            for postfix in PYTHON_FILE_POSTFIX_NAMES:
                if file_name.endswith(postfix):
                    import_name = file_name[:-len(postfix)]
                    break
            
            else:
                continue
        
        elif is_directory(path):
            if is_file(join_paths(path, '__init__.py')):
                import_name = file_name
            else:
                continue
        
        else:
            continue
        
        import_route = '.'.join([*COMMAND_IMPORT_ROUTE, import_name])
        _import_route(import_route)


def _find_external_commands():
    """
    Will try find external commands in registered external import routes.
    """
    external_import_routes = get_external_command_routes()
    for import_route in external_import_routes:
        _import_route(import_route)


_FIND_COMMANDS_INVOKED = False

def maybe_find_commands():
    """
    Looks up the local commands if not yet looked up.
    """
    global _FIND_COMMANDS_INVOKED
    if not _FIND_COMMANDS_INVOKED:
        try:
            _find_commands()
        finally:
            _FIND_COMMANDS_INVOKED = True


def _find_commands():
    """
    Looks up the local commands.
    """
    _find_internal_commands()
    _find_external_commands()
