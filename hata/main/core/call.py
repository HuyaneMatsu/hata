__all__ = ('call_command', 'execute_command_from_system_parameters',)

import sys

from ...discord import KOKORO

from .command import CommandResult, normalize_command_name
from .command.result import (
    COMMAND_RESULT_CODE_COMMAND_NOT_AVAILABLE,  COMMAND_RESULT_CODE_COMMAND_NOT_FOUND,
    COMMAND_RESULT_CODE_COMMAND_REQUIRED
)
from .constants import REGISTERED_COMMANDS_BY_NAME, SYSTEM_DEFAULT_PARAMETER
from .lookup import maybe_find_commands


def call_command(parameters, index, output_stream):
    """
    Tries to call a command.
    
    Parameters
    ----------
    parameters : `list` of `str`
        Command line parameters.
    index : `int`
        The index of the first parameter trying to process.
    output_stream : `stream-like`
        Output stream.
    """
    maybe_find_commands()
    
    # Use goto
    while True:
        if index >= len(parameters):
            command_result = CommandResult(
                COMMAND_RESULT_CODE_COMMAND_REQUIRED,
            )
            break
    
        command_name = parameters[index]
        index += 1
        command_name = normalize_command_name(command_name)
        
        try:
            command = REGISTERED_COMMANDS_BY_NAME[command_name]
        except KeyError:
            command_result = CommandResult(
                COMMAND_RESULT_CODE_COMMAND_NOT_FOUND,
                command_name,
            )
            break
            
        if not command.available:
            command_result = CommandResult(
                COMMAND_RESULT_CODE_COMMAND_NOT_AVAILABLE,
                command_name,
            )
            break
        
        command_result = command.invoke(parameters, index)
        break
            
    
    output = command_result.get_message()
    if (output is not None):
        output_stream.write(output)
        
        if not output.endswith('\n'):
            output_stream.write('\n')
    


def execute_command_from_system_parameters():
    """
    Calls the respective command from system parameters.
    """
    system_parameters = sys.argv
    if len(system_parameters) < 2:
        system_parameters = [*system_parameters, SYSTEM_DEFAULT_PARAMETER]
    
    try:
        call_command(system_parameters, 1, sys.stdout)
    except BaseException as err:
        exception = err
    else:
        exception = None
    
    # Stop the event loop on exception or if we are doing nothing.
    if KOKORO.running and (exception is not None) or (not KOKORO.get_tasks()):
        KOKORO.stop()
    
    if (exception is not None):
        raise exception
