__all__ = ('ContextCommand',)

from scarletio import copy_docs

from .....discord.events.handling_helpers import Router, check_name, route_name, route_value

from ...converters import get_context_command_parameter_converters
from ...utils import _check_maybe_route, raw_name_to_display
from ...wrappers import CommandWrapper
from ...exceptions import handle_command_exception
from ...responding import process_command_coroutine

from ..command_base_application_command import CommandBaseApplicationCommand
from ..command_base_application_command.helpers import (
    _validate_allow_in_dm, _validate_delete_on_unload, _validate_guild,
    _validate_is_global, _validate_name, _validate_nsfw, _validate_required_permissions
)
from ..helpers import validate_application_target_type
from ...response_modifier import ResponseModifier


class ContextCommand(CommandBaseApplicationCommand):
    """
    Base class for ``Slasher``'s application commands.
    
    Attributes
    ----------
    _exception_handlers : `None`, `list` of `CoroutineFunction`
        Exception handlers added with ``.error`` to the interaction handler.
        
        Same as ``Slasher._exception_handlers``.
    
    _parent_reference : `None`, ``WeakReferer`` to ``Slasher``
        Reference to the slasher application command's parent.
    
    name : `str`
        Application command name. It's length can be in range [1:32].
    
    _permission_overwrites : `None`, `dict` of (`int`, `list` of ``ApplicationCommandPermissionOverwrite``)
        Permission overwrites applied to the context command.

    _registered_application_command_ids : `None`, `dict` of (`int`, `int`) items
        The registered application command ids, which are matched by the command's schema.
        
        If empty set as `None`, if not then the keys are the respective guild's id and the values are the application
        command id.
    
    _schema : `None`, ``ApplicationCommand``
        Internal slot used by the ``.get_schema`` method.
    
    _unloading_behaviour : `int`
        Behaviour what describes what should happen when the command is removed from the slasher.
        
        Can be any of the following:
        
        +-------------------------------+-------+
        | Respective name               | Value |
        +-------------------------------+-------+
        | UNLOADING_BEHAVIOUR_DELETE    | 0     |
        +-------------------------------+-------+
        | UNLOADING_BEHAVIOUR_KEEP      | 1     |
        +-------------------------------+-------+
        | UNLOADING_BEHAVIOUR_INHERIT   | 2     |
        +-------------------------------+-------+
    
    global_ : `bool`
        Whether the command is a global command.
        
        Global commands have their ``.guild_ids`` set as `None`.
    
    guild_ids : `None`, `set` of `int`
        The ``Guild``'s id to which the command is bound to.
    
    nsfw : `None`, `bool`
        Whether the application command is only allowed in nsfw channels.
    
    required_permissions : `None`, ``Permission``
        The required permissions to use the application command inside of a guild.
    
    _command_function : `async-callable˛
        The command's function to call.
    
    _parameter_converters : `tuple` of ``ParameterConverter``
        Parsers to parse command parameters.
    
    response_modifier : `None`, ``ResponseModifier``
        Modifies values returned and yielded to command coroutine processor.
    
    target : ``ApplicationCommandTargetType``
        The target type of the context command.
    
    Class Attributes
    ----------------
    COMMAND_COMMAND_NAME : `str`
        The command's name defining parameter's name.
    COMMAND_PARAMETER_NAMES : `tuple` of `str`
        All parameters names accepted by ``.__new__``
    COMMAND_NAME_NAME : `str`
        The command's "command" defining parameter's name.
    """
    __slots__ = ('_command_function', '_parameter_converters', 'response_modifier', 'target',)
    
    COMMAND_PARAMETER_NAMES = (
        *CommandBaseApplicationCommand.COMMAND_PARAMETER_NAMES,
        'target',
    )
    
    
    def __new__(
        cls,
        func,
        name = None,
        is_global = None,
        guild = None,
        is_default = None,
        delete_on_unload = None,
        allow_in_dm = None,
        required_permissions = None,
        target = None,
        nsfw = None,
        **keyword_parameters,
    ):
        """
        Creates a new ``SlashCommand`` with the given parameters.
        
        Parameters
        ----------
        func : `None`, `async-callable` = `None`, Optional
            The function used as the command when using the respective context command.
        
        name : `None`, `str`, `tuple` of (`str`, `Ellipsis`, `None`) = `None`, Optional
            The command's name if applicable. If not given or if given as `None`, the `func`'s name will be use
            instead.
        
        is_global : `None`, `bool`, `tuple` of (`None`, `bool`, `Ellipsis`) = `None`, Optional
            Whether the context command is global. Defaults to `False`.
        
        guild : `None`, ``Guild``,  `int`, (`list`, `set`) of (`int`, ``Guild``) or \
                `tuple` of (`None`, ``Guild``,  `int`, `Ellipsis`, (`list`, `set`) of (`int`, ``Guild``)) = `None`
                , Optional
            To which guild(s) the command is bound to.
        
        is_global : `None`, `bool`, `tuple` of (`None`, `bool`, `Ellipsis`) = `None`, Optional
            Whether the context command is the default command in it's category.
        
        delete_on_unload : `None`, `bool`, `tuple` of (`None`, `bool`, `Ellipsis`) = `None`, Optional
            Whether the command should be deleted from Discord when removed.
        
        allow_in_dm : `None`, `bool`, `tuple` of (`None`, `bool`, `Ellipsis`) = `None`, Optional
            Whether the command can be used in private channels (dm).
        
        required_permissions : `None`, `int`, ``Permission``, `tuple` of (`None`, `int`, ``Permission``,
                `Ellipsis`) = `None`, Optional
            The required permissions to use the application command inside of a guild.
        
        target : `None`, `int`, `str`, ``ApplicationCommandTargetType`` = `None`, Optional
            The target type of the command.
        
        nsfw : `None`, `bool`, `tuple` of (`None`, `bool`, `Ellipsis`) = `None`, Optional
            Whether the application command is only allowed in nsfw channels.
        
        **keyword_parameters : Keyword parameters
            Additional keyword parameters.
        
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
        self : ``SlashCommand``, ``Router``
        
        Raises
        ------
        TypeError
            If a parameter's type is incorrect.
        ValueError
            If a parameter's value is incorrect.
        """
        if (func is not None) and isinstance(func, CommandWrapper):
            command, wrappers = func.fetch_function_and_wrappers_back()
        else:
            command = func
            wrappers = None
        
        if command is None:
            raise ValueError(
                f'For context commands `command` parameter is required (cannot be `None` either).'
            )
        
        target = validate_application_target_type(target)
        
        # Check for routing
        
        route_to = 0
        name, route_to = _check_maybe_route('name', name, route_to, _validate_name)
        is_global, route_to = _check_maybe_route('is_global', is_global, route_to, _validate_is_global)
        guild_ids, route_to = _check_maybe_route('guild', guild, route_to, _validate_guild)
        unloading_behaviour, route_to = _check_maybe_route(
            'delete_on_unload', delete_on_unload, route_to, _validate_delete_on_unload
        )
        allow_in_dm, route_to = _check_maybe_route('allow_in_dm', allow_in_dm, route_to, _validate_allow_in_dm)
        nsfw, route_to = _check_maybe_route('nsfw', nsfw, route_to, _validate_nsfw)
        required_permissions, route_to = _check_maybe_route(
            'required_permissions', required_permissions, route_to, _validate_required_permissions
        )
        
        if route_to:
            name = route_name(name, route_to)
            name = [raw_name_to_display(check_name(command, sub_name)) for sub_name in name]
            
            is_global = route_value(is_global, route_to)
            guild_ids = route_value(guild_ids, route_to)
            unloading_behaviour = route_value(unloading_behaviour, route_to)
            allow_in_dm = route_value(allow_in_dm, route_to)
            nsfw = route_value(nsfw, route_to)
            required_permissions = route_value(required_permissions, route_to)
            target = route_value(target, route_to)
        
        else:
            name = check_name(command, name)
            name = raw_name_to_display(name)
            
        
        # Check extra parameters
        response_modifier = ResponseModifier(keyword_parameters)
        
        if keyword_parameters:
            raise TypeError(
                f'Extra or unused parameters: {keyword_parameters!r}.'
            )
        
        
        command, parameter_converters = get_context_command_parameter_converters(command)
        
        
        if route_to:
            router = []
            
            for (
                name, is_global, guild_ids, unloading_behaviour, nsfw, required_permissions, allow_in_dm
            ) in zip(
                name, is_global, guild_ids, unloading_behaviour, nsfw, required_permissions, allow_in_dm
            ):
                
                if is_global and (guild_ids is not None):
                    raise TypeError(
                        f'`is_global` and `guild` contradict each other, got is_global = {is_global!r}, '
                        f'guild = {guild!r}.'
                    )
                
                self = object.__new__(cls)
                self.guild_ids = guild_ids
                self.global_ = is_global
                self.name = name
                self._schema = None
                self._registered_application_command_ids = None
                self._unloading_behaviour = unloading_behaviour
                self.allow_in_dm = allow_in_dm
                self.nsfw = nsfw
                self.required_permissions = required_permissions
                self._permission_overwrites = None
                self.target = target
                self._exception_handlers = None
                self._parent_reference = None
                self._parameter_converters = parameter_converters
                self._command_function = command
                self.response_modifier = response_modifier
                
                if (wrappers is not None):
                    for wrapper in wrappers:
                        wrapper.apply(self)
                
                router.append(self)
            
            return Router(router)
        
        else:
            if is_global and (guild_ids is not None):
                raise TypeError(
                    f'`is_global` and `guild` contradict each other, got is_global = {is_global!r}, '
                    f'guild = {guild!r}.'
                )
            
            self = object.__new__(cls)
            self.guild_ids = guild_ids
            self.global_ = is_global
            self.name = name
            self._schema = None
            self._registered_application_command_ids = None
            self._unloading_behaviour = unloading_behaviour
            self.allow_in_dm = allow_in_dm
            self.nsfw = nsfw
            self.required_permissions = required_permissions
            self._permission_overwrites = None
            self.target = target
            self._exception_handlers = None
            self._parent_reference = None
            self._parameter_converters = parameter_converters
            self._command_function = command
            self.response_modifier = response_modifier
            
            if (wrappers is not None):
                for wrapper in wrappers:
                    wrapper.apply(self)
            
            return self
    
    
    @copy_docs(CommandBaseApplicationCommand._cursed_repr_builder)
    def _cursed_repr_builder(self):
        for repr_parts in CommandBaseApplicationCommand._cursed_repr_builder(self):
            
            yield repr_parts
            
            repr_parts.append(', target = ')
            repr_parts.append(self.target.name)
    
    
    @copy_docs(CommandBaseApplicationCommand.invoke)
    async def invoke(self, client, interaction_event):
        parameters = []
        
        for parameter_converter in self._parameter_converters:
            try:
                parameter = await parameter_converter(client, interaction_event, None)
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
            await process_command_coroutine(
                client,
                interaction_event,
                self.response_modifier,
                command_coroutine,
            )
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
    
    
    @copy_docs(CommandBaseApplicationCommand.copy)
    def copy(self):
        new = CommandBaseApplicationCommand.copy(self)
        
        # _command_function
        new._command_function = self._command_function
        
        # _parameter_converters
        new._parameter_converters = self._parameter_converters
        
        # response_modifier
        new.response_modifier = self.response_modifier
        
        # target
        new.target = self.target
        
        return new
    
    
    @copy_docs(CommandBaseApplicationCommand.__hash__)
    def __hash__(self):
        hash_value = CommandBaseApplicationCommand.__hash__(self)
        
        # _command_function
        command_function = self._command_function
        try:
            command_function_hash_value = hash(command_function)
        except TypeError:
            command_function_hash_value = object.__hash__(command_function)
        hash_value ^= command_function_hash_value
        
        # _parameter_converters
        # Internal field
        
        # response_modifier
        hash_value ^= hash(self.response_modifier)
        
        # target
        hash_value ^= self.target.value << 20
        
        return hash_value
    
    
    @copy_docs(CommandBaseApplicationCommand._is_equal_same_type)
    def _is_equal_same_type(self, other):
        if not CommandBaseApplicationCommand._is_equal_same_type(self, other):
            return False
        
        # _command_function
        if self._command_function != other._command_function:
            return False
        
        # _parameter_converters
        # Internal field
        
        # response_modifier
        if self.response_modifier != other.response_modifier:
            return False
        
        # target
        if self.target is not other.target:
            return False
        
        return True
