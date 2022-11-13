__all__ = ()

from math import floor, log10

from .... import __package__ as PACKAGE_NAME
from ... import REGISTERED_COMMANDS, REGISTERED_COMMANDS_BY_NAME, command_sort_key, normalize_command_name, register
from ...core.helpers import render_main_call_into


PACKAGE = __import__(PACKAGE_NAME)

BREAK_LINE = '─' * 80


def show_command(command_name, sub_command_names):
    command = REGISTERED_COMMANDS_BY_NAME.get(normalize_command_name(command_name), None)
    
    output_parts = []
    if command is None:
        output_parts = []
        
        output_parts.append('No command is added for: ')
        output_parts.append(repr(command_name))
        output_parts.append('\n\n')
        output_parts.append('Try using "$ ')
        render_main_call_into(output_parts)
        output_parts.append(' help" to list all available commands.\n')
    
    else:
        command.render_direct_usage_into(output_parts, *sub_command_names)
        output_parts.append('\n')
    
    return ''.join(output_parts)


def list_commands():
    output_parts = []
    output_parts.append('Available commands:\n\n')
    
    command_count = len(REGISTERED_COMMANDS)
    index_adjust = floor(log10(command_count)) + 1
    
    for index, command in enumerate(sorted(REGISTERED_COMMANDS, key = command_sort_key), 1):
        command_name = command.name
        output_parts.append(str(index).rjust(index_adjust))
        output_parts.append('. ')
        output_parts.append(command_name)
        output_parts.append('\n')
    
    output_parts.append('\n')
    output_parts.append('Use "$ ')
    render_main_call_into(output_parts)
    output_parts.append(' help ')
    output_parts.append('COMMAND-NAME')
    output_parts.append('" for more information.\n')
    
    return ''.join(output_parts)


@register(
    name = 'help',
    alters = 'h'
)
def help_(command_name: str = None, *sub_command_names):
    """Either lists the available commands, or shows the command's usage."""
    if command_name is None:
        return list_commands()
    else:
        return show_command(command_name, sub_command_names)


@register(
    into = help_
)
def list_all():
    """Shows the help for all the available commands with their sub-commands included."""
    output_parts = []
    field_added = False
    
    for command in sorted(REGISTERED_COMMANDS, key = command_sort_key):
        for output_parts in command.walk_usage_into(output_parts):
            output_parts.append('\n\n')
            output_parts.append(BREAK_LINE)
            output_parts.append('\n\n')
            field_added = True
    
    if field_added:
        del output_parts[-3:]
    
    return ''.join(output_parts)
