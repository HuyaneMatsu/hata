__all__ = ()

from scarletio import RichAttributeErrorBaseType

from .parameter import get_command_parameters_for
from .parameter_result import ParameterResult
from .result import (
    COMMAND_RESULT_CODE_CALL, COMMAND_RESULT_CODE_PARAMETER_UNEXPECTED, COMMAND_RESULT_CODE_PARAMETER_UNSATISFIED,
    CommandResult
)


class CommandFunction(RichAttributeErrorBaseType):
    """
    Command line function to call.
    
    Attributes
    ----------
    _function : `callable`
        The function to call.
    _parent_reference : `None`, ``WeakReferer``
        Weakreference to the command function's parent.
    _parameter : `list` of ``CommandParameter``
        Parameter parsers to call the command with.
    description : `None`, `str`
        The command's description.
    name : `str`
        The command's name.
    """
    __slots__ = (
        '_function', '_parent_reference', '_parameter', 'description', 'name',
    )
    
    def __new__(cls, parent, function, name, description):
        """
        Creates a new ``CommandFunction``.
        
        Parameters
        ----------
        parent : ``CommandCategory``
            The command's parent.
        function : `callable`
            The function to call when the command is used.
        name : `str`
            The command's name.
        description : `None`, `str`
            The command's description.
        """
        parameters = get_command_parameters_for(function)
        
        self = object.__new__(cls)
        self._function = function
        self._parameter = parameters
        self._parent_reference = parent._self_reference
        self.description = description
        self.name = name
        return self
    
    
    def _trace_back_name(self):
        """
        Traces back to the source name of the command.
        
        This method is an iterable generator.
        
        Yields
        ------
        name : `str`
        """
        parent_reference = self._parent_reference
        if (parent_reference is not None):
            parent = parent_reference()
            if (parent is not None):
                yield from parent._trace_back_name()
    
    
    def invoke(self, parameters, index):
        """
        Calls the command line command.
        
        Parameters
        ----------
        parameters : `list` of `str`
            Command line parameters.
        index : `int`
            The index of the first parameter trying to process.
        
        Returns
        -------
        command_result : ``CommandResult``
        """
        positional_parameters = []
        keyword_parameters = {}
        
        command_result = parse_parameters_into(
            parameters, index, self._parameter, positional_parameters, keyword_parameters
        )
        if (command_result is not None):
            return command_result
        
        
        return CommandResult(
            COMMAND_RESULT_CODE_CALL,
            self._function,
            positional_parameters,
            keyword_parameters,
        )



def parse_parameters_into(parameter_values, start_index, command_parameters, positional_parameters, keyword_parameters):
    """
    Parameters
    ----------
    parameter_values : `list` of `str`
        Command line parameters.
    start_index : `int`
        The index of the first parameter trying to process.
    command_parameters : `list` of ``CommandParameter``
        Parameters of the respective command.
    positional_parameters : `list` of `Any`
        Positional parameters to call the respective function with.
    keyword_parameters : `dict` of (`str`, `Any`) items
        Keyword parameters to call the respective function with.
    
    Returns
    -------
    command_result : `None`, ``CommandResult``
        Returns a command result if failed.
    """
    parameter_values = parameter_values[start_index:]
    
    for parameter_value in parameter_values:
        if parameter_value.startswith('---'):
            return CommandResult(
                COMMAND_RESULT_CODE_PARAMETER_UNEXPECTED,
                parameter_value,
            )
    
    parameter_values.reverse()
    
    
    parameter_results = [ParameterResult(command_parameter) for command_parameter in command_parameters]
    
    while parameter_values:
        parameter_value = parameter_values.pop()
        
        if parameter_value.startswith('--'):
            parameter_name, parsed_value = parse_modifier_parameter_name(parameter_value)
            parameter_result = find_satisfiable_modifier_parameter_result_for(parameter_results, parameter_name)
            if (parameter_result is None):
                return CommandResult(
                    COMMAND_RESULT_CODE_PARAMETER_UNEXPECTED,
                    parameter_value,
                )
            
            command_result = parameter_result.feed(parsed_value)
            if (command_result is not None):
                return command_result
            
            continue
        
        
        if parameter_value.startswith('-'):
            parameter_name = re_normalise_parameter_name(parameter_value)
            parameter_result = find_satisfiable_keyword_parameter_result_for(
                parameter_results,
                parameter_name,
            )
            
            if (parameter_result is None):
                return CommandResult(
                    COMMAND_RESULT_CODE_PARAMETER_UNEXPECTED,
                    parameter_value,
                )
            
            if len(parameter_values) == 0:
                return CommandResult(
                    COMMAND_RESULT_CODE_PARAMETER_UNSATISFIED,
                    parameter_value,
                )
        
            command_result = parameter_result.feed_as(parameter_values.pop(), parameter_name)
            if (command_result is not None):
                return command_result
            
            continue
        
        
        parameter_result = find_next_satisfiable_positional_parameter_result(parameter_results)
        if (parameter_result is None):
            return CommandResult(
                COMMAND_RESULT_CODE_PARAMETER_UNEXPECTED,
                parameter_value,
            )
        
        command_result = parameter_result.feed(parameter_value)
        if (command_result is not None):
            return command_result
        
        continue
    
    
    for parameter_result in parameter_results:
        if not parameter_result.put_into(positional_parameters, keyword_parameters):
            return CommandResult(
                COMMAND_RESULT_CODE_PARAMETER_UNSATISFIED,
                parameter_result.command_parameter,
            )
    
    return None


def re_normalise_parameter_name(parameter_name):
    """
    Re-normalises parameter name.
    
    Parameters
    ----------
    parameter_name : `str`
        The parameter name to normalise.
    
    Returns
    -------
    parameter_name : `str`
    """
    return '-'.join(parameter_name.replace('_', ' ').replace('-', ' ').split())


def parse_modifier_parameter_name(parameter_name):
    """
    Parses modifier type parameter.
    
    Parameters
    ----------
    parameter_name : `str`
        The parameter name to parse.
    
    Returns
    -------
    output_name : `str`
        The parameter's normalises and stripped name.
    output_value : `bool`
        The set value to the parameter.
    """
    parameter_name = re_normalise_parameter_name(parameter_name)
    if parameter_name.startswith('no-'):
        output_value = False
        output_name = parameter_name[len('no-'):]
    else:
        output_value = True
        output_name = parameter_name
    
    return output_name, output_value


def find_satisfiable_modifier_parameter_result_for(parameter_results, parameter_name):
    """
    Finds a satisfiable modifier parameter for the given nane.
    
    Parameters
    ----------
    parameter_results : `list` of ``ParameterResult``
        Parameter results to select from.
    parameter_name : `str`
        Parameter name to match.
    
    Returns
    -------
    parameter_result : ``ParameterResult``
        The matched parameter parse result.
    """
    for parameter_result in parameter_results:
        if (
            parameter_result.is_satisfiable() and
            parameter_result.matches_name(parameter_name) and
            parameter_result.is_modifier()
        ):
            return parameter_result


def find_satisfiable_keyword_parameter_result_for(parameter_results, parameter_name):
    """
    Finds a satisfiable keyword parameter for the given nane.
    
    Parameters
    ----------
    parameter_results : `list` of ``ParameterResult``
        Parameter results to select from.
    parameter_name : `str`
        Parameter name to match.
    
    Returns
    -------
    parameter_result : ``ParameterResult``
        The matched parameter parse result.
    """
    for parameter_result in parameter_results:
        if (
            parameter_result.is_satisfiable() and
            parameter_result.matches_name(parameter_name)
        ):
            return parameter_result


def find_next_satisfiable_positional_parameter_result(parameter_results):
    """
    Finds a satisfiable positional parameter for the given nane.
    
    Parameters
    ----------
    parameter_results : `list` of ``ParameterResult``
        Parameter results to select from.
    
    Returns
    -------
    parameter_result : ``ParameterResult``
        The matched parameter parse result.
    """
    for parameter_result in parameter_results:
        if (
            parameter_result.is_satisfiable() and
            parameter_result.is_positional()
        ):
            return parameter_result
