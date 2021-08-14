import sys
from math import log10, floor
from .. import __package__ as PACKAGE_NAME
from ..__main__ import COMMAND_MAP, COMMAND_NAMES
from ..backend.utils import get_short_executable

PACKAGE = __import__(PACKAGE_NAME)

NAME = 'help'
USAGE = 'h | help *command*'

HELP = (
    f'Either lists the available command, or shows the command\'s usage.\n'
)

def show_command(command_name):
    command_file_name = COMMAND_MAP.get(command_name.lower(), None)
    
    output_parts = []
    if command_file_name is None:
        output_parts = []
        
        output_parts.append('No command is added for: ')
        output_parts.append(repr(command_name))
        output_parts.append('\n')
        output_parts.append('Try using "$ ')
        output_parts.append(get_short_executable())
        output_parts.append(' ')
        output_parts.append(PACKAGE_NAME)
        output_parts.append(' help" to list all available commands\n.')
    else:
        __import__(f'{PACKAGE_NAME}.main.{command_file_name}')
        command_module = getattr(PACKAGE.main, command_file_name)
        name = command_module.NAME
        usage = command_module.USAGE
        help_ = command_module.HELP
        
        output_parts.append('Help for: "')
        output_parts.append(name)
        output_parts.append('"\n\nUsage: "$ ')
        output_parts.append(get_short_executable())
        output_parts.append(' ')
        output_parts.append(PACKAGE_NAME)
        output_parts.append(' ')
        output_parts.append(usage)
        output_parts.append('"\n\n')
        output_parts.append(help_)
    
    output = ''.join(output_parts)
    sys.stderr.write(output)


def list_commands():
    output_parts = []
    output_parts.append('Available commands:\n\n')
    
    command_count = len(COMMAND_NAMES)
    index_adjust = floor(log10(command_count))+1
    index = 0
    while index != command_count:
        command_name = COMMAND_NAMES[index]
        index += 1
        output_parts.append(str(index).rjust(index_adjust))
        output_parts.append('.: ')
        output_parts.append(command_name)
        output_parts.append('\n')
    
    output_parts.append('\n')
    output_parts.append('Use "$ ')
    output_parts.append(get_short_executable())
    output_parts.append(' ')
    output_parts.append(PACKAGE_NAME)
    output_parts.append(' help ')
    output_parts.append('*command*')
    output_parts.append('" for more information.\n')
    
    output = ''.join(output_parts)
    sys.stderr.write(output)


def __main__():
    system_parameters = sys.argv
    if len(system_parameters) < 3:
        command_parameter = None
    else:
        command_parameter = system_parameters[2].lower()
    
    if command_parameter is None:
        list_commands()
    else:
        show_command(command_parameter)
