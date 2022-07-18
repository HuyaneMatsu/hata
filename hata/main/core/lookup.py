__all__ = ('find_commands',)

import sys
from os import listdir as list_directory
from os.path import isdir as is_directory, isfile as is_file, join as join_paths

from scarletio import render_exception_into

from .constants import (
    COMMAND_DIRECTORY, COMMAND_IMPORT_ROUTE, PYTHON_FILE_POSTFIX_NAMES, REGISTERED_COMMANDS,
    REGISTERED_COMMANDS_BY_NAME
)


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
        if name == 'find_commands':
            if line == '__import__(import_route)':
                should_show_frame = False
    
    return should_show_frame


def find_commands():
    """
    Looks up the local commands.
    """
    REGISTERED_COMMANDS.clear()
    REGISTERED_COMMANDS_BY_NAME.clear()
    
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
