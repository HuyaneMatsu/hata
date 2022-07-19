__all__ = ('add_external_command_route', 'get_external_command_routes',)

import sys
from os.path import exists, join as join_paths, isdir as is_directory, isfile as is_file

from .constants import EXTERNAL_IMPORT_ROUTES_FILE, PYTHON_FILE_POSTFIX_NAMES


def _validate_import_route(import_route):
    """
    Returns whether the given import route refers to an existing file / directory.
    
    Parameters
    ----------
    import_route : `str`
        The import route to check out.
    
    Returns
    -------
    exists : `bool`
    """
    import_route_split = import_route.split('.')
    
    for path in sys.path:
        full_path = join_paths(path, *import_route_split)
        if exists(full_path):
            if is_directory(full_path):
                if is_file(join_paths(full_path, '__init__.py')):
                    return True
        
        else:
            for postfix in PYTHON_FILE_POSTFIX_NAMES:
                if is_file(full_path + postfix):
                    return True
    
    return False


def _save_external_command_routes(command_routes):
    """
    Saves the import routes.
    
    Parameters
    ----------
    command_routes : `set` of `str`
    """
    content = '\n'.join(sorted(command_routes))
    
    with open(EXTERNAL_IMPORT_ROUTES_FILE, 'w') as file:
        file.write(content)


def get_external_command_routes(*, fix_errors=True):
    """
    Reads the external command routes.
    
    Parameters
    ----------
    fix_errors : `bool` = `True`, Optional (Keyword only)
        Whether read errors should be fixed.
    """
    command_routes = set()
    
    if not exists(EXTERNAL_IMPORT_ROUTES_FILE):
        return command_routes
    
    
    with open(EXTERNAL_IMPORT_ROUTES_FILE, 'r') as file:
        content = file.read()
    
    error_found = False
    
    for import_route in content.splitlines():
        import_route = import_route.strip()
        
        if _validate_import_route(import_route):
            command_routes.add(import_route)
        
        else:
            error_found = True
    
    if error_found and fix_errors:
        _save_external_command_routes(command_routes)
    
    return command_routes


def add_external_command_route(command_route, *, validate_command_route=False):
    """
    Adds a new external command route.
    
    Parameters
    ----------
    command_route : `str`
        The command route to add.
    validate_command_route : `bool` = `False`, Optional (Keyword only)
        Whether the existence of the added command route should be checked initially.
    
    Returns
    -------
    command_route_added : `bool`
        Whether the command route was added.
    """
    if validate_command_route:
        if not _validate_import_route(command_route):
            return False
    
    command_routes = get_external_command_routes(fix_errors=False)
    command_routes.add(command_route)
    _save_external_command_routes(command_routes)
    return True
