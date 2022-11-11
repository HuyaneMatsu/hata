__all__ = ()

from .....discord.application_command.constants import (
    APPLICATION_COMMAND_DESCRIPTION_LENGTH_MAX, APPLICATION_COMMAND_DESCRIPTION_LENGTH_MIN
)
from .....discord.preconverters import preconvert_bool

from ...utils import normalize_description

from ..command_base import CommandBase
from ..command_base_application_command.helpers import _reset_application_command_schema


def _validate_is_default(is_default):
    """
    Validates the given `is_default` value.
    
    Parameters
    ----------
    is_default : `None`, `bool`
        The `is_default` value to validate.
    
    Returns
    -------
    is_default : `bool`
        The validated `is_default` value.
    
    Raises
    ------
    TypeError
        If `is_default` was not given as `None` nor as `bool`.
    """
    if is_default is None:
        is_default = False
    else:
        is_default = preconvert_bool(is_default, 'is_default')
    
    return is_default


def _generate_description_from(command, name, description):
    """
    Generates description from the command and it's optionally given description. If both `description` and
    `command.__doc__` is missing, defaults to `name`.
    
    Parameters
    ----------
    command : `None`, `callable`
        The command's function.
    name : `None`, `str`
        The command's name, if name defaulting should be applied.
    description : `Any`
        The command's description.
    
    Returns
    -------
    description : `str`
        The generated description.
    
    Raises
    ------
    ValueError
        If `description` length is out of range [2:100].
    """
    while True:
        if (description is not None) or isinstance(description, str):
            break
        
        if (command is not None):
            description = getattr(command, '__doc__', None)
            if (description is not None) and isinstance(description, str):
                break
        
        if (name is not None):
            description = name
            break
        
        return
    
    description = normalize_description(description)
    
    if description is None:
        description_length = 0
    else:
        description_length = len(description)
    
    if (
        description_length < APPLICATION_COMMAND_DESCRIPTION_LENGTH_MIN or
        description_length > APPLICATION_COMMAND_DESCRIPTION_LENGTH_MAX
    ):
        raise ValueError(
            f'`description` length is out of the expected range '
            f'[{APPLICATION_COMMAND_DESCRIPTION_LENGTH_MIN}:{APPLICATION_COMMAND_DESCRIPTION_LENGTH_MAX}], got '
            f'{description_length!r}; {description!r}.'
        )
    
    return description


def _reset_parent_schema(entity):
    """
    Resets the command category's or function's parent's schema.
    
    Parameters
    ----------
    entity : ``SlashCommandFunction``, ``SlashCommandCategory``
        The category or function to reset it's parent's schema.
    """
    # Reset the parent's schema recursively
    while True:
        parent_reference = entity._parent_reference
        if (parent_reference is None):
            break
        
        entity = parent_reference()
        if (entity is None):
            break
        
        if isinstance(entity, CommandBase):
            _reset_application_command_schema(entity)
            break


def _checkout_auto_complete_parameter_name(parameter_name):
    """
    Checks out one parameter name to auto complete.
    
    Parameters
    ----------
    parameter_name : `str`
        The parameter's name to auto complete.
    
    Returns
    -------
    parameter_name : `str`
        The validated parameter name to autocomplete.
    
    Raises
    ------
    TypeError
        If `parameter_name` is not `str`.
    ValueError
        If `parameter_name` is an empty string.
    """
    if type(parameter_name) is str:
        pass
    elif isinstance(parameter_name, str):
        parameter_name = str(parameter_name)
    else:
        raise TypeError(
            f'`parameter_name` can be `str`, got '
            f'{parameter_name.__class__.__name__}; {parameter_name!r}.'
        )
    
    if not parameter_name:
        raise ValueError(
            f'`parameter_name` cannot be empty string.'
        )
    
    return parameter_name


def _build_auto_complete_parameter_names(parameter_name, parameter_names):
    """
    Builds a checks out parameter names.
    
    Parameters
    ----------
    parameter_name : `str`
        The parameter's name to auto complete.
    parameter_names : `tuple` of `str`
        Additional parameter to autocomplete.
    
    Returns
    -------
    processed_parameter_names : `list` of `str`
        The processed parameter names.
    
    Raises
    ------
    TypeError
        If `parameter_name` is not `str`.
    ValueError
        If `parameter_name` is an empty string.
    """
    processed_parameter_names = []
    
    parameter_name = _checkout_auto_complete_parameter_name(parameter_name)
    processed_parameter_names.append(parameter_name)
    
    if parameter_names:
        for iter_parameter_name in parameter_names:
            iter_parameter_name = _checkout_auto_complete_parameter_name(iter_parameter_name)
            processed_parameter_names.append(iter_parameter_name)
    
    return processed_parameter_names


def _register_auto_complete_function(parent, parameter_names, function):
    """
    Returned by `.autocomplete` decorators wrapped inside of `functools.partial` if `function` is not given.
    
    Parameters
    ----------
    parent : ``Slasher``, ``SlashCommand``, ``SlashCommandFunction``,
            ``SlashCommandCategory``
        The parent entity to register the auto completer to.
    parameter_names : `list` of `str`
        The parameters' names.
    function : `async-callable`
        The function to register as auto completer.
    
    Returns
    -------
    auto_completer : ``SlashCommandParameterAutoCompleter``
        The registered auto completer
    
    Raises
    ------
    RuntimeError
        - `function` cannot be `None`.
        - If the application command function has no parameter named, like `parameter_name`.
        - If the parameter cannot be auto completed.
    TypeError
        If `function` is not an asynchronous.
    """
    if (function is None):
        raise RuntimeError(
            f'`function` cannot be `None`.'
        )
    
    return parent._add_autocomplete_function(parameter_names, function)
