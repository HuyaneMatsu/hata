__all__ = ('ComponentCommand', )

from scarletio import copy_docs

from .....discord.events.handling_helpers import Router, check_name, route_name, route_value

from ...converters import get_component_command_parameter_converters
from ...exceptions import handle_command_exception
from ...responding import process_command_coroutine
from ...response_modifier import ResponseModifier
from ...utils import _check_maybe_route
from ...wrappers import CommandWrapper

from ..command_base_custom_id import CommandBaseCustomId
from ..command_base_custom_id.helpers import _validate_custom_ids, _validate_name, split_and_check_satisfaction

from .constants import COMMAND_TARGETS_COMPONENT_COMMAND


class ComponentCommand(CommandBaseCustomId):
    """
    A command, which is called if a message component interaction is received with a matched `custom_id`.
    
    Attributes
    ----------
    _command_function : `async-callable˛
        The command's function to call.
    _exception_handlers : `None`, `list` of `CoroutineFunction`
        Exception handlers added with ``.error`` to the interaction handler.
        
        Same as ``Slasher._exception_handlers``.
    
    _parent_reference : `None`, ``WeakReferer`` to ``SlashCommand``
        The parent slasher of the component command.
    _parameter_converters : `tuple` of ``ParameterConverter``
        Parsers to parse command parameters.
    _string_custom_ids : `None`, `tuple` of `str`
        The custom id-s to wait for.
    _regex_custom_ids : `None`, `tuple` of `re.Pattern`.
        Regex pattern to match custom-ids.
    name : `str`
        The component commands name.
        
        Only used for debugging.
    
    response_modifier : `None`, ``ResponseModifier``
        Modifies values returned and yielded to command coroutine processor.
    
    Class Attributes
    ----------------
    COMMAND_COMMAND_NAME : `str`
        The command's name defining parameter's name.
    COMMAND_PARAMETER_NAMES : tuple of `str`
        All parameters names accepted by ``.__new__``
    COMMAND_NAME_NAME : `str`
        The command's command defining parameter's name.
    """
    __slots__ = ()
    
    
    def __new__(cls, func, custom_id, name = None, target = None, **kwargs):
        """
        Creates a new ``ComponentCommand`` with the given parameters
        
        Parameters
        ----------
        func : `None`, `async-callable`
            The function used as the command when using the respective slash command.
        custom_id : `str`, (`list`, `set`) of `str`, `tuple` of (`str`, (`list`, `set`) of `str`)
            Custom id to match by the component command.
        name : `None`, `str` = `None`, Optional
            The name of the component command.
        target : `None`, `str` = `None`, Optional
            The component command's target.
        
        Other parameters
        ----------------
        allowed_mentions : `None`, `str`, ``UserBase``, ``Role``, ``AllowedMentionProxy``, \
                `list` of (`str`, ``UserBase``, ``Role`` ), Optional (Keyword only)
            Which user or role can the response message ping (or everyone).
        show_for_invoking_user_only : `bool`, Optional (Keyword only)
            Whether the response message should only be shown for the invoking user.
        wait_for_acknowledgement : `bool`, Optional (Keyword only)
            Whether acknowledge tasks should be ensure asynchronously.
        
        Returns
        -------
        self : ``ComponentCommand``, ``Router``
        
        Raises
        ------
        TypeError
            - If `func` is not async callable, neither cannot be instanced to async.
            - If `func` accepts keyword only parameters.
            - If `func` accepts `*args`.
            - If `func` accepts `**kwargs`.
            - If `name` was not given neither as `None`, `str`.
            - If `custom_id`'s type is incorrect.
        ValueError:
            - If no `custom_id` was received.
            - If `custom_id` contains incorrect value.
            - If `target`'s value is not correct.
        """
        if (target is not None) and (target not in COMMAND_TARGETS_COMPONENT_COMMAND):
            raise ValueError(
                f'`target` can be `None` or any of `{COMMAND_TARGETS_COMPONENT_COMMAND!r}`\'s '
                f'values, got {target!r}'
            )
        
        if (func is not None) and isinstance(func, CommandWrapper):
            command, wrappers = func.fetch_function_and_wrappers_back()
        else:
            command = func
            wrappers = None
        
        # Check for routing.
        route_to = 0
        name, route_to = _check_maybe_route('name', name, route_to, _validate_name)
        custom_id, route_to = _check_maybe_route('custom_id', custom_id, route_to, _validate_custom_ids)
        
        
        # Check extra parameters
        response_modifier = ResponseModifier(kwargs)
        
        if kwargs:
            raise TypeError(f'Extra or unused parameters: {kwargs!r}.')
        
        
        command, parameter_converters = get_component_command_parameter_converters(command)
        
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
                self._string_custom_ids = string_custom_ids
                self._regex_custom_ids = regex_custom_ids
                self._parent_reference = None
                self._exception_handlers = None
                self.name = name
                self.response_modifier = response_modifier
                
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
            self._string_custom_ids = string_custom_ids
            self._regex_custom_ids = regex_custom_ids
            self._parent_reference = None
            self._exception_handlers = None
            self.name = name
            self.response_modifier = response_modifier
            
            if (wrappers is not None):
                for wrapper in wrappers:
                    wrapper.apply(self)
            
            return self
    
    
    @copy_docs(CommandBaseCustomId.invoke)
    async def invoke(self, client, interaction_event, regex_match):
        parameters = []
        
        for parameter_converter in self._parameter_converters:
            try:
                parameter = await parameter_converter(client, interaction_event, regex_match)
            except GeneratorExit:
                raise
            
            except BaseException as err:
                exception = err
            
            else:
                parameters.append(parameter)
                continue
            
            await handle_command_exception(
                self,
                client,
                interaction_event,
                exception,
            )
            return
        
        command_coroutine = self._command_function(*parameters)
        
        try:
            await process_command_coroutine(client, interaction_event, self.response_modifier, command_coroutine)
        except GeneratorExit:
            raise
        
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
