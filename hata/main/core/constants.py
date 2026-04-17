__all__ = ('LIBRARY_CALLED_DIRECTLY', 'REGISTERED_COMMANDS', 'REGISTERED_COMMANDS_BY_NAME',)

import sys
from sys import modules
from os import getcwd as get_current_work_directory
from os.path import basename as get_file_name, dirname as get_directory_name, join as join_paths

from ... import __file__ as PACKAGE_INIT_FILE, __package__ as PACKAGE_NAME


UPPER_DIRECTORY = get_directory_name(get_directory_name(PACKAGE_INIT_FILE))
PACKAGE_MAIN_FILE = join_paths(get_directory_name(PACKAGE_INIT_FILE), '__main__.py')
WORKING_DIRECTORY = get_current_work_directory()
COMMAND_DIRECTORY = join_paths(UPPER_DIRECTORY, PACKAGE_NAME, 'main', 'commands')
EXTERNAL_IMPORT_ROUTES_FILE = join_paths(UPPER_DIRECTORY, PACKAGE_NAME, 'main', '.external')

COMMAND_IMPORT_ROUTE = (PACKAGE_NAME, 'main', 'commands')

PYTHON_FILE_POSTFIX_NAMES = frozenset(('.py', '.pyd', '.pyc', '.so'))
SYSTEM_DEFAULT_PARAMETER = 'help'

REGISTERED_COMMANDS = set()
REGISTERED_COMMANDS_BY_NAME = {}

# Get which file was executed.
main_module = modules.get('__main__', None)
if main_module is None:
    LIBRARY_CALLED_DIRECTLY = False
else:
    main_module_spec = main_module.__spec__
    if main_module_spec is not None:
        LIBRARY_CALLED_DIRECTLY = (main_module.__spec__.origin == PACKAGE_MAIN_FILE)
    
    else:
        executed_file = next(iter(sys.argv), None)
        if (executed_file is not None):
            executed_file = get_file_name(executed_file)
        if (UPPER_DIRECTORY != WORKING_DIRECTORY) and (executed_file == PACKAGE_NAME):
            LIBRARY_CALLED_DIRECTLY = True
        else:
            LIBRARY_CALLED_DIRECTLY = False

# Clear up
main_module = None
main_module_spec = None
executed_file = None

del main_module
del main_module_spec
del executed_file
