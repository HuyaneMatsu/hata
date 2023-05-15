__all__ = ()

from os import listdir as list_directory, mkdir as create_directory
from os.path import (
    abspath as absolute_path, basename as base_name, dirname as get_parent_directory_path, exists, isdir as is_directory
)


def _validate_bot(bots_value):
    """
    Validates the given `bot` value. Either `directory_path` or `error_message` is always returned as non-`None`.
    
    Parameters
    ----------
    bots_value : `tuple` of `str`
        The inputted bots.
    
    Returns
    -------
    bots : `None`, `list` of `str`
        The validated bots.
    error_message : `None`, `str`
        Error message.
    """
    if not bots_value:
        return None, f'Please define at least one bot to create.\n'
    
    for value in bots_value:
        if (not value) or (not value.isidentifier()):
            return None, f'Bot name: {value!r} is not a valid identifier.\n'
    
    return sorted({*bots_value}), None


def _validate_name(name_value):
    """
    Validates the given `name` value. Either `directory_path` or `error_message` is always returned as non-`None`.
    
    Parameters
    ----------
    name_value : `str`
        The passed value by the user.
    
    Returns
    -------
    directory_path : `None`, `str`
        Directory path of the project. Might need to be created recursively.
    error_message : `None`, `str`
        Error message.
    """
    directory_path = absolute_path(name_value)
    if is_directory(directory_path):
        if list_directory(directory_path):
            return None, f'Path already exists and not empty:\n{directory_path}\n'
    
    elif exists(directory_path):
        return None, f'Path already exists and its not a directory:\n{directory_path}\n'
    
    else:
        parent_directory_path = get_parent_directory_path(directory_path)
        while True:
            if is_directory(parent_directory_path):
                break
            
            elif exists(parent_directory_path):
                return None, f'Parent already exists, but its not a directory:\n{parent_directory_path}\n'
            
            parent_directory_path = get_parent_directory_path(parent_directory_path)
            continue
    
    return directory_path, None


def _validate_project_name(project_name_value, name_value):
    """
    Validates the given `project_name` value.
    
    Either `project_name` or `error_message` is always returned as non-`None`.
    
    Parameters
    ----------
    project_name_value : `None`, `str`
        The project's name value explicitly defined by the user if any.
    name_value : `str`
        The project's name (used for location).
    
    Returns
    -------
    directory_path : `None`, `str`
        Directory path of the project. Might need to be created recursively.
    error_message : `None`, `str`
        Error message.
    """
    if (project_name_value is not None) and project_name_value:
        project_name = None
    else:
        project_name = base_name(name_value)
    
    if (not project_name) or (not project_name.isidentifier()):
        return (
            None,
            (
                f'A project name\'s must be a valid identifier, got {project_name!r}.\n'
                f'Note that if project name is not explicitly defined it is detected from the name parameter.\n'
            )
        )
    
    return project_name, None


def create_directory_recursive(directory_path):
    """
    Creates the directory's path recursively.
    
    Parameters
    ----------
    directory_path : `str`
        The path to create.
    """
    to_create = None
    
    while True:
        if exists(directory_path):
            break
        
        if (to_create is None):
            to_create = []
        to_create.append(directory_path)
        
        directory_path = get_parent_directory_path(directory_path)
        continue
    
    if (to_create is not None):
        for path in reversed(to_create):
            create_directory(path)
