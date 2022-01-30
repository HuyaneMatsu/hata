__all__ = ('SlasherApplicationCommand', )

from functools import partial as partial_func

from scarletio import WeakReferer, copy_docs, export, include

from ...discord.client import Client
from ...discord.events.handling_helpers import (
    Router, _EventHandlerManager, check_name, create_event_from_class, route_name, route_value
)
from ...discord.guild import Guild
from ...discord.interaction import (
    APPLICATION_COMMAND_CONTEXT_TARGET_TYPES, ApplicationCommand, ApplicationCommandOption,
    ApplicationCommandOptionType, ApplicationCommandTargetType, InteractionEvent
)
from ...discord.interaction.application_command import (
    APPLICATION_COMMAND_DESCRIPTION_LENGTH_MAX, APPLICATION_COMMAND_DESCRIPTION_LENGTH_MIN,
    APPLICATION_COMMAND_NAME_LENGTH_MAX, APPLICATION_COMMAND_NAME_LENGTH_MIN, APPLICATION_COMMAND_OPTIONS_MAX,
    APPLICATION_COMMAND_PERMISSION_OVERWRITE_MAX
)
from ...discord.preconverters import preconvert_bool, preconvert_snowflake

from .converters import (
    InternalParameterConverter, SlashCommandParameterConverter,
    get_application_command_parameter_auto_completer_converters, get_context_command_parameter_converters,
    get_slash_command_parameter_converters
)
from .exceptions import (
    SlasherApplicationCommandParameterConversionError, _register_exception_handler, handle_command_exception,
    test_exception_handler
)
from .responding import process_auto_completer_coroutine, process_command_coroutine
from .response_modifier import ResponseModifier
from .utils import (
    SYNC_ID_GLOBAL, SYNC_ID_NON_GLOBAL, UNLOADING_BEHAVIOUR_DELETE, UNLOADING_BEHAVIOUR_INHERIT,
    UNLOADING_BEHAVIOUR_KEEP, _check_maybe_route, normalize_description, raw_name_to_display
)
from .wrappers import SlasherCommandWrapper, get_parameter_configurers


Slasher = include('Slasher')

# Routers

SLASH_COMMAND_PARAMETER_NAMES = (
    'command', 'name', 'description', 'show_for_invoking_user_only', 'is_global', 'guild', 'is_default',
    'delete_on_unload', 'allow_by_default', 'target', 'allowed_mentions', 'wait_for_acknowledgement'
)

SLASH_COMMAND_NAME_NAME = 'name'
SLASH_COMMAND_COMMAND_NAME = 'command'

APPLICATION_COMMAND_OPTION_TYPE_SUB_COMMAND = ApplicationCommandOptionType.sub_command
APPLICATION_COMMAND_OPTION_TYPE_SUB_COMMAND_CATEGORY = ApplicationCommandOptionType.sub_command_group

APPLICATION_COMMAND_FUNCTION_DEEPNESS = -1
APPLICATION_COMMAND_HANDLER_DEEPNESS = 0
APPLICATION_COMMAND_DEEPNESS = 1
APPLICATION_COMMAND_CATEGORY_DEEPNESS_START = 2
APPLICATION_COMMAND_CATEGORY_DEEPNESS_MAX = 3


def _validate_is_global(is_global):
    """
    Validates the given `is_global` value.
    
    Parameters
    ----------
    is_global : `None`, `bool`
        The `is_global` value to validate.
    
    Returns
    -------
    is_global : `bool`
        The validated `is_global` value.
    
    Raises
    ------
    TypeError
        If `is_global` was not given as `None` nor as `bool`.
    """
    if is_global is None:
        is_global = False
    else:
        is_global = preconvert_bool(is_global, 'is_global')
    
    return is_global


def _validate_1_guild(guild):
    """
    Validates 1 guild value.
    
    Parameters
    ----------
    guild : ``Guild``, `int`
        The guild value to validate.
    
    Returns
    -------
    guild_id : `int`
        Validated guild value converted to `int`.
    
    Raises
    ------
    TypeError
        If `guild` was not given neither as ``Guild`` nor `int`.
    ValueError
        If `guild` is an integer out of uint64 value range.
    """
    if isinstance(guild, Guild):
        guild_id = guild.id
    elif isinstance(guild, (int, str)):
        guild_id = preconvert_snowflake(guild, 'guild')
    else:
        raise TypeError(
            f'`guild`can be `{Guild.__class__.__name__}`, `int`, got {guild.__class__.__name__}; {guild!r}.'
        )
    
    return guild_id


def _validate_guild(guild):
    """
    Validates the given `guild` value.
    
    Parameters
    ----------
    guild : `None`, `int`, ``Guild``, (`list`, `set`) of (`int`, ``Guild``
        The `is_global` value to validate.
    
    Returns
    -------
    guild_ids : `None`, `set` of `int`
        The validated `guild` value.
    
    Raises
    ------
    TypeError
        If `guild` was not given neither as `None`, ``Guild``,  `int`, (`list`, `set`) of (`int`, ``Guild``)
    ValueError
        - If `guild` is given as an empty container.
        - If `guild` is or contains an integer out of uint64 value range.
    """
    if guild is None:
        guild_ids = None
    else:
        guild_ids = set()
        if isinstance(guild, (list, set)):
            for guild_value in guild:
                guild_id = _validate_1_guild(guild_value)
                guild_ids.add(guild_id)
        else:
            guild_id = _validate_1_guild(guild)
            guild_ids.add(guild_id)
        
        if not guild_ids:
            raise ValueError(
                f'`guild` cannot be empty container, got {guild!r}.'
            )
    
    return guild_ids


def _validate_name(name):
    """
    Validates the given name.
    
    Parameters
    ----------
    name : `None`, `str`
        A command's respective name.
    
    Returns
    -------
    name : `None`, `str`
        The validated name.
    
    Raises
    ------
    TypeError
        If `name` is not given as `None` neither as `str`.
    ValueError
        If `name` length is out of the expected range [1:32].
    """
    if name is not None:
        name_type = name.__class__
        if name_type is str:
            pass
        elif issubclass(name_type, str):
            name = str(name)
        else:
            raise TypeError(
                f'`name` can be `None`, `str`, got {name_type.__name__}; {name!r}.'
            )
        
        name_length = len(name)
        if (
            name_length < APPLICATION_COMMAND_NAME_LENGTH_MIN or
            name_length > APPLICATION_COMMAND_NAME_LENGTH_MAX
        ):
            raise ValueError(
                f'`name` length is out of the expected range '
                f'[{APPLICATION_COMMAND_NAME_LENGTH_MIN}:'
                f'{APPLICATION_COMMAND_NAME_LENGTH_MAX}], got {name_length!r}; {name!r}.'
            )
    
    return name


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


def _validate_delete_on_unload(delete_on_unload):
    """
    Validates the given `delete_on_unload` value.
    
    Parameters
    ----------
    delete_on_unload : `None`, `bool`
        The `delete_on_unload` value to validate.
    
    Returns
    -------
    unloading_behaviour : `int`
        The validated `delete_on_unload` value.
    
    Raises
    ------
    TypeError
        If `delete_on_unload` was not given as `None` nor as `bool`.
    """
    if delete_on_unload is None:
        unloading_behaviour = UNLOADING_BEHAVIOUR_INHERIT
    else:
        delete_on_unload = preconvert_bool(delete_on_unload, 'delete_on_unload')
        if delete_on_unload:
            unloading_behaviour = UNLOADING_BEHAVIOUR_DELETE
        else:
            unloading_behaviour = UNLOADING_BEHAVIOUR_KEEP
    
    return unloading_behaviour


def _validate_allow_by_default(allow_by_default):
    """
    Validates the given `allow_by_default` value.
    
    Parameters
    ----------
    allow_by_default : `None`, `bool`
        The `allow_by_default` value to validate.
    
    Returns
    -------
    allow_by_default : `bool`
        The validated `allow_by_default` value.
    
    Raises
    ------
    TypeError
        If `allow_by_default` was not given as `None` nor as `bool`.
    """
    if allow_by_default is None:
        allow_by_default = True
    else:
        allow_by_default = preconvert_bool(allow_by_default, 'allow_by_default')
    
    return allow_by_default


DEFAULT_APPLICATION_COMMAND_TARGET_TYPE = ApplicationCommandTargetType.chat

APPLICATION_COMMAND_TARGET_TYPES_BY_NAME = {
    application_command_target_type.name: application_command_target_type for
    application_command_target_type in ApplicationCommandTargetType.INSTANCES.values()
}

APPLICATION_COMMAND_TARGET_TYPES_BY_VALUE = {
    application_command_target_type.value: application_command_target_type for
    application_command_target_type in ApplicationCommandTargetType.INSTANCES.values()
}


def _validate_target(target):
    """
    Validates the given `TargetType` value.
    
    Parameters
    ----------
    target : `None`, `int`, `str`, ``ApplicationCommandTargetType``
        The `target` to validate.
    
    Returns
    -------
    target : ``ApplicationCommandTargetType``
        The validated `target`.
    
    Raises
    ------
    ValueError
        - If `target` could not be matched by any expected target type name or value.
    TypeError
        - If `target` is neither `None`, `int`, `str`, nor ``ApplicationCommandTargetType``.
    """
    if target is None:
        target = ApplicationCommandTargetType.none
    
    elif isinstance(target, ApplicationCommandTargetType):
        pass
    
    elif isinstance(target, str):
        if type(target) is not str:
            target = str(target)
        
        target = target.lower()
        
        try:
            target = APPLICATION_COMMAND_TARGET_TYPES_BY_NAME[target]
        except KeyError:
            raise ValueError(
                f'Unknown `target` name: {target!r}.'
            ) from None
    
    elif isinstance(target, int):
        if type(target) is not int:
            target = int(target)
        
        try:
            target = APPLICATION_COMMAND_TARGET_TYPES_BY_NAME[target]
        except KeyError:
            raise ValueError(
                f'Unknown `target` value: {target!r}.'
            ) from None
    
    else:
        raise TypeError(
            f'`target` can be `None`, `{ApplicationCommandTargetType.__name__}`, `str`,  `int`, got '
            f'{target.__class__.__name__}; {target!r}.'
        )
    
    if target is ApplicationCommandTargetType.none:
        target = DEFAULT_APPLICATION_COMMAND_TARGET_TYPE
    
    return target


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


def _register_autocomplete_function(parent, parameter_names, function):
    """
    Returned by `.autocomplete` decorators wrapped inside of `functools.partial` if `function` is not given.
    
    Parameters
    ----------
    parent : ``Slasher``, ``SlasherApplicationCommand``, ``SlasherApplicationCommandFunction``,
            ``SlasherApplicationCommandCategory``
        The parent entity to register the auto completer to.
    parameter_names : `list` of `str`
        The parameters' names.
    function : `async-callable`
        The function to register as auto completer.
    
    Returns
    -------
    auto_completer : ``SlasherApplicationCommandParameterAutoCompleter``
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


def _reset_parent_schema(entity):
    """
    Resets the command category's or function's parent's schema.
    
    Parameters
    ----------
    entity : ``SlasherApplicationCommandFunction``, ``SlasherApplicationCommandCategory``
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
        
        if isinstance(entity, SlasherApplicationCommand):
            _reset_slasher_application_command_schema(entity)
            break

def _reset_slasher_application_command_schema(entity):
    """
    Resets the slasher application commands schema.
    
    Parameters
    ----------
    entity : ``SlasherApplicationCommand``
        The command to reset's its schema if applicable.
    """
    schema = entity._schema
    if (schema is not None):
        entity._schema = None
        
        parent_reference = entity._parent_reference
        if (parent_reference is not None):
            slasher = parent_reference()
            
            if (slasher is not None):
                slasher._schema_reset(entity)


@export
class SlasherApplicationCommand:
    """
    Class to wrap an application command providing interface for ``Slasher``.
    
    Attributes
    ----------
    _auto_completers : `None`, `list` of ``SlasherApplicationCommandParameterAutoCompleter``
        Auto completer functions.
    _command : `None`, ``SlasherApplicationCommandFunction``
        The command of the slash command.
    _exception_handlers : `None`, `list` of `CoroutineFunction`
        Exception handlers added with ``.error`` to the interaction handler.
        
        Same as ``Slasher._exception_handlers``.
    
    _parent_reference : `None`, ``WeakReferer`` to ``Slasher``
        Reference to the slasher application command's parent.
    
    _permission_overwrites : `None`, `dict` of (`int`, `list` of ``ApplicationCommandPermissionOverwrite``)
        Permission overwrites applied to the slash command.
    _registered_application_command_ids : `None`, `dict` of (`int`, `int`) items
        The registered application command ids, which are matched by the command's schema.
        
        If empty set as `None`, if not then the keys are the respective guild's id and the values are the application
        command id.
    _schema : `None`, ``ApplicationCommand``
        Internal slot used by the ``.get_schema`` method.
    _self_reference : `None`, ``WeakReferer`` to ``SlasherApplicationCommand``
        Back reference to the slasher application command.
        
        Used by sub commands to access the parent entity.
    
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
    
    _sub_commands : `None`, `dict` of (`str`, (``SlasherApplicationCommandFunction`` or \
            ``SlasherApplicationCommandCategory``)) items
        Sub-commands of the slash command.
        
        Mutually exclusive with the ``._command`` parameter.
    
    allow_by_default : `bool`
        Whether the command is enabled by default for everyone who has `use_application_commands` permission.
    description : `str`
        Application command description. It's length can be in range [2:100].
    guild_ids : `None`, `set` of `int`
        The ``Guild``'s id to which the command is bound to.
    is_default : `bool`
        Whether the command is the default command in it's category.
    is_global : `bool`
        Whether the command is a global command.
        
        Guild commands have ``.guild_ids`` set as `None`.
    name : `str`
        Application command name. It's length can be in range [1:32].
    target : ``ApplicationCommandTargetType``
        The target type of the slash command.
        
        Defaults to ``ApplicationCommandTargetType.chat`.
    
    Notes
    -----
    ``SlasherApplicationCommand``-s are weakreferable.
    """
    __slots__ = (
        '__weakref__', '_auto_completers', '_command', '_exception_handlers', '_parent_reference',
        '_permission_overwrites', '_registered_application_command_ids', '_schema', '_self_reference', '_sub_commands',
        '_unloading_behaviour', 'allow_by_default', 'description', 'guild_ids', 'is_default', 'is_global', 'name',
        'target'
    )
    
    def _register_guild_and_application_command_id(self, guild_id, application_command_id):
        """
        Registers an application command's identifier to the ``SlasherApplicationCommand`.
        
        Parameters
        ----------
        application_command_id : `int`
            The application command's identifier.
        guild_id : `int`
            The guild where the application command is in.
        """
        registered_application_command_ids = self._registered_application_command_ids
        if registered_application_command_ids is None:
            registered_application_command_ids = self._registered_application_command_ids = {}
        
        registered_application_command_ids[guild_id] = application_command_id
    
    def _unregister_guild_and_application_command_id(self, guild_id, application_command_id):
        """
        Unregisters an application command's identifier from the ``SlasherApplicationCommand`.
        
        Parameters
        ----------
        guild_id : `int`
            The guild's id, where the application command is in.
        application_command_id : `int`
            The application command's identifier.
        """
        registered_application_command_ids = self._registered_application_command_ids
        if registered_application_command_ids is not None:
            try:
                maybe_application_command_id = registered_application_command_ids[guild_id]
            except KeyError:
                pass
            else:
                if maybe_application_command_id == application_command_id:
                    del registered_application_command_ids[guild_id]
                    
                    if not registered_application_command_ids:
                        self._registered_application_command_ids = None
    
    def _pop_command_id_for(self, guild_id):
        """
        Pops the given application command id from the command for the respective guild.
        
        Parameters
        ----------
        guild_id : `int`
            A guild's identifier.
        
        Returns
        -------
        application_command_id : `int`
            The popped application command's identifier. Returns `0` if nothing is matched.
        """
        registered_application_command_ids = self._registered_application_command_ids
        if registered_application_command_ids is None:
            application_command_id = 0
        else:
            application_command_id = registered_application_command_ids.pop(guild_id, 0)
        
        return application_command_id
    
    def _iter_application_command_ids(self):
        """
        Iterates over all the registered application command id-s added to the slash command.
        
        This method is a generator, what should be used inside of a `for` loop.
        
        Yields
        ------
        application_command_id : `int`
        """
        registered_application_command_ids = self._registered_application_command_ids
        if (registered_application_command_ids is not None):
            yield from registered_application_command_ids.values()
    
    def _exhaust_application_command_ids(self):
        """
        Iterates over all the registered application command id-s added to the slash command and removes them.
        
        This method is a generator, what should be used inside of a `for` loop.
        
        Yields
        ------
        application_command_id : `int`
        """
        registered_application_command_ids = self._registered_application_command_ids
        if (registered_application_command_ids is not None):
            while registered_application_command_ids:
                guild_id, application_command_id = registered_application_command_ids.popitem()
                yield application_command_id
            
            self._registered_application_command_ids = None
    
    def _iter_sync_ids(self):
        """
        Iterates over all the respective sync ids of the command. If the command is a guild bound command, then will
        iterate over it's guild's id-s.
        
        This method is a generator, what should be used inside of a `for` loop.
        
        Yields
        ------
        sync_id : `int`
        """
        if self.is_global:
            yield SYNC_ID_GLOBAL
            return
        
        guild_ids = self.guild_ids
        if guild_ids is None:
            yield SYNC_ID_NON_GLOBAL
            return
        
        yield from guild_ids
    
    def _iter_guild_ids(self):
        """
        Iterates over all the guild identifiers used by the command.
        
        Yields
        ------
        guild_id : `int`
        """
        registered_application_command_ids = self._registered_application_command_ids
        if registered_application_command_ids is not None:
            for sync_id in registered_application_command_ids:
                if sync_id > (1 << 22):
                    yield sync_id
    
    
    @classmethod
    def from_class(cls, klass):
        """
        Creates a new ``SlasherApplicationCommand`` from the given `klass`.
        
        Parameters
        ----------
        klass : `type`
            The class to create slash command from.
        
        Returns
        -------
        self : ``SlasherApplicationCommand``, ``Router``
        
        Raises
        ------
        TypeError
            If any attribute's type is incorrect.
        ValueError
            If any attribute's value is incorrect.
        """
        return create_event_from_class(cls, klass, SLASH_COMMAND_PARAMETER_NAMES, SLASH_COMMAND_NAME_NAME,
            SLASH_COMMAND_COMMAND_NAME)
    
    
    def __new__(cls, func, name=None, description=None, is_global=None,
            guild=None, is_default=None, delete_on_unload=None, allow_by_default=None, target=None,
            **kwargs,
        ):
        """
        Creates a new ``SlasherApplicationCommand`` with the given parameters.
        
        Parameters
        ----------
        func : `None`, `async-callable` = `None`, Optional
            The function used as the command when using the respective slash command.
        name : `None`, `str`, `tuple` of (`str`, `Ellipsis`, `None`) = `None`, Optional
            The command's name if applicable. If not given or if given as `None`, the `func`'s name will be use
            instead.
        description : `None`, `Any`, `tuple` of (`None`, `Ellipsis`, `Any`) = `None`, Optional
            Description to use instead of the function's docstring.
        is_global : `None`, `bool`, `tuple` of (`None`, `bool`, `Ellipsis`) = `None`, Optional
            Whether the slash command is global. Defaults to `False`.
        guild : `None`, ``Guild``,  `int`, (`list`, `set`) of (`int`, ``Guild``) or \
                `tuple` of (`None`, ``Guild``,  `int`, `Ellipsis`, (`list`, `set`) of (`int`, ``Guild``)) = `None`
                , Optional
            To which guild(s) the command is bound to.
        is_global : `None`, `bool`, `tuple` of (`None`, `bool`, `Ellipsis`) = `None`, Optional
            Whether the slash command is the default command in it's category.
        delete_on_unload : `None`, `bool`, `tuple` of (`None`, `bool`, `Ellipsis`) = `None`, Optional
            Whether the command should be deleted from Discord when removed.
        allow_by_default : `None`, `bool`, `tuple` of (`None`, `bool`, `Ellipsis`) = `None`, Optional
            Whether the command is enabled by default for everyone who has `use_application_commands` permission.
        target : `None`, `int`, `str`, ``ApplicationCommandTargetType`` = `None`, Optional
            The target type of the slash command.
            
            Defaults to `ApplicationCommandTargetType.chat`.
        
        **kwargs : Keyword parameters
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
        self : ``SlasherApplicationCommand``, ``Router``
        
        Raises
        ------
        TypeError
            If a parameter's type is incorrect.
        ValueError
            If a parameter's value is incorrect.
        """
        if (func is not None) and isinstance(func, SlasherCommandWrapper):
            command, wrappers = func.fetch_function_and_wrappers_back()
        else:
            command = func
            wrappers = None
        
        # Check for routing
        
        route_to = 0
        name, route_to = _check_maybe_route('name', name, route_to, _validate_name)
        description, route_to = _check_maybe_route('description', description, route_to, None)
        is_global, route_to = _check_maybe_route('is_global', is_global, route_to, _validate_is_global)
        guild_ids, route_to = _check_maybe_route('guild', guild, route_to, _validate_guild)
        is_default, route_to = _check_maybe_route('is_default', is_default, route_to, _validate_is_default)
        unloading_behaviour, route_to = _check_maybe_route('delete_on_unload', delete_on_unload, route_to,
            _validate_delete_on_unload)
        allow_by_default, route_to = _check_maybe_route('allow_by_default', allow_by_default, route_to,
            _validate_allow_by_default)
        
        target = _validate_target(target)
        
        if route_to:
            name = route_name(name, route_to)
            name = [raw_name_to_display(check_name(command, sub_name)) for sub_name in name]
            
            default_description = _generate_description_from(command, None, None)
            is_global = route_value(is_global, route_to)
            guild_ids = route_value(guild_ids, route_to)
            is_default = route_value(is_default, route_to)
            unloading_behaviour = route_value(unloading_behaviour, route_to)
            allow_by_default = route_value(allow_by_default, route_to)
            target = route_value(target, route_to)
            
            description = [
                _generate_description_from(command, sub_name, description)
                    if ((description is None) or (description is not default_description)) else default_description
                for sub_name, description in zip(name, description)]
        
        else:
            name = check_name(command, name)
            
            sub_name_length = len(name)
            if (
                sub_name_length < APPLICATION_COMMAND_NAME_LENGTH_MIN or
                sub_name_length > APPLICATION_COMMAND_NAME_LENGTH_MAX
            ):
                raise ValueError(
                    f'`name` length is out of the expected range '
                    f'[{APPLICATION_COMMAND_NAME_LENGTH_MIN}:'
                    f'{APPLICATION_COMMAND_NAME_LENGTH_MAX}], got {sub_name_length!r}; {name!r}.'
                )
            
            name = raw_name_to_display(name)
            
            description = _generate_description_from(command, name, description)
        
        
        # Check extra parameters
        response_modifier = ResponseModifier(kwargs)
        
        if kwargs:
            raise TypeError(f'Extra or unused parameters: {kwargs!r}.')
        
        
        if target in APPLICATION_COMMAND_CONTEXT_TARGET_TYPES:
            if command is None:
                raise ValueError(
                    f'For context commands `command` parameter is required (cannot be `None`).'
                )
            
            command, parameter_converters = get_context_command_parameter_converters(command)
        else:
            if command is None:
                parameter_converters = None
            else:
                parameter_configurers = get_parameter_configurers(wrappers)
                command, parameter_converters = get_slash_command_parameter_converters(command, parameter_configurers)
        
        
        if route_to:
            router = []
            
            for (
                name, description, is_global, guild_ids, is_default, unloading_behaviour, allow_by_default
            ) in zip(
                name, description, is_global, guild_ids, is_default, unloading_behaviour, allow_by_default
            ):
                
                if is_global and (guild_ids is not None):
                    raise TypeError(
                        f'`is_global` and `guild` contradict each other, got is_global={is_global!r}, '
                        f'guild={guild!r}.'
                    )
                
                if (command is None):
                    command_function = None
                    sub_commands = {}
                else:
                    command_function = SlasherApplicationCommandFunction(command, parameter_converters, name,
                        description, response_modifier, is_default)
                    sub_commands = None
                
                self = object.__new__(cls)
                self._command = command_function
                self._sub_commands = sub_commands
                self.description = description
                self.guild_ids = guild_ids
                self.is_global = is_global
                self.name = name
                self._schema = None
                self._registered_application_command_ids = None
                self.is_default = is_default
                self._unloading_behaviour = unloading_behaviour
                self.allow_by_default = allow_by_default
                self._permission_overwrites = None
                self.target = target
                self._auto_completers = None
                self._exception_handlers = None
                self._parent_reference = None
                self._self_reference = None
                
                if (command_function is not None):
                    command_function._parent_reference = self._get_self_reference()
                
                if (wrappers is not None):
                    for wrapper in wrappers:
                        wrapper.apply(self)
                
                router.append(self)
            
            return Router(router)
        else:
            if is_global and (guild_ids is not None):
                raise TypeError(
                    f'`is_global` and `guild` contradict each other, got is_global={is_global!r}, '
                    f'guild={guild!r}.'
                )
            
            if (command is None):
                sub_commands = {}
                command_function = None
            else:
                command_function = SlasherApplicationCommandFunction(command, parameter_converters, name, description,
                    response_modifier, is_default)
                sub_commands = None
            
            self = object.__new__(cls)
            self._command = command_function
            self._sub_commands = sub_commands
            self.description = description
            self.guild_ids = guild_ids
            self.is_global = is_global
            self.name = name
            self._schema = None
            self._registered_application_command_ids = None
            self.is_default = is_default
            self._unloading_behaviour = unloading_behaviour
            self.allow_by_default = allow_by_default
            self._permission_overwrites = None
            self.target = target
            self._auto_completers = None
            self._exception_handlers = None
            self._parent_reference = None
            self._self_reference = None
            
            if (command_function is not None):
                command_function._parent_reference = self._get_self_reference()
            
            if (wrappers is not None):
                for wrapper in wrappers:
                    wrapper.apply(self)
            
            return self
    
    
    def __repr__(self):
        """returns the slash command's representation."""
        result = ['<', self.__class__.__name__, ' name=', repr(self.name), ', type=']
        
        guild_ids = self.guild_ids
        if guild_ids is None:
            if self.is_global:
                type_name = 'global'
            else:
                type_name = 'non-global'
        else:
            type_name = 'guild bound'
        
        result.append(type_name)
        
        if not self.allow_by_default:
            result.append(', allow_by_default=False')
        
        target = self.target
        if target is not DEFAULT_APPLICATION_COMMAND_TARGET_TYPE:
             result.append(', target=')
             result.append(target.name)
        
        if (guild_ids is not None):
            result.append(', guild_ids=')
            result.append(repr(guild_ids))
        
        unloading_behaviour = self._unloading_behaviour
        if unloading_behaviour != UNLOADING_BEHAVIOUR_INHERIT:
            result.append(', unloading_behaviour=')
            if unloading_behaviour == UNLOADING_BEHAVIOUR_DELETE:
                unloading_behaviour_name = 'delete'
            else:
                unloading_behaviour_name = 'keep'
            
            result.append(unloading_behaviour_name)
        
        result.append('>')
        
        return ''.join(result)
    
    
    async def __call__(self, client, interaction_event):
        """
        Calls the slash command.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client who received the event.
        interaction_event : ``InteractionEvent``
            The received interaction event.
        """
        options = interaction_event.interaction.options
        
        command = self._command
        if (command is not None):
            await command(client, interaction_event, options)
            return
        
        if (options is None) or (len(options) != 1):
            return
        
        option = options[0]
        
        try:
            sub_command = self._sub_commands[option.name]
        except KeyError:
            pass
        else:
            await sub_command(client, interaction_event, option.options)
            return
        
        # Do not put this into the `except` branch.
        await handle_command_exception(
            self,
            client,
            interaction_event,
            SlasherApplicationCommandParameterConversionError(
                None,
                option.name,
                'sub-command',
                list(self._sub_commands.keys()),
            )
        )
        return
    
    
    async def call_auto_completion(self, client, interaction_event, auto_complete_option):
        """
        Calls the auto completion function of the slasher application command.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client who received the event.
        interaction_event : ``InteractionEvent``
            The received interaction event.
        auto_complete_option : ``ApplicationCommandAutocompleteInteraction``
            The option to autocomplete.
        """
        command_function = self._command
        if (command_function is not None):
            await command_function.call_auto_completion(client, interaction_event, auto_complete_option)
            return
        
        sub_commands = self._sub_commands
        if (sub_commands is not None):
            auto_complete_option = auto_complete_option.options[0]
            
            auto_complete_option_type = auto_complete_option.type
            if (
                (auto_complete_option_type is APPLICATION_COMMAND_OPTION_TYPE_SUB_COMMAND) or
                (auto_complete_option_type is APPLICATION_COMMAND_OPTION_TYPE_SUB_COMMAND_CATEGORY)
            ):
                options = auto_complete_option.options
                if (options is not None):
                    try:
                        sub_command = sub_commands[auto_complete_option.name]
                    except KeyError:
                        pass
                    else:
                        await sub_command.call_auto_completion(client, interaction_event, auto_complete_option)
            
            return
        
        # no more cases
    
    def get_schema(self):
        """
        Returns an application command schema representing the slash command.
        
        Returns
        -------
        schema : ``ApplicationCommand``
        """
        schema = self._schema
        if schema is None:
            schema = self._schema = self.as_schema()
        
        return schema
    
    
    def as_schema(self):
        """
        Creates a new application command schema representing the slash command.
        
        Returns
        -------
        schema : ``ApplicationCommand``
        """
        command = self._command
        if command is None:
            sub_commands = self._sub_commands
            options = [sub_command.as_option() for sub_command in sub_commands.values()]
        else:
            parameter_converters = command._parameter_converters
            
            options = None
            for parameter_converter in parameter_converters:
                option = parameter_converter.as_option()
                if (option is not None):
                    if (options is None):
                        options = []
                    
                    options.append(option)
        
        return ApplicationCommand(self.name, self.description, allow_by_default=self.allow_by_default,
            options=options, target_type=self.target)
    
    
    def as_sub(self, deepness):
        """
        Returns the slash command as a sub-command or sub-category.
        
        Parameters
        ----------
        deepness : `int`
            How nested the category or function will be.
        
        Returns
        -------
        new : ``SlasherApplicationCommandFunction``, ``SlasherApplicationCommandCategory``
        """
        command = self._command
        if (command is not None):
            return command
        
        return SlasherApplicationCommandCategory(self, deepness)
    
    
    def copy(self):
        """
        Copies the slash command.
        
        Returns
        -------
        new : ``ApplicationCommand``
        """
        command = self._command
        if (command is not None):
            command = command.copy()
        
        sub_commands = self._sub_commands
        if (sub_commands is not None):
            sub_commands = {category_name: category.copy() for category_name, category in sub_commands.items()}
        
        guild_ids = self.guild_ids
        if (guild_ids is not None):
            guild_ids = guild_ids.copy()
        
        new = object.__new__(type(self))
        new._command = command
        new._sub_commands = sub_commands
        new._registered_application_command_ids = None
        new._schema = None
        new.description = self.description
        new.guild_ids = guild_ids
        new.is_global = self.is_global
        new.name = self.name
        new._unloading_behaviour = self._unloading_behaviour
        new.allow_by_default = self.allow_by_default
        
        permission_overwrites = self._permission_overwrites
        if (permission_overwrites is not None):
            permission_overwrites = {
                guild_id: permission_overwrite.copy() for
                guild_id, permission_overwrite in permission_overwrites.items()
            }
        
        new._permission_overwrites = permission_overwrites
        
        new.target = self.target
        
        auto_completers = self._auto_completers
        if (auto_completers is not None):
            auto_completers = auto_completers.copy()
        new._auto_completers = auto_completers
        
        exception_handlers = self._exception_handlers
        if (exception_handlers is not None):
            exception_handlers = exception_handlers.copy()
        new._exception_handlers = exception_handlers
        
        new._self_reference = None
        
        if (sub_commands is not None):
            for sub_command in sub_commands.values():
                sub_command._parent_reference = new._get_self_reference()
        
        return new
    
    
    @property
    def interactions(self):
        """
        Enables you to add sub-commands or sub-categories to the slash command.
        
        Returns
        -------
        handler : ``_EventHandlerManager``
        
        Raises
        ------
        RuntimeError
            The ``SlasherApplicationCommand`` is not a category.
        """
        if self._command is not None:
            raise RuntimeError(
                f'The {self.__class__.__name__} is not a category.'
            )
        
        return _EventHandlerManager(self)
    
    
    def create_event(self, func, *args, **kwargs):
        """
        Adds a sub-command under the slash command.
        
        Parameters
        ----------
        func : `async-callable`
            The function used as the command when using the respective slash command.
        *args : Positional Parameters
            Positional parameters to pass to ``SlasherApplicationCommand``'s constructor.
        **kwargs : Keyword parameters
            Keyword parameters to pass to the ``SlasherApplicationCommand``'s constructor.
        
        Returns
        -------
        self : ``SlasherApplicationCommandFunction``, ``SlasherApplicationCommandCategory``
        
        Raises
        ------
        TypeError
            If Any parameter's type is incorrect.
        ValueError
            If Any parameter's value is incorrect.
        RuntimeError
            - The ``SlasherApplicationCommand`` is not a category.
            - The ``SlasherApplicationCommand`` reached the maximal amount of children.
            - If the command to add is a default sub-command meanwhile the category already has one.
        """
        if self._command is not None:
            raise RuntimeError(f'The {self!r} is not a category.')
        
        if isinstance(func, Router):
            func = func[0]
        
        if isinstance(func, type(self)):
            self._add_application_command(func)
            return self
        
        command = type(self)(func, *args, **kwargs)
        
        if isinstance(command, Router):
            command = command[0]
        
        return self._add_application_command(command)
    
    
    def create_event_from_class(self, klass):
        """
        Breaks down the given class to it's class attributes and tries to add it as a sub-command or sub-category.
        
        Parameters
        ----------
        klass : `type`
            The class, from what's attributes the command will be created.
        
        Returns
        -------
        self : ``SlasherApplicationCommandFunction``, ``SlasherApplicationCommandCategory``
         
        Raises
        ------
        TypeError
            If Any attribute's type is incorrect.
        ValueError
            If Any attribute's value is incorrect.
        RuntimeError
            - The ``SlasherApplicationCommand`` is not a category.
            - The ``SlasherApplicationCommand`` reached the maximal amount of children.
            - If the command to add is a default sub-command meanwhile the category already has one.
        """
        command = type(self).from_class(klass)
        
        if isinstance(command, Router):
            command = command[0]
        
        return self._add_application_command(command)
    
    
    def _add_application_command(self, command):
        """
        Adds a sub-command or sub-category to the slash command.
        
        Parameters
        ----------
        command : ``SlasherApplicationCommand``
            The slash command to add.
        
        Raises
        ------
        RuntimeError
            - The ``SlasherApplicationCommand`` reached the maximal amount of children.
            - If the command to add is a default sub-command meanwhile the category already has one.
        """
        sub_commands = self._sub_commands
        if len(sub_commands) == APPLICATION_COMMAND_OPTIONS_MAX and (command.name not in sub_commands):
            raise RuntimeError(
                f'The {self!r} reached the maximal amount of children '
                f'({APPLICATION_COMMAND_OPTIONS_MAX}).'
            )
        
        if command.is_default:
            for sub_command in sub_commands.values():
                if sub_command.is_default:
                    raise RuntimeError(
                        f'{self!r} already has a default command.'
                    )
        
        as_sub = command.as_sub(APPLICATION_COMMAND_CATEGORY_DEEPNESS_START)
        as_sub._parent_reference = self._get_self_reference()
        
        sub_commands[as_sub.name] = as_sub
        _reset_slasher_application_command_schema(self)
        
        auto_completers = self._auto_completers
        if (auto_completers is not None):
            for auto_completer in auto_completers:
                as_sub._try_resolve_auto_completer(auto_completer)
        
        return as_sub
    
    
    def __eq__(self, other):
        """Returns whether the two slash commands are the same."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self._command != other._command:
            return False
        
        if self._sub_commands != other._sub_commands:
            return False
        
        if self._unloading_behaviour != other._unloading_behaviour:
            return False
        
        if self.description != other.description:
            return False
        
        if self.guild_ids != other.guild_ids:
            return False
        
        if self.is_default != other.is_default:
            return False
        
        if self.is_global != other.is_global:
            return False
        
        if self.name != other.name:
            return False
        
        if self.allow_by_default != other.allow_by_default:
            return False
        
        if self._permission_overwrites != other._permission_overwrites:
            return False
        
        if self.target is not other.target:
            return False
        
        if self._auto_completers != other._auto_completers:
            return False
        
        if self._exception_handlers != other._exception_handlers:
            return False
        
        return True
    
    
    def add_permission_overwrite(self, guild_id, permission_overwrite):
        """
        Adds an overwrite to the slash command.
        
        Parameters
        ----------
        guild_id : `int`
            The guild's id where the overwrite will be applied.
        permission_overwrite : ``ApplicationCommandPermissionOverwrite``, `None`
            The permission overwrite to add
        
        Raises
        ------
        AssertionError
            - Each command in each guild can have up to `10` overwrite, which is already reached.
        """
        permission_overwrites = self._permission_overwrites
        if permission_overwrites is None:
            self._permission_overwrites = permission_overwrites = {}
        
        permission_overwrites_for_guild = permission_overwrites.get(guild_id, None)
        
        if __debug__:
            if (
                (permission_overwrites_for_guild is not None) and
                (len(permission_overwrites_for_guild) >= APPLICATION_COMMAND_PERMISSION_OVERWRITE_MAX)
            ):
                raise AssertionError(
                    f'`Each command in each guild can have up to '
                    f'{APPLICATION_COMMAND_PERMISSION_OVERWRITE_MAX} permission overwrites which is already reached.'
                )
        
        if (permission_overwrites_for_guild is not None) and (permission_overwrite is not None):
            target_id = permission_overwrite.target_id
            for index in range(len(permission_overwrites_for_guild)):
                iter_permission_overwrites = permission_overwrites_for_guild[index]
                
                if iter_permission_overwrites.target_id != target_id:
                    continue
                
                if permission_overwrite.allow == iter_permission_overwrites.allow:
                    return
                
                del permission_overwrites_for_guild[index]
                
                if permission_overwrites_for_guild:
                    return
                
                permission_overwrites[guild_id] = None
                return
        
        if permission_overwrite is None:
            if permission_overwrites_for_guild is None:
                permission_overwrites[guild_id] = None
        else:
            if permission_overwrites_for_guild is None:
                permission_overwrites[guild_id] = permission_overwrites_for_guild = []
            
            permission_overwrites_for_guild.append(permission_overwrite)
    
    
    def get_permission_overwrites_for(self, guild_id):
        """
        Returns the slash command's permissions overwrites for the given guild.
        
        Returns
        -------
        permission_overwrites : `None`, `list` of ``ApplicationCommandPermissionOverwrite``
            Returns `None` instead of an empty list.
        """
        permission_overwrites = self._permission_overwrites
        if (permission_overwrites is not None):
            return permission_overwrites.get(guild_id, None)
    
    
    def _get_permission_sync_ids(self):
        """
        Gets the permission overwrite guild id-s which should be synced.
        
        Returns
        -------
        permission_sync_ids : `set` of `int`
        """
        permission_sync_ids = set()
        guild_ids = self.guild_ids
        # If the command is guild bound, sync it in every guild, if not, then sync it in every guild where it has an
        # a permission overwrite.
        if (guild_ids is None):
            permission_overwrites = self._permission_overwrites
            if (permission_overwrites is not None):
                permission_sync_ids.update(permission_overwrites.keys())
        else:
            permission_sync_ids.update(guild_ids)
        
        return permission_sync_ids
    
    
    def get_real_command_count(self):
        """
        Gets the real command count of the slasher application command. This includes every sub attached to it as well.
        
        Returns
        -------
        real_command_count: `int`
        """
        if (self._command is None):
            sub_commands = self._sub_commands
            real_command_count = 0
            
            if (sub_commands is not None):
                for sub_command_or_category in sub_commands.values():
                    if isinstance(sub_command_or_category, SlasherApplicationCommandFunction):
                        real_command_count += 1
                    else:
                        # Nesting more is not allowed by Discord.
                        real_command_count += len(sub_command_or_category._sub_commands)
        
        else:
            real_command_count = 1
        
        return real_command_count
    
    
    def autocomplete(self, parameter_name, *parameter_names, function=None):
        """
        Registers an auto completer function to the application command.
        
        Can be used as a decorator, as:
        
        ```py
        @bot.interactions(is_global=True)
        async def buy(
            item: ('str', 'Select an item to buy.'),
        ):
            return 'Great success.'
        
        AUTO_COMPLETE_CHOICES = (
            'cake',
            'shrimp fry',
        )
        
        @buy.autocomplete('item')
        async def autocomplete_item_parameter(value):
            if value is None:
                return AUTO_COMPLETE_CHOICES[:20]
            
            value = value.lower()
            
            return [choice for choice in AUTO_COMPLETE_CHOICES if choice.startswith(value)]
        ```
        
        Parameters
        ----------
        parameter_name : `str`
            The parameter's name.
        *parameter_names : `str`
            Additional parameter names to autocomplete
        function : `None`, `async-callable` = `None`, Optional (Keyword only)
            The function to register as auto completer.
        
        Returns
        -------
        function / wrapper : `async-callable`, `functools.partial`
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
        parameter_names = _build_auto_complete_parameter_names(parameter_name, parameter_names)
        
        if (function is None):
            return partial_func(_register_autocomplete_function, self, parameter_names)
        
        return self._add_autocomplete_function(parameter_names, function)
    
    
    def _add_autocomplete_function(self, parameter_names, function):
        """
        Registers an autocomplete function.
        
        Parameters
        ----------
        parameter_names : `list` of `str`
            The parameters' names.
        function : `async-callable`
            The function to register as auto completer.
        
        Returns
        -------
        auto_completer : ``SlasherApplicationCommandParameterAutoCompleter``
            The registered auto completer
        
        Raises
        ------
        RuntimeError
            - If the application command function has no parameter named, like `parameter_name`.
            - If the parameter cannot be auto completed.
        TypeError
            If `function` is not an asynchronous.
        """
        if isinstance(function, SlasherApplicationCommandParameterAutoCompleter):
            function = function._command
        
        command_function = self._command
        if command_function is None:
            
            auto_completer = SlasherApplicationCommandParameterAutoCompleter(
                function,
                parameter_names,
                APPLICATION_COMMAND_DEEPNESS,
                self,
            )
            
            # If it is none, try to resolve the parameters in sub commands.
            auto_completers = self._auto_completers
            if (auto_completers is None):
                auto_completers = []
                self._auto_completers = auto_completers
            
            auto_completers.append(auto_completer)
            
            sub_commands = self._sub_commands
            if (sub_commands is not None):
                for sub_command in sub_commands.values():
                    sub_command._try_resolve_auto_completer(auto_completer)
        
        else:
            auto_completer = command_function._add_autocomplete_function(parameter_names, function)
        
        _reset_slasher_application_command_schema(self)
        
        return auto_completer
    
    
    def error(self, exception_handler=None, *, first=False):
        """
        Registers an exception handler to the ``SlasherApplicationCommand``.
        
        Parameters
        ----------
        exception_handler : `None`, `CoroutineFunction` = `None`, Optional
            Exception handler to register.
        first : `bool` = `False`, Optional (Keyword Only)
            Whether the exception handler should run first.
        
        Returns
        -------
        exception_handler / wrapper : `CoroutineFunction` / `functools.partial`
            If `exception_handler` is not given, returns a wrapper.
        """
        if exception_handler is None:
            return partial_func(_register_exception_handler, first)
        
        return self._register_exception_handler(exception_handler, first)
    
    
    def _register_exception_handler(self, exception_handler, first):
        """
        Registers an exception handler to the ``SlasherApplicationCommand``.
        
        Parameters
        ----------
        exception_handler : `CoroutineFunction`
            Exception handler to register.
        first : `bool`
            Whether the exception handler should run first.
        
        Returns
        -------
        exception_handler : `CoroutineFunction`
        """
        test_exception_handler(exception_handler)
        
        exception_handlers = self._exception_handlers
        if exception_handlers is None:
            self._exception_handlers = exception_handlers = []
        
        if first:
            exception_handlers.insert(0, exception_handler)
        else:
            exception_handlers.append(exception_handler)
        
        return exception_handler
    
    
    def _get_self_reference(self):
        """
        Gets a weak reference to the ``SlasherApplicationCommand``.
        
        Returns
        -------
        self_reference : ``WeakReferer`` to ``SlasherApplicationCommand``
        """
        self_reference = self._self_reference
        if self_reference is None:
            self_reference = WeakReferer(self)
            self._self_reference = self_reference
        
        return self_reference
    
    
    def _try_resolve_auto_completer(self, auto_completer):
        """
        Tries to register auto completer to the slasher application command.
        
        Parameters
        ----------
        auto_completer : ``SlasherApplicationCommandParameterAutoCompleter``
            The auto completer.
        
        Returns
        -------
        resolved : `int`
            The amount of parameters resolved.
        """
        resolved = 0
        
        command = self._command
        if command is None:
            sub_commands = self._sub_commands
            if (sub_commands is not None):
                for sub_command in sub_commands.values():
                    resolved += sub_command._try_resolve_auto_completer(auto_completer)
        else:
            resolved += command._try_resolve_auto_completer(auto_completer)
        
        if resolved:
            _reset_slasher_application_command_schema(self)
        
        return resolved


class SlasherApplicationCommandFunction:
    """
    Represents an application command's backend implementation.
    
    Attributes
    ----------
    _auto_completers : `None`, `list` of ``SlasherApplicationCommandParameterAutoCompleter``
        Auto completer functions.
    _command : `async-callable˛
        The command's function to call.
    _exception_handlers : `None`, `list` of `CoroutineFunction`
        Exception handlers added with ``.error`` to the interaction handler.
        
        Same as ``Slasher._exception_handlers``.
    
    _parameter_converters : `tuple` of ``ParameterConverter``
        Parsers to parse command parameters.
    _parent_reference : `None`, ``WeakReferer`` to (``SlasherApplicationCommand``,
            ``SlasherApplicationCommandCategory``)
        Reference to the parent application command or category.
    _self_reference : `None`, ``WeakReferer`` to ``SlasherApplicationCommandFunction``
        Back reference to the slasher application command function.
        
        Used by auto completers to access the parent entity.
    
    description : `str`
        The slash command's description.
    is_default : `bool`
        Whether the command is the default command in it's category.
    name : `str`
        The name of the slash command. It's length can be in range [1:32].
    response_modifier : `None`, ``ResponseModifier``
        Modifies values returned and yielded to command coroutine processor.
    """
    __slots__ = (
        '__weakref__', '_auto_completers', '_command', '_exception_handlers', '_parameter_converters',
        '_parent_reference', '_self_reference', 'category', 'description', 'is_default', 'name',
        'response_modifier'
    )
    
    def __new__(cls, command, parameter_converters, name, description, response_modifier, is_default):
        """
        Creates a new ``SlasherApplicationCommandFunction`` with the given parameters.
        
        Parameters
        ----------
        command : `async-callable`
            The command's function to call.
        parameter_converters : `tuple` of ``ParameterConverter``
            Parsers to parse command parameters.
        name : `str`
            The name of the slash command.
        description : `str`
            The slash command's description.
        response_modifier : `None`, ``ResponseModifier``
            Modifies values returned and yielded to command coroutine processor.
        is_default : `bool`
            Whether the command is the default command in it's category.
        """
        self = object.__new__(cls)
        self._auto_completers = None
        self._command = command
        self._parameter_converters = parameter_converters
        self.response_modifier = response_modifier
        self.description = description
        self.name = name
        self.is_default = is_default
        self._exception_handlers = None
        self._parent_reference = None
        self._self_reference = None
        
        return self
    
    
    async def __call__(self, client, interaction_event, options):
        """
        Calls the slash command function.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client who received the event.
        interaction_event : ``InteractionEvent``
            The received interaction event.
        options : `None`, `list` of ``InteractionEventChoice``
            Options bound to the function.
        
        Raises
        ------
        SlasherApplicationCommandParameterConversionError
            Exception occurred meanwhile parsing parameter.
        """
        parameters = []
        
        parameter_relation = {}
        if (options is not None):
            for option in options:
                parameter_relation[option.name] = option.value
        
        for parameter_converter in self._parameter_converters:
            if isinstance(parameter_converter, InternalParameterConverter):
                value = None
            else:
                value = parameter_relation.get(parameter_converter.name, None)
            
            try:
                parameter = await parameter_converter(client, interaction_event, value)
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
            
        
        command_coroutine = self._command(*parameters)
        
        try:
            await process_command_coroutine(
                client,
                interaction_event,
                self.response_modifier,
                command_coroutine,
            )
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
    
    
    async def call_auto_completion(self, client, interaction_event, auto_complete_option):
        """
        Calls the respective auto completion function of the slasher application command function.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client who received the event.
        interaction_event : ``InteractionEvent``
            The received interaction event.
        auto_complete_option : ``ApplicationCommandAutocompleteInteraction`` or \
                ``ApplicationCommandAutocompleteInteractionOption``
            The option to autocomplete.
        """
        focused_option = auto_complete_option.focused_option
        if (focused_option is None):
            return
        
        parameter_name = focused_option.name
        
        for parameter_converter in self._parameter_converters:
            if isinstance(parameter_converter, SlashCommandParameterConverter):
                if parameter_converter.name == parameter_name:
                    break
        else:
            return
        
        auto_completer = parameter_converter.auto_completer
        if (auto_completer is not None):
            await auto_completer(client, interaction_event)
        
    
    def _get_auto_completable_parameters(self):
        """
        Gets the auto completable parameter converters of the application command function.
        
        Returns
        -------
        parameter_converters : `list` of ``SlashCommandParameterConverter``
        """
        auto_completable_parameters = set()
        
        for parameter_converter in self._parameter_converters:
            if (
                isinstance(parameter_converter, SlashCommandParameterConverter) and
                parameter_converter.can_auto_complete()
            ):
                auto_completable_parameters.add(parameter_converter)
        
        return auto_completable_parameters
    
    def __repr__(self):
        """Returns the application command option's representation."""
        repr_parts = [
            '<', self.__class__.__name__,
            ' name=', repr(self.name),
            ', description=', repr(self.description),
        ]
        
        if self.is_default:
            repr_parts.append(', is_default=True')
        
        response_modifier = self.response_modifier
        if (response_modifier is not None):
            repr_parts.append(', response_modifier')
            repr_parts.append(repr(response_modifier))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    def as_option(self):
        """
        Returns the slash command function as an application command option.
        
        Returns
        -------
        option : ``ApplicationCommandOption``
        """
        parameter_converters = self._parameter_converters
        options = None
        for parameter_converter in parameter_converters:
            option = parameter_converter.as_option()
            if (option is not None):
                if options is None:
                    options = []
                
                options.append(option)
        
        return ApplicationCommandOption(self.name, self.description, ApplicationCommandOptionType.sub_command,
            options=options, default=self.is_default)
    
    
    def copy(self):
        """
        Copies the slash command function.
        
        Returns
        -------
        self : ``SlasherApplicationCommandFunction``
        """
        new = object.__new__(type(self))
        new._command = self._command
        new._parameter_converters = self._parameter_converters
        new.response_modifier = self.response_modifier
        new.description = self.description
        new.name = self.name
        new.is_default = self.is_default
        
        auto_completers = self._auto_completers
        if (auto_completers is not None):
            auto_completers = auto_completers.copy()
        new._auto_completers = auto_completers
        
        exception_handlers = self._exception_handlers
        if (exception_handlers is not None):
            exception_handlers = exception_handlers.copy()
        new._exception_handlers = exception_handlers
        
        new._parent_reference = self._parent_reference
        new._self_reference = None
        
        return self
    
    
    def __eq__(self, other):
        """Returns whether the two slash command functions are equal."""
        if type(self) is not type(other):
            return False
        
        if self._command != other._command:
            return False
        
        if self._parameter_converters != other._parameter_converters:
            return False
        
        if self.response_modifier != other.response_modifier:
            return False
        
        if self.description != other.description:
            return False
        
        if self.name != other.name:
            return False
        
        if self.is_default != other.is_default:
            return False
        
        if self._auto_completers != other._auto_completers:
            return False
        
        if self._exception_handlers != other._exception_handlers:
            return False
        
        return True
    
    
    def autocomplete(self, parameter_name, *parameter_names, function=None):
        """
        Registers an auto completer function to the application command.
        
        Parameters
        ----------
        parameter_name : `str`
            The parameter's name.
        *parameter_names : `str`
            Additional parameter names to autocomplete
        function : `None`, `callable` = `None`, Optional (Keyword only)
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
        parameter_names = _build_auto_complete_parameter_names(parameter_name, parameter_names)
        
        if (function is None):
            return partial_func(_register_autocomplete_function, self, parameter_names)
        
        return self._add_autocomplete_function(parameter_names, function)
    
    
    @copy_docs(SlasherApplicationCommand._add_autocomplete_function)
    def _add_autocomplete_function(self, parameter_names, function):
        if isinstance(function, SlasherApplicationCommandParameterAutoCompleter):
            function = function._command
        
        auto_completer = SlasherApplicationCommandParameterAutoCompleter(
            function,
            parameter_names,
            APPLICATION_COMMAND_FUNCTION_DEEPNESS,
            self,
        )
        
        auto_completable_parameters = self._get_auto_completable_parameters()
        matched_auto_completable_parameters = auto_completer._difference_match_parameters(auto_completable_parameters)
        if not matched_auto_completable_parameters:
            raise RuntimeError(
                f'Application command function `{self.name}` has no parameter matching any '
                f'parameters of `{auto_completer!r}`.'
            )
        
        auto_completers = self._auto_completers
        if (auto_completers is None):
            auto_completers = []
            self._auto_completers = auto_completers
        
        auto_completers.append(auto_completer)
        
        for parameter_converter in matched_auto_completable_parameters:
            parameter_converter.register_auto_completer(auto_completer)
        
        return auto_completer
    
    
    def _try_resolve_auto_completer(self, auto_completer):
        """
        Tries to register auto completer to the slasher application command function.
        
        Parameters
        ----------
        auto_completer : ``SlasherApplicationCommandParameterAutoCompleter``
            The auto completer.
        
        Returns
        -------
        resolved : `int`
            The amount of parameters resolved.
        """
        resolved = 0
        
        auto_completable_parameters = self._get_auto_completable_parameters()
        matched_auto_completable_parameters = auto_completer._difference_match_parameters(auto_completable_parameters)
        for parameter_converter in matched_auto_completable_parameters:
            resolved += parameter_converter.register_auto_completer(auto_completer)
        
        return resolved
    
    
    def error(self, exception_handler=None, *, first=False):
        """
        Registers an exception handler to the ``SlasherApplicationCommandFunction``.
        
        Parameters
        ----------
        exception_handler : `None`, `CoroutineFunction` = `None`, Optional
            Exception handler to register.
        first : `bool` = `False`, Optional (Keyword Only)
            Whether the exception handler should run first.
        
        Returns
        -------
        exception_handler / wrapper : `CoroutineFunction` / `functools.partial`
            If `exception_handler` is not given, returns a wrapper.
        """
        if exception_handler is None:
            return partial_func(_register_exception_handler, first)
        
        return self._register_exception_handler(exception_handler, first)
    
    
    def _register_exception_handler(self, exception_handler, first):
        """
        Registers an exception handler to the ``SlasherApplicationCommandFunction``.
        
        Parameters
        ----------
        exception_handler : `CoroutineFunction`
            Exception handler to register.
        first : `bool`
            Whether the exception handler should run first.
        
        Returns
        -------
        exception_handler : `CoroutineFunction`
        """
        test_exception_handler(exception_handler)
        
        exception_handlers = self._exception_handlers
        if exception_handlers is None:
            self._exception_handlers = exception_handlers = []
        
        if first:
            exception_handlers.insert(0, exception_handler)
        else:
            exception_handlers.append(exception_handler)
        
        return exception_handler
    
    
    def _get_self_reference(self):
        """
        Gets a weak reference to the ``SlasherApplicationCommandFunction``.
        
        Returns
        -------
        self_reference : ``WeakReferer`` to ``SlasherApplicationCommandFunction``
        """
        self_reference = self._self_reference
        if self_reference is None:
            self_reference = WeakReferer(self)
            self._self_reference = self_reference
        
        return self_reference


class SlasherApplicationCommandCategory:
    """
    Represents an application command's backend implementation.
    
    Attributes
    ----------
    _auto_completers : `None`, `list` of ``SlasherApplicationCommandParameterAutoCompleter``
        Auto completer functions by.
    _deepness : `int`
        How nested the category is.
    _exception_handlers : `None`, `list` of `CoroutineFunction`
        Exception handlers added with ``.error`` to the interaction handler.
        
        Same as ``Slasher._exception_handlers``.
    
    _self_reference : ``WeakReferer`` to ``SlasherApplicationCommandCategory``
        Back reference to the slasher application command category.
        
        Used by sub commands to access the parent entity.
    
    _sub_commands : `dict` of (`str`, ``SlasherApplicationCommandFunction``) items
        The sub-commands of the category.
    _parent_reference : `None`, ``WeakReferer`` to ``SlasherApplicationCommand``
        The parent slash command of the category if any.
    description : `str`
        The slash command's description.
    is_default : `bool`
        Whether the command is the default command in it's category.
    name : `str`
        The name of the slash sub-category.
    """
    __slots__ = (
        '__weakref__', '_auto_completers', '_deepness', '_exception_handlers', '_self_reference', '_sub_commands',
        '_parent_reference', 'description', 'is_default', 'name'
    )
    
    def __new__(cls, slasher_application_command, deepness):
        """
        Creates a new ``SlasherApplicationCommandCategory`` with the given parameters.
        
        Parameters
        ----------
        slasher_application_command : ``SlasherApplicationCommand``
            The parent slash command.
        """
        if deepness > APPLICATION_COMMAND_CATEGORY_DEEPNESS_MAX:
            raise RuntimeError('Cannot add anymore sub-category under sub-categories.')
        
        self = object.__new__(cls)
        self.name = slasher_application_command.name
        self.description = slasher_application_command.description
        self._sub_commands = {}
        self._parent_reference = None
        self.is_default = slasher_application_command.is_default
        self._auto_completers = None
        self._deepness = deepness
        self._exception_handlers = None
        self._self_reference = None
        
        return self
    
    
    async def __call__(self, client, interaction_event, options):
        """
        Calls the slash command category.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client who received the event.
        interaction_event : ``InteractionEvent``
            The received interaction event.
        options : `None`, `list` of ``InteractionEventChoice``
            Options bound to the category.
        """
        if (options is None) or len(options) != 1:
            return
        
        option = options[0]
        
        try:
            sub_command = self._sub_commands[option.name]
        except KeyError:
            pass
        else:
            await sub_command(client, interaction_event, option.options)
            return
        
        # Do not put this into the `except` branch.
        await handle_command_exception(
            self,
            client,
            interaction_event,
            SlasherApplicationCommandParameterConversionError(
                None,
                option.name,
                'sub-command',
                list(self._sub_commands.keys()),
            )
        )
        return
    
    @copy_docs(SlasherApplicationCommand.call_auto_completion)
    async def call_auto_completion(self, client, interaction_event, auto_complete_option):
        auto_complete_option_type = auto_complete_option.type
        if (
            (auto_complete_option_type is APPLICATION_COMMAND_OPTION_TYPE_SUB_COMMAND) or
            (auto_complete_option_type is APPLICATION_COMMAND_OPTION_TYPE_SUB_COMMAND_CATEGORY)
        ):
            options = auto_complete_option.options
            if (options is not None):
                option = options[0]
                sub_commands = self._sub_commands
                if (sub_commands is not None):
                    try:
                        sub_command = sub_commands[option.name]
                    except KeyError:
                        pass
                    else:
                        await sub_command.call_auto_completion(client, interaction_event, option)
    
    
    def as_option(self):
        """
        Returns the slash command category as an application command option.
        
        Returns
        -------
        option : ``ApplicationCommandOption``
        """
        sub_commands = self._sub_commands
        if sub_commands:
            options = [sub_command.as_option() for sub_command in sub_commands.values()]
        else:
            options = None
        
        return ApplicationCommandOption(self.name, self.description, ApplicationCommandOptionType.sub_command_group,
            options=options, default=self.is_default)
    
    
    def copy(self):
        """
        Copies the slash command category.
        
        Returns
        -------
        new : ``SlasherApplicationCommandCategory``
        """
        sub_commands = {category_name: category.copy() for category_name, category in self._sub_commands.items()}
        
        new = object.__new__(type(self))
        new._sub_commands = sub_commands
        new.description = self.description
        new.name = self.name
        new._parent_reference = None
        
        auto_completers = self._auto_completers
        if (auto_completers is not None):
            auto_completers = auto_completers.copy()
        new._auto_completers = auto_completers
        
        exception_handlers = self._exception_handlers
        if (exception_handlers is not None):
            exception_handlers = exception_handlers.copy()
        new._exception_handlers = exception_handlers
        
        new._self_reference = None
        
        return new
    
    
    @property
    def interactions(self):
        """
        Enables you to add sub-commands under the sub-category.
        
        Returns
        -------
        handler : ``_EventHandlerManager``
        """
        return _EventHandlerManager(self)
    
    
    def create_event(self, func, *args, **kwargs):
        """
        Adds a sub-command under the slash category.
        
        Parameters
        ----------
        func : `async-callable`
            The function used as the command when using the respective slash command.
        *args : Positional Parameters
            Positional parameters to pass to ``SlasherApplicationCommand``'s constructor.
        **kwargs : Keyword parameters
            Keyword parameters to pass to the ``SlasherApplicationCommand``'s constructor.
        
        Returns
        -------
        self : ``SlasherApplicationCommandCategory``
        
        Raises
        ------
        TypeError
            If Any parameter's type is incorrect.
        ValueError
            If Any parameter's value is incorrect.
        RuntimeError
            - The ``SlasherApplicationCommand`` reached the maximal amount of children.
            - Cannot add anymore sub-category under sub-categories.
            - If the command to add is a default sub-command meanwhile the category already has one.
        """
        if isinstance(func, Router):
            func = func[0]
        
        if isinstance(func, SlasherApplicationCommand):
            self._add_application_command(func)
            return self
        
        command = SlasherApplicationCommand(func, *args, **kwargs)
        if isinstance(command, Router):
            command = command[0]
        
        return self._add_application_command(command)
    
    
    def create_event_from_class(self, klass):
        """
        Breaks down the given class to it's class attributes and tries to add it as a sub-command.
        
        Parameters
        ----------
        klass : `type`
            The class, from what's attributes the command will be created.
        
        Returns
        -------
        self : ``SlasherApplicationCommandCategory``
         
        Raises
        ------
        TypeError
            If Any attribute's type is incorrect.
        ValueError
            If Any attribute's value is incorrect.
        RuntimeError
            - The ``SlasherApplicationCommand`` reached the maximal amount of children.
            - Cannot add anymore sub-category under sub-categories.
            - If the command to add is a default sub-command meanwhile the category already has one.
        """
        command = create_event_from_class(SlasherApplicationCommand, klass, SLASH_COMMAND_PARAMETER_NAMES,
            SLASH_COMMAND_NAME_NAME, SLASH_COMMAND_COMMAND_NAME)
        
        if isinstance(command, Router):
            command = command[0]
        
        return self._add_application_command(command)
    
    
    def _add_application_command(self, command):
        """
        Adds a sub-command or sub-category to the slash command.
        
        Parameters
        ----------
        command : ``SlasherApplicationCommand``
            The slash command to add.
        
        Returns
        -------
        as_sub : ``SlasherApplicationCommandFunction``, ``SlasherApplicationCommandCategory``
            The command as sub-command.
        
        Raises
        ------
        RuntimeError
            - The ``SlasherApplicationCommand`` reached the maximal amount of children.
            - Cannot add anymore sub-category under sub-categories.
            - If the command to add is a default sub-command meanwhile the category already has one.
        """
        sub_commands = self._sub_commands
        if len(sub_commands) == APPLICATION_COMMAND_OPTIONS_MAX and (command.name not in sub_commands):
            raise RuntimeError(
                f'The {self.__class__.__name__} reached the maximal amount of children '
                f'({APPLICATION_COMMAND_OPTIONS_MAX}).'
            )
        
        as_sub = command.as_sub(self._deepness + 1)
        
        if command.is_default:
            for sub_command in sub_commands.values():
                if sub_command.is_default:
                    raise RuntimeError(
                        f'{self!r} already ha  default command.'
                    )
        
        as_sub._parent_reference = self._get_self_reference()
        sub_commands[command.name] = as_sub
        
        _reset_parent_schema(self)
        
        # Resolve auto completers recursively
        parent = self
        while True:
            auto_completers = parent._auto_completers
            if (auto_completers is not None):
                for auto_completer in auto_completers:
                    as_sub._try_resolve_auto_completer(auto_completer)
            
            if isinstance(parent, Slasher):
                break
            
            parent_reference = parent._parent_reference
            if (parent_reference is None):
                break
            
            parent = parent_reference()
            if (parent is None):
                break
        
        return as_sub
    
    def __eq__(self, other):
        """Returns whether the two slash commands categories are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.name != other.name:
            return False
        
        if self.description != other.description:
            return False
        
        if self._sub_commands != other._sub_commands:
            return False
        
        if self.is_default != other.is_default:
            return False
        
        if self._auto_completers != other._auto_completers:
            return False
        
        if self._exception_handlers != other._exception_handlers:
            return False
        
        return True
    
    
    def autocomplete(self, parameter_name, *parameter_names, function=None):
        """
        Registers an auto completer function to the application command.
        
        Parameters
        ----------
        parameter_name : `str`
            The parameter's name.
        *parameter_names : `str`
            Additional parameter names to autocomplete
        function : `None`, `callable` = `None`, Optional (Keyword only)
            The function to register as auto completer.
        
        Returns
        -------
        function / wrapper : `async-callable`, `functools.partial`
            The registered function if given or a wrapper to register the function with.
        """
        parameter_names = _build_auto_complete_parameter_names(parameter_name, parameter_names)
        
        if (function is None):
            return partial_func(_register_autocomplete_function, self, parameter_names)
            
        return self._add_autocomplete_function(parameter_names, function)
    
    
    @copy_docs(SlasherApplicationCommand._add_autocomplete_function)
    def _add_autocomplete_function(self, parameter_names, function):
        if isinstance(function, SlasherApplicationCommandParameterAutoCompleter):
            function = function._command
        
        auto_completer = SlasherApplicationCommandParameterAutoCompleter(
            function,
            parameter_names,
            self._deepness,
            self,
        )
        
        auto_completers = self._auto_completers
        if (auto_completers is None):
            auto_completers = []
            self._auto_completers = auto_completers
        
        auto_completers.append(auto_completer)
        
        resolved = 0
        sub_commands = self._sub_commands
        for sub_command in sub_commands.values():
            resolved += sub_command._try_resolve_auto_completer(auto_completer)
        
        if resolved:
            _reset_parent_schema(self)
        
        return auto_completer
    
    
    def _try_resolve_auto_completer(self, auto_completer):
        """
        Tries to register auto completer to the slasher application command function.
        
        Parameters
        ----------
        auto_completer : ``SlasherApplicationCommandParameterAutoCompleter``
            The auto completer.
        
        Returns
        -------
        resolved : `int`
            The amount of parameters resolved.
        """
        resolved = 0
        for sub_command in self._sub_commands.values():
             resolved += sub_command._try_resolve_auto_completer(auto_completer)
        
        return resolved
    
    
    def error(self, exception_handler=None, *, first=False):
        """
        Registers an exception handler to the ``SlasherApplicationCommandCategory``.
        
        Parameters
        ----------
        exception_handler : `None`, `CoroutineFunction` = `None`, Optional
            Exception handler to register.
        first : `bool` = `False`, Optional (Keyword Only)
            Whether the exception handler should run first.
        
        Returns
        -------
        exception_handler / wrapper : `CoroutineFunction` / `functools.partial`
            If `exception_handler` is not given, returns a wrapper.
        """
        if exception_handler is None:
            return partial_func(_register_exception_handler, first)
        
        return self._register_exception_handler(exception_handler, first)
    
    
    def _register_exception_handler(self, exception_handler, first):
        """
        Registers an exception handler to the ``SlasherApplicationCommandCategory``.
        
        Parameters
        ----------
        exception_handler : `CoroutineFunction`
            Exception handler to register.
        first : `bool`
            Whether the exception handler should run first.
        
        Returns
        -------
        exception_handler : `CoroutineFunction`
        """
        test_exception_handler(exception_handler)
        
        exception_handlers = self._exception_handlers
        if exception_handlers is None:
            self._exception_handlers = exception_handlers = []
        
        if first:
            exception_handlers.insert(0, exception_handler)
        else:
            exception_handlers.append(exception_handler)
        
        return exception_handler
    
    
    def _get_self_reference(self):
        """
        Gets a weak reference to the ``SlasherApplicationCommandCategory``.
        
        Returns
        -------
        self_reference : ``WeakReferer`` to ``SlasherApplicationCommandCategory``
        """
        self_reference = self._self_reference
        if self_reference is None:
            self_reference = WeakReferer(self)
            self._self_reference = self_reference
        
        return self_reference


class SlasherApplicationCommandParameterAutoCompleter:
    """
    Represents an application command parameter's auto completer.
    
    Attributes
    ----------
    _command : `async-callable˛
        The command's function to call.
    _exception_handlers : `None`, `list` of `CoroutineFunction`
        Exception handlers added with ``.error`` to the interaction handler.
        
        Same as ``Slasher._exception_handlers``.
    
    _parameter_converters : `tuple` of ``ParameterConverter``
        Parsers to parse command parameters.
    _parent_reference : `None`, ``WeakReferer`` to (``SlasherApplicationCommand``,
            ``SlasherApplicationCommandFunction``, ``SlasherApplicationCommandCategory``)
        The parent slash command of the auto completer, where it was registered to.
    name_pairs : `frozenset` of `tuple` (`str`, `str`)
        Raw - display parameter names, to which the converter should autocomplete.
    deepness : `int`
        How deep the auto completer was created. Deeper auto completers always overwrite higher ones.
    """
    __slots__ = (
        '_command', '_exception_handlers', '_parameter_converters', '_parent_reference', 'deepness', 'name_pairs'
    )
    
    def __new__(cls, function, parameter_names, deepness, parent):
        """
        Creates a new ``SlasherApplicationCommandParameterAutoCompleter`` with the given parameters.
        
        Parameters
        ----------
        function : `async-callable`
            The function to create auto completer from.
        parameter_names : `list` of `str`
            The names, which should be auto completed.
        deepness : `int`
            How deep the auto completer was created.
        parent : `None`, ``Slasher``, ``SlasherApplicationCommand``, ``SlasherApplicationCommandCategory``,
            ``SlasherApplicationCommandFunction``
        """
        command, parameter_converters = get_application_command_parameter_auto_completer_converters(function)
        
        name_pairs = frozenset((name, raw_name_to_display(name)) for name in set(parameter_names))
        
        if parent is None:
            parent_reference = None
        else:
            parent_reference = parent._get_self_reference()
        
        self = object.__new__(cls)
        self._command = command
        self._parameter_converters = parameter_converters
        self.name_pairs = name_pairs
        self.deepness = deepness
        self._parent_reference = parent_reference
        self._exception_handlers = None
        
        return self
    
    
    async def __call__(self, client, interaction_event):
        """
        Calls the parameter auto completer.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client who received the event.
        interaction_event : ``InteractionEvent``
            The received interaction event.
        """
        parameters = []
        
        for parameter_converter in self._parameter_converters:
            parameter = await parameter_converter(client, interaction_event, None)
            parameters.append(parameter)
        
        auto_completer_coroutine = self._command(*parameters)
        
        try:
            await process_auto_completer_coroutine(
                client,
                interaction_event,
                auto_completer_coroutine,
            )
        except BaseException as err:
            exception = err
        else:
            return
        
        # Do not put this into the `except` branch.
        await handle_command_exception(
            self,
            client,
            interaction_event,
            exception,
        )
        return
    
    
    def __repr__(self):
        """Returns the parameter auto completer's representation."""
        repr_parts = ['<', self.__class__.__name__, '>']
        
        repr_parts.append(' name_pairs=')
        repr_parts.append(repr(self.name_pairs))
        
        return ''.join(repr_parts)
    
    
    def _is_deeper_than(self, other):
        """
        Returns whether self is deeper than other.
        
        Parameters
        ----------
        other : ``SlasherApplicationCommandParameterAutoCompleter``
        """
        self_deepness = self.deepness
        if self_deepness == APPLICATION_COMMAND_FUNCTION_DEEPNESS:
            return True
        
        other_deepness = other.deepness
        if other_deepness == APPLICATION_COMMAND_FUNCTION_DEEPNESS:
            return False
        
        if self_deepness > other_deepness:
            return True
        
        return False
    
    
    def _difference_match_parameters(self, auto_completable_parameters):
        """
        Matches auto completable parameters returning a list of the matched ones.
        
        Parameters
        ----------
        auto_completable_parameters : `set` of ``SlashCommandParameterConverter``
            Auto completable parameters.
        
        Returns
        -------
        matched : `list` of ``SlashCommandParameterConverter``
            The matched parameters.
        """
        matched = []
        
        name_pairs = set(self.name_pairs)
        
        for name_pair in list(name_pairs):
            name = name_pair[1]
            
            for parameter in auto_completable_parameters:
                if parameter.name == name:
                    name_pairs.discard(name_pair)
                    matched.append(parameter)
                    auto_completable_parameters.discard(parameter)
                    break
        
        for name_pair in list(name_pairs):
            name = name_pair[0]
            
            for parameter in auto_completable_parameters:
                if parameter.parameter_name == name:
                    name_pairs.discard(name_pair)
                    matched.append(parameter)
                    auto_completable_parameters.discard(parameter)
                    break
        
        return matched
    
    
    def error(self, exception_handler=None, *, first=False):
        """
        Registers an exception handler to the ``SlasherApplicationCommandParameterAutoCompleter``.
        
        Parameters
        ----------
        exception_handler : `None`, `CoroutineFunction` = `True`, Optional
            Exception handler to register.
        first : `bool` = `False`, Optional (Keyword Only)
            Whether the exception handler should run first.
        
        Returns
        -------
        exception_handler / wrapper : `CoroutineFunction` / `functools.partial`
            If `exception_handler` is not given, returns a wrapper.
        """
        if exception_handler is None:
            return partial_func(_register_exception_handler, first)
        
        return self._register_exception_handler(exception_handler, first)
    
    
    def _register_exception_handler(self, exception_handler, first):
        """
        Registers an exception handler to the ``SlasherApplicationCommandParameterAutoCompleter``.
        
        Parameters
        ----------
        exception_handler : `CoroutineFunction`
            Exception handler to register.
        first : `bool`
            Whether the exception handler should run first.
        
        Returns
        -------
        exception_handler : `CoroutineFunction`
        """
        test_exception_handler(exception_handler)
        
        exception_handlers = self._exception_handlers
        if exception_handlers is None:
            self._exception_handlers = exception_handlers = []
        
        if first:
            exception_handlers.insert(0, exception_handler)
        else:
            exception_handlers.append(exception_handler)
        
        return exception_handler
