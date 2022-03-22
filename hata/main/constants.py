__all__ = ('COMMAND_NAME_TO_COMMAND', 'COMMANDS',)

from os.path import dirname as get_directory_name, join as join_paths

from .. import __package__ as PACKAGE_NAME


COMMANDS = set()

COMMAND_NAME_TO_COMMAND = {}

COMMAND_FOLDER = join_paths(
    get_directory_name(__file__),
    'commands',
)

COMMAND_IMPORT_ROUTE = (PACKAGE_NAME, 'main', 'commands')
