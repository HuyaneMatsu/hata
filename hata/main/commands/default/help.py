__all__ = ()

from os import get_terminal_size
from math import floor, log10

from ...core import REGISTERED_COMMANDS, REGISTERED_COMMANDS_BY_NAME, command_sort_key, normalize_command_name, register
from ...core.helpers import render_main_call_into


BREAK_LINE_LENGTH_DEFAULT = 80


def render_break_line_into(into, character, name):
    """
    Renders a break line with the given name at the middle.
    
    Parameters
    ----------
    into : `list` of `str`
        The container to render into.
    character : `str`
        The character to create the break from.
    name : `str`
        The command's name.
    
    Returns
    -------
    into : `list` of `str`
    """
    try:
        terminal_size = get_terminal_size()
    except OSError:
        break_line_length = BREAK_LINE_LENGTH_DEFAULT
    else:
        break_line_length = terminal_size.columns
    
    leftover_space = break_line_length - len(name) - 2
    if leftover_space <= 0:
        into.append(name)
    else:
        into.append(character * (leftover_space >> 1))
        into.append(' ')
        into.append(name)
        into.append(' ')
        into.append(character * ((leftover_space >> 1) + (leftover_space & 1)))
    
    into.append('\n')
    
    return into


def show_command(all_, command_name, sub_command_names):
    """
    Returns a command's description.
    
    Parameters
    ----------
    all : `bool`
        Whether all commands should be scanned for the specified name.
    command_name : `str`
        The command name to query for.
    sub_command_names : `tuple` of `str`
        Additional sub command names to search for within the main command.
    
    Returns
    -------
    description : `str`
    """
    command = REGISTERED_COMMANDS_BY_NAME.get(normalize_command_name(command_name), None)
    if (not all_) and (not command.available):
        command = None
    
    output_parts = []
    if command is None:
        output_parts = []
        
        output_parts.append('No command is added for: ')
        output_parts.append(repr(command_name))
        output_parts.append('\n\n')
        output_parts.append('Try using "$ ')
        render_main_call_into(output_parts)
        output_parts.append(' help" to list ')
        output_parts.append('all the' if all_ else 'the available')
        output_parts.append(' commands.\n')
    
    else:
        command.render_direct_usage_into(output_parts, *sub_command_names)
    
    return ''.join(output_parts)


def list_commands(all_):
    """
    Lists all commands.
    
    Parameters
    ----------
    all : `bool`
        Whether all commands should be shown.
    
    Returns
    -------
    description : `str`
    """
    output_parts = []
    output_parts.append('All' if all_ else 'Available')
    output_parts.append(' commands:\n\n')
    
    command_count = len(REGISTERED_COMMANDS)
    if command_count:
        index_adjust = floor(log10(command_count)) + 1
    else:
        index_adjust = 1
    
    if all_:
        commands = [*REGISTERED_COMMANDS]
    else:
        commands = [command for command in REGISTERED_COMMANDS if command.available]
    commands.sort(key = command_sort_key)
    
    for index, command in enumerate(commands, 1):
        command_name = command.name
        output_parts.append(str(index).rjust(index_adjust))
        output_parts.append('. ')
        output_parts.append(command_name)
        output_parts.append('\n')
    
    output_parts.append('\n')
    output_parts.append('Use "$ ')
    render_main_call_into(output_parts)
    output_parts.append(' help COMMAND-NAME')
    if all_:
        output_parts.append(' --all')
    output_parts.append('" for more information.\n')
    
    return ''.join(output_parts)


@register(
    name = 'help',
    aliases = 'h',
)
def help_(command_name: str = None, *sub_command_names, all_: bool = False):
    """Either lists the available commands, or shows the command's usage."""
    if command_name is None:
        return list_commands(all_)
    else:
        return show_command(all_, command_name, sub_command_names)


@register(
    into = help_,
)
def list_(*, all_: bool = False):
    """
    Shows the help of the available commands with their sub-commands included.
    Use the `--all` parameter to show the non-available ones as well.
    """
    output_parts = []
    
    if all_:
        commands = [*REGISTERED_COMMANDS]
    else:
        commands = [command for command in REGISTERED_COMMANDS if command.available]
    commands.sort(key = command_sort_key)
    
    for command in commands:
        command_name = command.name
        output_parts = render_break_line_into(output_parts, '=', command_name)
        
        for command_function in command.iter_command_functions(sort = True):
            command_function_name = command_function.get_full_name()
            if command_function_name != command_name:
                output_parts = render_break_line_into(output_parts, '-', command_function_name)
            
            output_parts.append('\n')
            output_parts = command_function.render_usage_into(output_parts)
            output_parts.append('\n')
    
    return ''.join(output_parts)
