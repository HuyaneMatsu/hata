__all__ = ('CommandResult',)

import sys
from scarletio import RichAttributeErrorBaseType, get_short_executable

from .... import __package__ as PACKAGE_NAME

from ..constants import REGISTERED_COMMANDS

from .parameter import TYPE_IDENTIFIER_TO_NAME


class CommandResult(RichAttributeErrorBaseType):
    """
    Represents an command's result.
    
    Attributes
    ----------
    error_code : `int`
        Command result code.
    detail_parameters : `tuple` of `str`
        Additional parameters to pass to the result processor.
    """
    __slots__ = ('detail_parameters', 'error_code',)
    
    def __new__(cls, error_code, *detail_parameters):
        """
        Creates a new ``CommandResult`` with the given parameters.
        
        Parameters
        ----------
        error_code : `int`
            Command result code.
        *detail_parameters : Positional parameters
            Additional parameters to pass to the result processor.
        """
        self = object.__new__(cls)
        self.error_code = error_code
        self.detail_parameters = detail_parameters
        return self
    
    
    def get_message(self):
        """
        Returns the command's result message.
        
        Returns
        -------
        message : `str`
        """
        return COMMAND_RESULT_CODE_TO_MESSAGE_PROCESSOR[self.error_code](*self.detail_parameters)


COMMAND_RESULT_CODE_CONVERSION_FAILED = 1
COMMAND_RESULT_CODE_PARAMETER_REQUIRED = 2
COMMAND_RESULT_CODE_PARAMETER_UNEXPECTED = 3
COMMAND_RESULT_CODE_PARAMETER_EXTRA = 4
COMMAND_RESULT_CODE_PARAMETER_UNSATISFIED = 5
COMMAND_RESULT_CODE_COMMAND_UNINITIALIZED = 6
COMMAND_RESULT_CODE_CATEGORY_EMPTY = 7
COMMAND_RESULT_CODE_CATEGORY_REQUIRES_PARAMETER = 8
COMMAND_RESULT_CODE_CATEGORY_UNKNOWN_SUB_COMMAND = 9
COMMAND_RESULT_CODE_COMMAND_REQUIRED = 10
COMMAND_RESULT_CODE_CALL = 11
COMMAND_RESULT_CODE_COMMAND_NOT_FOUND = 12


def command_result_processor_conversion_failed(command_line_parameter, received_value):
    """
    Command result message processor if conversion fails.
    
    Parameters
    ----------
    command_line_parameter : ``CommandParameter``
        Respective command parameter.
    received_value : `str`
        Received value, which could not be converted to the respective type.
    
    Returns
    -------
    message : `str`
    """
    message_parts = []
    
    message_parts.append('Parameter: ')
    message_parts.append(repr(command_line_parameter.name))
    message_parts.append(' received value of incorrect type.\nGot: ')
    message_parts.append(received_value)
    message_parts.append('\nExpected type: ')
    
    type_name = TYPE_IDENTIFIER_TO_NAME[command_line_parameter.expected_type_identifier]
    message_parts.append(type_name)
    message_parts.append('\n')
    
    return ''.join(message_parts)


def command_result_processor_parameter_required(command_line_parameter):
    """
    Command result message processor if a parameter stays unsatisfied.
    
    Parameters
    ----------
    command_line_parameter : ``CommandParameter``
        Respective command parameter.
    
    Returns
    -------
    message : `str`
    """
    message_parts = []
    
    message_parts.append('Parameter: ')
    message_parts.append(repr(command_line_parameter.name))
    message_parts.append(' is required.\n')
    
    return ''.join(message_parts)


def command_result_processor_parameter_unexpected(parameter_value):
    """
    Command result message processor if a received parameter is unexpected.
    
    Parameters
    ----------
    parameter_value : `str`
        Received parameter.
    
    Returns
    -------
    message : `str`
    """
    message_parts = []
    
    message_parts.append('Unexpected parameter: ')
    message_parts.append(repr(parameter_value))
    message_parts.append('.\n')
    
    return ''.join(message_parts)


def command_result_processor_parameter_extra(parameter_values):
    """
    Command result message processor if received extra parameter(s).
    
    Parameters
    ----------
    parameter_values : `str`
        Extra parameters.
    
    Returns
    -------
    message : `str`
    """
    message_parts = []
    
    message_parts.append('Extra parameters: ')
    
    index = 0
    limit = len(parameter_values)
    
    while True:
        parameter_value = parameter_values[index]
        index += 1
        
        message_parts.append(repr(parameter_value))
        
        if index == limit:
            break
        
        message_parts.append(', ')
        continue
    
    message_parts.append('.\n')
    
    return ''.join(message_parts)


def command_result_processor_parameter_unsatisfied(command_line_parameter):
    """
    Command result message processor if a parameter name is defined, but it's value is not.
    
    Parameters
    ----------
    command_line_parameter : ``CommandParameter``
        Respective command parameter.
    
    Returns
    -------
    message : `str`
    """
    message_parts = []
    
    message_parts.append('Keyword parameter without value defined: ')
    message_parts.append(repr(command_line_parameter.name))
    message_parts.append('.\n')
    
    return ''.join(message_parts)


def command_result_processor_command_uninitialized(command_line_command):
    """
    Command result message processor if a command line command is not initialized (should not happen).
    
    Parameters
    ----------
    command_line_command : ``Command``
        Respective command.
    
    Returns
    -------
    message : `str`
    """
    message_parts = []
    
    message_parts.append('Command: ')
    message_parts.append(repr(command_line_command.name))
    message_parts.append(' is not initialized correctly.\n')
    
    return ''.join(message_parts)
    

def command_result_processor_category_empty(command_category):
    """
    Command result message processor if a command category is empty.
    
    Parameters
    ----------
    command_category : ``CommandCategory``
        Respective command category.
    
    Returns
    -------
    message : `str`
    """
    command_full_name = ''.join(command_category._trace_back_name())
    
    message_parts = []
    
    message_parts.append('Command category: ')
    message_parts.append(repr(command_full_name))
    message_parts.append(' has no direct command, neither sub commands registered.\n')
    
    return ''.join(message_parts)


def command_result_processor_category_requires_parameter(command_category):
    """
    Command result message processor if a command category has no command function to call, when no extra parameter
    is defined.
    
    Parameters
    ----------
    command_category : ``CommandCategory``
        Respective command category.
    
    Returns
    -------
    message : `str`
    """
    command_full_name = ''.join(command_category._trace_back_name())

    message_parts = []
    
    message_parts.append('Command category: ')
    message_parts.append(repr(command_full_name))
    message_parts.append(
        ' has no direct command defined, only sub commands.\n'
        'Please define a sub command by name to call.\n'
        'Available sub-commands:\n'
    )
    
    command_categories = command_category._command_categories
    if (command_categories is not None):
        for command_category_name in sorted(command_categories.keys()):
            message_parts.append('- ')
            message_parts.append(command_category_name)
            message_parts.append('\n')
    
    return ''.join(message_parts)


def command_result_processor_category_unknown_sub_command(command_category, command_name):
    """
    Command result message processor if a command category received unknown sub-command.
    
    Parameters
    ----------
    command_category : ``CommandCategory``
        Respective command category.
    command_name : `str`
        The received command name.
    
    Returns
    -------
    message : `str`
    """
    command_full_name = ' '.join(command_category._trace_back_name())

    message_parts = []
    
    message_parts.append('Command category: ')
    message_parts.append(repr(command_full_name))
    message_parts.append(' has no sub command named: ')
    message_parts.append(repr(command_name))
    message_parts.append(
        '.\n'
        'Available sub-commands:\n'
    )
    
    command_categories = command_category._command_categories
    if (command_categories is not None):
        for command_category_name in sorted(command_categories.keys()):
            message_parts.append('- ')
            message_parts.append(command_category_name)
            message_parts.append('\n')
    
    return ''.join(message_parts)


def command_result_processor_command_required():
    """
    Command result message processor if a command name was not given to run.
    
    Returns
    -------
    message : `str`
    """
    return 'Command name required'


def command_result_processor_call(function, positional_parameters, keyword_parameters):
    """
    Parameters
    ----------
    function : `callable`
        Function to call.
    positional_parameters : `list` of `Any`
        Positional parameters to call the respective function with.
    keyword_parameters : `dict` of (`str`, `Any`) items
        Keyword parameters to call the respective function with.

    Returns
    -------
    message : `str`
    """
    return function(*positional_parameters, **keyword_parameters)



def command_result_processor_command_not_found(command_name):
    """
    Command result message processor if a command name was not given to run.
    
    Parameters
    ----------
    command_name : `str`
        Command name.
    
    Returns
    -------
    message : `str`
    """
    message_parts = []
    
    message_parts.append('There is no command for name: ')
    message_parts.append(repr(command_name))
    message_parts.append(
        '.\n'
        'The available commands are the following:\n'
    )
    
    for command in REGISTERED_COMMANDS:
        message_parts.append('- ')
        message_parts.append(command.name)
        message_parts.append('\n')
    
    message_parts.append('\nTry using "$ ')
    message_parts.append(get_short_executable())
    message_parts.append(' -m ')
    message_parts.append(PACKAGE_NAME)
    message_parts.append(' help" for more information\n.')
    
    return ''.join(message_parts)


COMMAND_RESULT_CODE_TO_MESSAGE_PROCESSOR = {
    COMMAND_RESULT_CODE_CONVERSION_FAILED: command_result_processor_conversion_failed,
    COMMAND_RESULT_CODE_PARAMETER_REQUIRED: command_result_processor_parameter_required,
    COMMAND_RESULT_CODE_PARAMETER_UNEXPECTED: command_result_processor_parameter_unexpected,
    COMMAND_RESULT_CODE_PARAMETER_EXTRA: command_result_processor_parameter_extra,
    COMMAND_RESULT_CODE_PARAMETER_UNSATISFIED: command_result_processor_parameter_unsatisfied,
    COMMAND_RESULT_CODE_COMMAND_UNINITIALIZED: command_result_processor_command_uninitialized,
    COMMAND_RESULT_CODE_CATEGORY_EMPTY: command_result_processor_category_empty,
    COMMAND_RESULT_CODE_CATEGORY_REQUIRES_PARAMETER: command_result_processor_category_requires_parameter,
    COMMAND_RESULT_CODE_CATEGORY_UNKNOWN_SUB_COMMAND: command_result_processor_category_unknown_sub_command,
    COMMAND_RESULT_CODE_COMMAND_REQUIRED: command_result_processor_command_required,
    COMMAND_RESULT_CODE_CALL: command_result_processor_call,
    COMMAND_RESULT_CODE_COMMAND_NOT_FOUND: command_result_processor_command_not_found,
}
