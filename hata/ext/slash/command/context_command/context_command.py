__all__ = ('ContextCommand',)

from warnings import warn

from scarletio import copy_docs

from .....discord.application import ApplicationIntegrationType
from .....discord.application_command import INTEGRATION_CONTEXT_TYPES_ALL
from .....discord.events.handling_helpers import check_name
from .....discord.permission import Permission

from ...converters import get_context_command_parameter_converters
from ...exceptions import handle_command_exception
from ...interfaces.command import CommandInterface
from ...responding import process_command_coroutine
from ...response_modifier import ResponseModifier
from ...utils import (
    UNLOADING_BEHAVIOUR_DELETE, UNLOADING_BEHAVIOUR_INHERIT, UNLOADING_BEHAVIOUR_KEEP, raw_name_to_display
)
from ...wrappers import CommandWrapper

from ..command_base_application_command import CommandBaseApplicationCommand
from ..command_base_application_command.helpers import (
    _maybe_exclude_dm_from_integration_context_types, _validate_allow_in_dm, _validate_delete_on_unload,
    _validate_guild, _validate_integration_context_types, _validate_integration_types, _validate_is_global,
    _validate_name, _validate_nsfw, _validate_required_permissions
)
from ..helpers import validate_application_target_type


class ContextCommand(CommandInterface, CommandBaseApplicationCommand):
    """
    Base class for ``Slasher``'s application commands.
    
    Attributes
    ----------
    _command_function : `async-callable˛
        The command's function to call.
    
    _exception_handlers : `None | list<CoroutineFunction>`
        Exception handlers added with ``.error`` to the interaction handler.
    
    _parent_reference : `None | WeakReferer<SelfReferenceInterface>`
        Reference to the slasher application command's parent.
    
    name : `str`
        Application command name. It's length can be in range [1:32].
    
    _permission_overwrites : `None | dict<int, list<ApplicationCommandPermissionOverwrite>>˙
        Permission overwrites applied to the context command.

    _registered_application_command_ids : `None | dict<int, int>`
        The registered application command ids, which are matched by the command's schema.
        
        If empty set as `None`, if not then the keys are the respective guild's id and the values are the application
        command id.
    
    _schema : `None | ApplicationCommand`
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
    
    guild_ids : `None | set<int>`
        The ``Guild``'s id to which the command is bound to.
    
    integration_context_types : `None | tuple<ApplicationCommandIntegrationContextType>`
        The places where the application command shows up.
    
    integration_types : `None | tuple<ApplicationIntegrationType>`
        The options where the application command can be integrated to.
    
    nsfw : `None`, `bool`
        Whether the application command is only allowed in nsfw channels.
    
    required_permissions : ``Permission``
        The required permissions to use the application command inside of a guild.
    
    _parameter_converters : `tuple<ParameterConverter>`
        Parsers to parse command parameters.
    
    response_modifier : `None | ResponseModifier`
        Modifies values returned and yielded to command coroutine processor.
    
    target : ``ApplicationCommandTargetType``
        The target type of the context command.
    """
    __slots__ = ('_command_function', '_parameter_converters', 'response_modifier', 'target',)
    
    def __new__(
        cls,
        function,
        name = None,
        *,
        allow_in_dm = ...,
        delete_on_unload = ...,
        guild = ...,
        integration_context_types = ...,
        integration_types = ...,
        is_global = ...,
        nsfw = ...,
        required_permissions = ...,
        target = ...,
        **keyword_parameters,
    ):
        """
        Creates a new context command with the given parameters.
        
        Parameters
        ----------
        function : `async-callable`
            The function used as the command when using the respective context command.
        
        name : `None | str` = `None`, Optional
            The command's name if applicable. If not given or if given as `None`, the `func`'s name will be use
            instead.
        
        delete_on_unload : `bool`, Optional (Keyword only)
            Whether the command should be deleted from Discord when removed.
        
        guild : `Guild | int | (list | set)<int | Guild>`, Optional (Keyword only)
            To which guild(s) the command is bound to.
        
        integration_context_types : `None | ApplicationCommandIntegrationContextType | int | str | \
                iterable<ApplicationCommandIntegrationContextType | int | str>`, Optional (Keyword only)
            The places where the application command shows up.
        
        integration_types : `None | ApplicationIntegrationType | int | str | \
                iterable<ApplicationIntegrationType | int | str>`, Optional (Keyword only)
            The options where the application command can be integrated to.
            
            The places where the application command shows up.
        
        is_global : `bool`, Optional (Keyword only)
            Whether the context command is the default command in it's category.
        
        nsfw : `bool`, Optional (Keyword only)
            Whether the application command is only allowed in nsfw channels.
        
        required_permissions : `int | Permission`, Optional (Keyword only)
            The required permissions to use the application command inside of a guild.
        
        target : `None | int | str | ApplicationCommandTargetType`, Optional (Keyword only)
            The target type of the command.
        
        **keyword_parameters : Keyword parameters
            Additional keyword parameters.
        
        Other Parameters
        ----------------
        allowed_mentions : `None | str, UserBase | Role | AllowedMentionProxy | list<str | UserBase | Role> \
                , Optional (Keyword only)
            Which user or role can the response message ping (or everyone).
        
        show_for_invoking_user_only : `bool`, Optional (Keyword only)
            Whether the response message should only be shown for the invoking user.
        
        wait_for_acknowledgement : `bool`, Optional (Keyword only)
            Whether acknowledge tasks should be ensure asynchronously.
        
        Raises
        ------
        TypeError
            If a parameter's type is incorrect.
        ValueError
            If a parameter's value is incorrect.
        """
        if (function is not None) and isinstance(function, CommandWrapper):
            command_function, wrappers = function.fetch_function_and_wrappers_back()
        else:
            command_function = function
            wrappers = None
        
        if command_function is None:
            raise ValueError(
                f'For context commands `command` parameter is required (cannot be `None` either).'
            )
        
        if target is ...:
            raise ValueError(
                f'For context commands `target` parameter is required (cannot be `None` either).'
            )
        
        target = validate_application_target_type(target)
        
        # Pre validate
        name = _validate_name(name)
        
        # allow_in_dm
        if (allow_in_dm is not ...):
            warn(
                (
                    '`allow_in_dm` parameter is deprecated and will be removed in 2024 November. '
                    'Please use `integration_context_types` instead.'
                ),
                FutureWarning,
                stacklevel = 5,
            )
            allow_in_dm = _validate_allow_in_dm(allow_in_dm)
        
        # delete_on_unload
        if delete_on_unload is ...:
            unloading_behaviour = UNLOADING_BEHAVIOUR_INHERIT
        elif _validate_delete_on_unload(delete_on_unload):
            unloading_behaviour = UNLOADING_BEHAVIOUR_DELETE
        else:
            unloading_behaviour = UNLOADING_BEHAVIOUR_KEEP
        
        # guild
        if guild is ...:
            guild_ids = None
        else:
            guild_ids = _validate_guild(guild)
        
        # integration_context_types
        if integration_context_types is ...:
            integration_context_types = INTEGRATION_CONTEXT_TYPES_ALL
        else:
            integration_context_types = _validate_integration_context_types(integration_context_types)
        
        # integration_types
        if integration_types is ...:
            integration_types = (ApplicationIntegrationType.guild_install,)
        else:
            integration_types = _validate_integration_types(integration_types)
        
        # is_global
        if is_global is ...:
            is_global = False
        else:
            is_global = _validate_is_global(is_global)
        
        # nsfw
        if nsfw is ...:
            nsfw = False
        else:
            nsfw = _validate_nsfw(nsfw)
        
        # required_permissions
        if required_permissions is ...:
            required_permissions = Permission()
        else:
            required_permissions = _validate_required_permissions(required_permissions)
        
        # Check extra parameters
        response_modifier = ResponseModifier(keyword_parameters)
        if keyword_parameters:
            raise TypeError(
                f'Extra or unused parameters: {keyword_parameters!r}.'
            )
        
        # Post validate
        name = check_name(command_function, name)
        name = raw_name_to_display(name)
        
        if is_global and (guild_ids is not None):
            raise TypeError(
                f'`is_global` and `guild` contradict each other, got is_global = {is_global!r}, '
                f'guild = {guild!r}.'
            )
        
        if (allow_in_dm is not ...):
            integration_context_types = _maybe_exclude_dm_from_integration_context_types(
                allow_in_dm, integration_context_types
            )
        
        if not is_global:
            integration_types = None
            integration_context_types = None
        
        command_function, parameter_converters = get_context_command_parameter_converters(command_function)
        
        # Construct
        self = object.__new__(cls)
        self._command_function = command_function
        self._exception_handlers = None
        self._parameter_converters = parameter_converters
        self._parent_reference = None
        self._permission_overwrites = None
        self._registered_application_command_ids = None
        self._schema = None
        self._unloading_behaviour = unloading_behaviour
        self.global_ = is_global
        self.guild_ids = guild_ids
        self.integration_context_types = integration_context_types
        self.integration_types = integration_types
        self.name = name
        self.nsfw = nsfw
        self.required_permissions = required_permissions
        self.response_modifier = response_modifier
        self.target = target
        
        if (wrappers is not None):
            for wrapper in wrappers:
                wrapper.apply(self)
        
        return self
    
    
    @copy_docs(CommandBaseApplicationCommand._put_repr_parts_into)
    def _put_repr_parts_into(self, repr_parts):
        repr_parts = CommandBaseApplicationCommand._put_repr_parts_into(self, repr_parts)
        
        # target
        repr_parts.append(', target = ')
        repr_parts.append(self.target.name)
        
        # response_modifier
        response_modifier = self.response_modifier
        if (response_modifier is not None):
            repr_parts.append(', response_modifier = ')
            repr_parts.append(repr(response_modifier))
        
        return repr_parts
    
    
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

    
    @copy_docs(CommandInterface.get_command_function)
    def get_command_function(self):
        return self._command_function
