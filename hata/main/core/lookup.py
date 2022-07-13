__all__ = ('find_commands',)

from os import listdir as list_directory
from os.path import isdir as is_directory, join as join_paths

from .constants import COMMAND_DIRECTORY, COMMAND_IMPORT_ROUTE, REGISTERED_COMMANDS, REGISTERED_COMMANDS_BY_NAME


def find_commands():
    """
    Looks up the local commands.
    """
    REGISTERED_COMMANDS.clear()
    REGISTERED_COMMANDS_BY_NAME.clear()
    
    for file_name in list_directory(COMMAND_DIRECTORY):
        path = join_paths(COMMAND_DIRECTORY, file_name)
        if is_directory(path):
            __import__('.'.join([*COMMAND_IMPORT_ROUTE, file_name]))
