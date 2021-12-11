__all__ = ('FormSubmitCommand', )

try:
    # CPython
    from re import Pattern
except ImportError:
    # ChadPython (PyPy)
    from re import _pattern_type as Pattern

from scarletio import copy_docs

from ...discord.events.handling_helpers import route_value, Router, check_name, route_name

from .wrappers import SlasherCommandWrapper
from .utils import _check_maybe_route
from .converters import get_form_submit_command_parameter_converters
from .responding import process_command_coroutine
from .exceptions import handle_command_exception
from .custom_id_based_command import _validate_name, _validate_custom_ids, split_and_check_satisfaction, \
    CustomIdBasedCommand

COMMAND_TARGETS_FORM_COMPONENT_COMMAND = frozenset((
    'form',
    'form_submit',
))


class FormSubmitCommand(CustomIdBasedCommand):
    """
    A command, which is called if a message component interaction is received with a matched `custom_id`.
    
    Attributes
    ----------
    _command_function : `async-callable˛
        The command's function to call.
    _exception_handlers : `None` or `list` of `CoroutineFunction`
        Exception handlers added with ``.error`` to the interaction handler.
        
        Same as ``Slasher._exception_handlers``.
    
    _parent_reference : `None` or ``WeakReferer`` to ``SlasherApplicationCommand``
        The parent slasher of the component command.
    _parameter_converters : `tuple` of ``ParameterConverter``
        Parsers to parse command parameters.
    _string_custom_ids : `None` or `tuple` of `str`
        The custom id-s to wait for.
    _regex_custom_ids : `None` or `tuple` of `re.Pattern`.
        Regex pattern to match custom-ids.
    name : `str`
        The component commands name.
        
        Only used for debugging.
    _keyword_parameter_converters : `tuple` of ``ParameterConverter``
        Parameter converters for keyword parameters.
    _multi_parameter_converter : `None` or ``ParameterConverter``
        Parameter converter for `*args` parameter.
    
    Class Attributes
    ----------------
    COMMAND_COMMAND_NAME : `str`
        The command's name defining parameter's name.
    COMMAND_PARAMETER_NAMES : tuple of `str`
        All parameters names accepted by ``.__new__``
    COMMAND_NAME_NAME : `str`
        The command's command defining parameter's name.
    """
    __slots__ = ('_keyword_parameter_converters', '_multi_parameter_converter')


    def __new__(cls, func, custom_id, name=None, target=None):
        """
        Creates a new ``FormSubmitCommand`` instance with the given parameters
        
        Parameters
        ----------
        func : `None` or `async-callable`, Optional
            The function used as the command when using the respective slash command.
        custom_id : `str`, (`list` or `set`) of `str`, `tuple` of (`str`, (`list` or `set`) of `str`)
            Custom id to match by the component command.
        name : `str` or `None`, Optional
            The name of the component command.
        target : `str` or `None`, Optional
            The form submit command's target.
        
        Returns
        -------
        self : ``ComponentCommand`` or ``Router``
        
        Raises
        ------
        TypeError
            - If `func` is not async callable, neither cannot be instanced to async.
            - If `func` accepts keyword only parameters.
            - If `func` accepts `*args`.
            - If `func` accepts `**kwargs`.
            - If `name` was not given neither as `None` or `str` instance.
            - If `custom_id`'s type is incorrect.
        ValueError:
            - If no `custom_id` was received.
            - If `custom_id` contains incorrect value.
            - If `target`'s value is not correct.
        """
        if (target is not None) and (target not in COMMAND_TARGETS_FORM_COMPONENT_COMMAND):
            raise ValueError(f'`target` can be either `None` or any of `{COMMAND_TARGETS_FORM_COMPONENT_COMMAND!r}`\s '
                f'values, got {target!r}')
        
        if (func is not None) and isinstance(func, SlasherCommandWrapper):
            command, wrappers = func.fetch_function_and_wrappers_back()
        else:
            command = func
            wrappers = None
        
        # Check for routing.
        route_to = 0
        name, route_to = _check_maybe_route('name', name, route_to, _validate_name)
        custom_id, route_to = _check_maybe_route('custom_id', custom_id, route_to, _validate_custom_ids)
        
        command, parameter_converters, multi_parameter_converter, keyword_parameter_converters = \
            get_form_submit_command_parameter_converters(command)
        
        if route_to:
            custom_id = route_value(custom_id, route_to)
            name = route_name(name, route_to)
            name = [check_name(command, sub_name) for sub_name in name]
            
            router = []
            
            for custom_id, name in zip(custom_id, name):
                string_custom_ids, regex_custom_ids = split_and_check_satisfaction(custom_id, parameter_converters)
                
                self = object.__new__(cls)
                self._command_function = command
                self._parameter_converters = parameter_converters
                self._keyword_parameter_converters = keyword_parameter_converters
                self._multi_parameter_converter = multi_parameter_converter
                self._string_custom_ids = string_custom_ids
                self._regex_custom_ids = regex_custom_ids
                self._parent_reference = None
                self._exception_handlers = None
                self.name = name
                
                if (wrappers is not None):
                    for wrapper in wrappers:
                        wrapper.apply(self)
                
                router.append(self)
            
            return Router(router)
        
        else:
            name = check_name(command, name)
            
            string_custom_ids, regex_custom_ids = split_and_check_satisfaction(custom_id, parameter_converters)
            
            self = object.__new__(cls)
            self._command_function = command
            self._parameter_converters = parameter_converters
            self._keyword_parameter_converters = keyword_parameter_converters
            self._multi_parameter_converter = multi_parameter_converter
            self._string_custom_ids = string_custom_ids
            self._regex_custom_ids = regex_custom_ids
            self._parent_reference = None
            self._exception_handlers = None
            self.name = name
            
            if (wrappers is not None):
                for wrapper in wrappers:
                    wrapper.apply(self)
            
            return self
    
    
    @copy_docs(CustomIdBasedCommand.__call__)
    async def __call__(self, client, interaction_event, regex_match):
        # Positional parameters
        positional_parameters = []
        
        for parameter_converter in self._parameter_converters:
            try:
                parameter = await parameter_converter(client, interaction_event, regex_match)
            except BaseException as err:
                exception = err
            else:
                positional_parameters.append(parameter)
                continue
            
            await handle_command_exception(
                self,
                client,
                interaction_event,
                exception,
            )
            return
        
        parameter_converter = self._multi_parameter_converter
        if (parameter_converter is not None):
            try:
                parameters = await parameter_converter(client, interaction_event, regex_match)
            except BaseException as err:
                exception = err
            else:
                if (parameters is not None):
                    positional_parameters.extend(parameters)
                
                exception = None
            
            # Call it here to not include the received exception as context
            if (exception is not None):
                await handle_command_exception(
                    self,
                    client,
                    interaction_event,
                    exception,
                )
                return
        
        # Keyword parameters
        keyword_parameters = {}
        
        for parameter_converter in self._keyword_parameter_converters:
            try:
                parameter = await parameter_converter(client, interaction_event, regex_match)
            except BaseException as err:
                exception = err
            else:
                keyword_parameters[parameter_converter.parameter_name] = parameter
                continue
            
            await handle_command_exception(
                self,
                client,
                interaction_event,
                exception,
            )
            return
        
        # Call command
        command_coroutine = self._command_function(*positional_parameters, **keyword_parameters)
        
        try:
            await process_command_coroutine(client, interaction_event, False, command_coroutine)
        except BaseException as err:
            exception = err
        else:
            return
        
        await handle_command_exception(
            self,
            client,
            interaction_event,
            exception,
        )
        return
