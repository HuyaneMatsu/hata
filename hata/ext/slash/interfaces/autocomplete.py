__all__ = ()

from functools import partial as partial_func

from scarletio import RichAttributeErrorBaseType, include

from ....discord.events.handling_helpers import Router

from ..constants import APPLICATION_COMMAND_FUNCTION_DEEPNESS

from .command import CommandInterface


SlashCommandParameterAutoCompleter = include('SlashCommandParameterAutoCompleter')


def validate_auto_complete_parameter_name(parameter_name):
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


def build_auto_complete_parameter_names(parameter_name, parameter_names):
    """
    Builds a checks out parameter names.
    
    Parameters
    ----------
    parameter_name : `str`
        The parameter's name to auto complete.
    parameter_names : `tuple<str>`
        Additional parameter to autocomplete.
    
    Returns
    -------
    processed_parameter_names : `list<str>`
        The processed parameter names.
    
    Raises
    ------
    TypeError
        If `parameter_name` is not `str`.
    ValueError
        If `parameter_name` is an empty string.
    """
    processed_parameter_names = []
    
    parameter_name = validate_auto_complete_parameter_name(parameter_name)
    processed_parameter_names.append(parameter_name)
    
    if parameter_names:
        for iterated_parameter_name in parameter_names:
            iterated_parameter_name = validate_auto_complete_parameter_name(iterated_parameter_name)
            if iterated_parameter_name not in processed_parameter_names:
                processed_parameter_names.append(iterated_parameter_name)
    
    return processed_parameter_names


def _register_auto_completer(parent, parameter_names, function):
    """
    Returned by `.autocomplete` decorators wrapped inside of `functools.partial` if `function` is not given.
    
    Parameters
    ----------
    parent : ``AutocompleteInterface``
        The parent entity to register the auto completer to.
    parameter_names : `list` of `str`
        The parameters' names.
    function : `async-callable`
        The function to register as auto completer.
    
    Returns
    -------
    auto_completer : `SlashCommandParameterAutoCompleter`
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
    return parent._register_auto_completer(function, parameter_names)


class AutocompleteInterface(RichAttributeErrorBaseType):
    """
    Common class for auto completable objects.
    """
    __slots__ = ()
    
    def autocomplete(self, parameter_name, *parameter_names, function = ...):
        """
        Registers an auto completer function to the application command.
        
        Parameters
        ----------
        parameter_name : `str`
            The parameter's name.
        
        *parameter_names : `str`
            Additional parameter names to autocomplete
        
        function : `None | async-callable`, Optional (Keyword only)
            The function to register as auto completer.
        
        Returns
        -------
        function / wrapper : `callable`, `functools.partial`
            The registered function if given or a wrapper to register the function with.
        
        Raises
        ------
        RuntimeError
            - If the parameter already has a auto completer defined.
            - If the application command function has no parameter named, like `parameter_name`.
            - If the parameter cannot be auto completed.
        TypeError
            If `function` is not an asynchronous.
        """
        parameter_names = build_auto_complete_parameter_names(parameter_name, parameter_names)
        
        if (function is ...):
            return partial_func(_register_auto_completer, self, parameter_names)
        
        return self._register_auto_completer(function, parameter_names)
    
    
    def _register_auto_completer(self, function, parameter_names):
        """
        Registers an autocomplete function.
        
        Parameters
        ----------
        function : `async-callable`
            The function to register as auto completer.
        
        parameter_names : `list<str>`
            The parameters' names.
        
        Returns
        -------
        auto_completer : `SlashCommandParameterAutoCompleter`
            The registered auto completer
        
        Raises
        ------
        RuntimeError
            - If the application command function has no parameter named, like `parameter_name`.
            - If the parameter cannot be auto completed.
        TypeError
            - If `function` is not an asynchronous.
        """
        auto_completer = self._make_auto_completer(function, parameter_names)
        self._store_auto_completer(auto_completer)
        return auto_completer
    
    
    def _store_auto_completer(self, auto_completer):
        """
        Stores an auto completer.
        
        Parameters
        -------
        auto_completer : ``SlashCommandParameterAutoCompleter``
            The auto completer to store.
        
        Returns
        -------
        stored : `bool`
        instance : ``SlashCommandParameterAutoCompleter``
        """
        auto_completers = self._auto_completers
        if (auto_completers is None):
            auto_completers = []
            self._auto_completers = auto_completers
        
        auto_completers.append(auto_completer)
        return True, auto_completer
    
    
    def _make_auto_completer(self, function, parameter_names):
        """
        Creates an auto completer.
        
        Parameters
        ----------
        function : `async-callable`
            The function to register as auto completer.
        parameter_names : `list<str>`
            The parameters' names.
        
        Returns
        -------
        auto_completer : ``SlashCommandParameterAutoCompleter``
            The created auto completer.
        
        Raises
        ------
        RuntimeError
            - If the application command function has no parameter named, like `parameter_name`.
            - If the parameter cannot be auto completed.
        TypeError
            - If `function` is not an asynchronous.
        """
        if isinstance(function, Router):
            function = function[0]
        
        if isinstance(function, CommandInterface):
            function = function.get_command_function()
        
        return SlashCommandParameterAutoCompleter(
            function,
            parameter_names,
            APPLICATION_COMMAND_FUNCTION_DEEPNESS,
            self,
        )
    
    
    @property
    def _auto_completers(self):
        """
        The registered auto completers.
        
        Overwrite it as an attribute in subclasses.
        
        Returns
        -------
        auto_completers : `None | list<SlashCommandParameterAutoCompleter>`
        """
        return None
    
    
    @_auto_completers.setter
    def _auto_completers(self, value):
        pass
