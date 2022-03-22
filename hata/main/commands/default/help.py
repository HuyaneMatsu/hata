import sys
from math import floor, log10

from scarletio import get_short_executable

from .... import __package__ as PACKAGE_NAME

from ... import COMMANDS, COMMAND_NAME_TO_COMMAND


PACKAGE = __import__(PACKAGE_NAME)


def show_command(command_name):
    command = COMMAND_NAME_TO_COMMAND.get(command_name.lower(), None)
    
    output_parts = []
    if command is None:
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
        output_parts.append('Help for: "')
        output_parts.append(command.name)
        output_parts.append('"\n\nUsage: "$ ')
        output_parts.append(get_short_executable())
        output_parts.append(' ')
        output_parts.append(PACKAGE_NAME)
        output_parts.append(' ')
        output_parts.append(command.usage)
        output_parts.append('"\n\n')
        output_parts.append(command.description)
        output_parts.append('\n')
    
    output = ''.join(output_parts)
    sys.stderr.write(output)


def list_commands():
    output_parts = []
    output_parts.append('Available commands:\n\n')
    
    command_count = len(COMMANDS)
    index_adjust = floor(log10(command_count)) + 1
    
    for index, command in enumerate(COMMANDS, 1):
        command_name = command.name
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
