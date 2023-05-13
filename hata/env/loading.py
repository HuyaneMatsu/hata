__all__ = ()

from os import environ as environmental_variables, environb as environmental_variables_binary
from os.path import dirname as get_directory_name, isfile as is_file, join as join_paths
from sys import _getframe as get_frame

from .parsing import parse_variables


MODULE_FRAME_NAME = '<module>'


def find_launched_location():
    """
    Finds the file that was launched.
    
    Returns
    -------
    location : `None`, `str`
    """
    frame = get_frame()
    
    last_named_location = None
    
    while True:
        frame = frame.f_back
        if frame is None:
            break
        
        # They might falsely name frames with auto generated functions, so check variables as well
        if (frame.f_code.co_name != MODULE_FRAME_NAME):
            continue
        
        frame_global = frame.f_globals
        # Try to not compare locals with globals if we are inside of a function.
        if (frame.f_locals is not frame_global):
            continue
        
        location = frame_global.get('__file__', None)
        if location is None:
            module_specification = frame_global.get('__spec__', None)
            if module_specification is not None:
                location = module_specification.origin
        
        if location is not None:
            last_named_location = location
    
    return last_named_location


def find_dot_env_file():
    """
    Tries to find dotenv location to load.
    
    returns
    -------
    location : `None`, `str`
    """
    launched_location = find_launched_location()
    if (launched_location is not None):
        file_path = join_paths(get_directory_name(launched_location), '.env')
        if is_file(file_path):
            return file_path


def insert_variables(variables):
    """
    Inserts the given variables into the environmental ones. If the variable already exists, will not overwrite it.
    
    Parameters
    ----------
    variables : `dict` of (`str`, `None` | `str`) items
        Loaded environmental variables to insert.
    """
    for key, value in variables.items():
        if value is None:
            value = ''
        
        environmental_variables.setdefault(key, value)
        environmental_variables_binary.setdefault(key.encode(), value.encode())


def load_dot_env_file():
    """
    Loads the dot env file if found.
    """
    location = find_dot_env_file()
    if location is None:
        return
    
    try:
        with open(location, 'r') as file:
            value = file.read()
    except (PermissionError, FileNotFoundError):
        return
    
    variables, error_location = parse_variables(value)
    insert_variables(variables)
