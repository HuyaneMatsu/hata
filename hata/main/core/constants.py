__all__ = ('REGISTERED_COMMANDS', 'REGISTERED_COMMANDS_BY_NAME',)

from os.path import dirname as get_directory_name, join as join_paths

from ... import __package__ as PACKAGE_NAME


COMMANDS = set()

COMMAND_NAME_TO_COMMAND = {}

COMMAND_DIRECTORY = join_paths(get_directory_name(get_directory_name(__file__)), 'commands')
EXTERNAL_IMPORT_ROUTES_FILE = join_paths(get_directory_name(get_directory_name(__file__)), '.external')

COMMAND_IMPORT_ROUTE = (PACKAGE_NAME, 'main', 'commands')

PYTHON_FILE_POSTFIX_NAMES = frozenset(('.py', '.pyd', '.pyc', '.so'))

SYSTEM_DEFAULT_PARAMETER = 'i'


REGISTERED_COMMANDS = set()
REGISTERED_COMMANDS_BY_NAME = {}
