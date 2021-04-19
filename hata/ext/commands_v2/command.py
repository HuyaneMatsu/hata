# -*- coding: utf-8 -*-
import re, reprlib

from ...backend.utils import WeakReferer

from ...discord.parsers import route_value, InteractionEvent, check_name, Router, route_name, _EventHandlerManager
from ...discord.preconverters import preconvert_bool

def _check_maybe_route(variable_name, variable_value, route_to, validator):
    """
    Helper class of ``Command`` parameter routing.
    
    Parameters
    ----------
    variable_name : `str`
        The name of the respective variable
    variable_value : `str`
        The respective value to route maybe.
    route_to : `int`
        The value how much times the routing should happen. by default should be given as `0` if no routing was
        done yet.
    validator : `callable` or `None`
        A callable, what validates the given `variable_value`'s value and converts it as well if applicable.
    
    Returns
    -------
    processed_value : `str`
        Processed value returned by the `validator`. If routing is happening, then a `tuple` of those values is
        returned.
    route_to : `int`
        The amount of values to route to.
    
    Raises
    ------
    ValueError
        Value is routed but to a bad count amount.
    BaseException
        Any exception raised by `validator`.
    """
    if (variable_value is not None) and isinstance(variable_value, tuple):
        route_count = len(variable_value)
        if route_count == 0:
            processed_value = None
        elif route_count == 1:
            variable_value = variable_value[0]
            if variable_value is ...:
                variable_value = None
            
            if validator is None:
                processed_value = variable_value
            else:
                processed_value = validator(variable_value)
        else:
            if route_to == 0:
                route_to = route_count
            elif route_to == route_count:
                pass
            else:
                raise ValueError(f'`{variable_name}` is routed to `{route_count}`, meanwhile something else is '
                    f'already routed to `{route_to}`.')
            
            if validator is None:
                processed_value = variable_value
            else:
                processed_values = []
                for value in variable_value:
                    if (value is not ...):
                        value = validator(value)
                    
                    processed_values.append(value)
                
                processed_value = tuple(processed_values)
    
    else:
        if validator is None:
            processed_value = variable_value
        else:
            processed_value = validator(variable_value)
    
    return processed_value, route_to


def _validate_hidden(hidden):
    """
    Validates the given `is_global` value.
    
    Parameters
    ----------
    hidden : `None` or `bool`
        The `hidden` value to validate.
    
    Returns
    -------
    hidden : `bool`
        The validated `hidden` value.
    
    Raises
    ------
    TypeError
        If `hidden` was not given as `None` nor as `bool` instance.
    """
    if hidden is None:
        hidden = False
    else:
        hidden = preconvert_bool(hidden, 'hidden')
    
    return hidden


def _validate_hidden_if_checks_fail(hidden_if_checks_fail):
    """
    Validates the given `hidden_if_checks_fail` value.
    
    Parameters
    ----------
    hidden_if_checks_fail : `None` or `bool`
        The `hidden_if_checks_fail` value to validate.
    
    Returns
    -------
    hidden_if_checks_fail : `bool`
        The validated `hidden` value.
    
    Raises
    ------
    TypeError
        If `hidden_if_checks_fail` was not given as `None` nor as `bool` instance.
    """
    if hidden_if_checks_fail is None:
        hidden_if_checks_fail = True
    else:
        hidden_if_checks_fail = preconvert_bool(hidden_if_checks_fail, 'hidden_if_checks_fail')
    
    return hidden_if_checks_fail


class Command:
    """
    Represents a command.
    
    Attributes
    ----------
    _category_hint : `str` or `None`
        Hint for the command processor to detect under which category the command should go.
    _category_reference : `None` or ``WeakReferer`` to ``Category``.
        Weak reference to the command's category.
    _checks : `None` or `tuple` of ``CheckBase``
        The checks of the commands.
    _command : `None` or ``CommandFunction``
        The actual command of the command to maybe call.
    _command_processor_reference : `None` or ``WeakReferer`` to ``CommandProcessor``.
        Weak reference to the command's command processor.
    _error_handlers : `None` or `list` of `function`
        Error handlers bind to the command.
    _sub_commands : `None` or `dict` of (`str`, ``CommandCategory``) items
        Sub command categories of the command.
    aliases : `None` or `list` of `str`
        Name aliases of the command if any. They are always lower case.
    display_name : `str`
        The command's display name.
    hidden : `bool`
        Whether the command should be hidden from help commands.
    hidden_if_checks_fail : bool`
        Whether the command should be hidden from help commands if the user's checks fail.
    name : `str`
        The command's name. Always lower case.
    """
    __slots__ = ('_category_hint', '_category_reference', '_checks', '_command', '_command_processor_reference',
        '_error_handlers', '_sub_commands', 'aliases', 'display_name', 'hidden', 'hidden_if_checks_fail', 'name')
    
    
    def _iter_checks(self):
        """
        Iterates over all the checks applied to the command.
        
        This method is a generator, which should be used inside of a for loop.
        
        Yields
        ------
        check : ``CheckBase``
        """
        checks = self._checks
        if (checks is not None):
            yield from checks
        
        category_reference = self._category_reference
        if (category_reference is not None):
            category = category_reference()
            if (category is not None):
                checks = category._checks
                if (checks is not None):
                    yield from checks
    
    
    def _iter_error_handlers(self):
        """
        Iterates over all the error handlers applied to the command.
        
        This method is a generator, which should be used inside of a for loop.
        
        Yields
        ------
        error_handler : `function`
        """
        error_handlers = self._error_handlers
        if (error_handlers is not None):
            yield from error_handlers
        
        category_reference = self._category_reference
        if (category_reference is not None):
            category = category_reference()
            if (category is not None):
                error_handlers = category._error_handlers
                if (error_handlers is not None):
                    yield from error_handlers
        
        command_processor_reference = self._command_processor_reference
        if (command_processor_reference is not None):
            command_processor = command_processor_reference()
            if (command_processor is not None):
                error_handlers = command_processor._error_handlers
                if (error_handlers is not None):
                    yield from error_handlers




