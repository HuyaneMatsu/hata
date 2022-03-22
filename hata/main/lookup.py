__all__ = ('find_commands',)

from os import listdir as list_directory
from os.path import isdir as is_directory, join as join_paths

from .constants import COMMANDS, COMMAND_FOLDER, COMMAND_IMPORT_ROUTE, COMMAND_NAME_TO_COMMAND


def find_commands():
    """
    Looks up the local commands.
    """
    COMMANDS.clear()
    COMMAND_NAME_TO_COMMAND.clear()
    
    for file_name in list_directory(COMMAND_FOLDER):
        path = join_paths(COMMAND_FOLDER, file_name)
        if is_directory(path):
            __import__('.'.join([*COMMAND_IMPORT_ROUTE, file_name]))
