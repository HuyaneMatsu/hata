__all__ = ('SlashCommand', )

from ...backend.utils import WeakReferer
from ...backend.export import export

from ...discord.events.handling_helpers import route_value, check_name, Router, route_name, _EventHandlerManager, \
    create_event_from_class
from ...discord.guild import Guild
from ...discord.preconverters import preconvert_snowflake, preconvert_bool
from ...discord.client import Client
from ...discord.interaction import ApplicationCommandOption, ApplicationCommand, InteractionEvent, \
    ApplicationCommandPermissionOverwrite, ApplicationCommandOptionType
from ...discord.limits import APPLICATION_COMMAND_OPTIONS_MAX, APPLICATION_COMMAND_PERMISSION_OVERWRITE_MAX, \
    APPLICATION_COMMAND_DESCRIPTION_LENGTH_MIN, APPLICATION_COMMAND_DESCRIPTION_LENGTH_MAX, \
    APPLICATION_COMMAND_NAME_LENGTH_MIN, APPLICATION_COMMAND_NAME_LENGTH_MAX
    

from .responding import process_command_coroutine
from .utils import raw_name_to_display, UNLOADING_BEHAVIOUR_DELETE, UNLOADING_BEHAVIOUR_KEEP, _check_maybe_route, \
    UNLOADING_BEHAVIOUR_INHERIT, SYNC_ID_GLOBAL, SYNC_ID_NON_GLOBAL, normalize_description
from .wrappers import SlashCommandWrapper, get_parameter_configurers
from .converters import generate_parameter_parsers
from .exceptions import SlashCommandParameterConversionError

# Routers

SLASH_COMMAND_PARAMETER_NAMES = ('command', 'name', 'description', 'show_for_invoking_user_only', 'is_global', 'guild',
    'is_default', 'delete_on_unload', 'allow_by_default')

SLASH_COMMAND_NAME_NAME = 'name'
SLASH_COMMAND_COMMAND_NAME = 'command'



def _validate_show_for_invoking_user_only(show_for_invoking_user_only):
    """
    Validates the given `show_for_invoking_user_only` value.
    
    Parameters
    ----------
    show_for_invoking_user_only : `None` or `bool`
        The `show_for_invoking_user_only` value to validate.
    
    Returns
    -------
    show_for_invoking_user_only : `bool`
        The validated `show_for_invoking_user_only` value.
    
    Raises
    ------
    TypeError
        If `show_for_invoking_user_only` was not given as `None` nor as `bool` instance.
    """
    if show_for_invoking_user_only is None:
        show_for_invoking_user_only = False
    else:
        show_for_invoking_user_only = preconvert_bool(show_for_invoking_user_only, 'show_for_invoking_user_only')
    
    return show_for_invoking_user_only


def _validate_is_global(is_global):
    """
    Validates the given `is_global` value.
    
    Parameters
    ----------
    is_global : `None` or `bool`
        The `is_global` value to validate.
    
    Returns
    -------
    is_global : `bool`
        The validated `is_global` value.
    
    Raises
    ------
    TypeError
        If `is_global` was not given as `None` nor as `bool` instance.
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
    guild : ``Guild`` or `int`
        The guild value to validate.
    
    Returns
    -------
    guild_id : `int`
        Validated guild value converted to `int` instance.
    
    Raises
    ------
    TypeError
        If `guild` was not given neither as ``Guild`` nor `int` instance.
    ValueError
        If `guild` is an integer out of uint64 value range.
    """
    if isinstance(guild, Guild):
        guild_id = guild.id
    elif isinstance(guild, (int, str)):
        guild_id = preconvert_snowflake(guild, 'guild')
    else:
        raise TypeError(f'`guild` was not given neither as `{Guild.__class__.__name__}`, neither as `int` '
            f'instance, got {guild.__class__.__name__}.')
    
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
    guild_ids : `None` or `set` of `int`
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
            raise ValueError(f'`guild` cannot be given as empty container, got {guild!r}.')
    
    return guild_ids


def _validate_name(name):
    """
    Validates the given name.
    
    Parameters
    ----------
    name : `None` or `str`
        A command's respective name.
    
    Returns
    -------
    name : `None` or `str`
        The validated name.
    
    Raises
    ------
    TypeError
        If `name` is not given as `None` neither as `str` instance.
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
            raise TypeError(f'`name` can be only given as `None` or as `str` instance, got {name_type.__name__}; '
                f'{name!r}.')
        
        name_length = len(name)
        if name_length < APPLICATION_COMMAND_NAME_LENGTH_MIN or \
                name_length > APPLICATION_COMMAND_NAME_LENGTH_MAX:
            raise ValueError(f'`name` length is out of the expected range '
                f'[{APPLICATION_COMMAND_NAME_LENGTH_MIN}:'
                f'{APPLICATION_COMMAND_NAME_LENGTH_MAX}], got {name_length!r}; {name!r}.')
    
    return name


def _validate_is_default(is_default):
    """
    Validates the given `is_default` value.
    
    Parameters
    ----------
    is_default : `None` or `bool`
        The `is_default` value to validate.
    
    Returns
    -------
    is_default : `bool`
        The validated `is_default` value.
    
    Raises
    ------
    TypeError
        If `is_default` was not given as `None` nor as `bool` instance.
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
    delete_on_unload : `None` or `bool`
        The `delete_on_unload` value to validate.
    
    Returns
    -------
    unloading_behaviour : `int`
        The validated `delete_on_unload` value.
    
    Raises
    ------
    TypeError
        If `delete_on_unload` was not given as `None` nor as `bool` instance.
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
    allow_by_default : `None` or `bool`
        The `allow_by_default` value to validate.
    
    Returns
    -------
    allow_by_default : `bool`
        The validated `allow_by_default` value.
    
    Raises
    ------
    TypeError
        If `allow_by_default` was not given as `None` nor as `bool` instance.
    """
    if allow_by_default is None:
        allow_by_default = True
    else:
        allow_by_default = preconvert_bool(allow_by_default, 'allow_by_default')
    
    return allow_by_default


def _generate_description_from(command, name, description):
    """
    Generates description from the command and it's optionally given description. If both `description` and
    `command.__doc__` is missing, defaults to `name`.
    
    Parameters
    ----------
    command : `None` or `callable`
        The command's function.
    name : `str` or `None`
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
    
    if description_length < APPLICATION_COMMAND_DESCRIPTION_LENGTH_MIN or \
            description_length > APPLICATION_COMMAND_DESCRIPTION_LENGTH_MAX:
        raise ValueError(f'`description` length is out of the expected range '
            f'[{APPLICATION_COMMAND_DESCRIPTION_LENGTH_MIN}:{APPLICATION_COMMAND_DESCRIPTION_LENGTH_MAX}], got '
            f'{description_length!r}; {description!r}.')
    
    return description

@export
class SlashCommand:
    """
    Class to wrap an application command providing interface for ``Slasher``.
    
    Attributes
    ----------
    _command : `None` or ``SlashCommandFunction``
        The command of the slash command.
    _overwrites : `None` or `dict` of (`int`, `list` of ``ApplicationCommandPermissionOverwrite``)
        Permission overwrites applied to the slash command.
    _registered_application_command_ids : `None` or `dict` of (`int`, `int`) items
        The registered application command ids, which are matched by the command's schema.
        
        If empty set as `None`, if not then the keys are the respective guild's id and the values are the application
        command id.
    _schema : `None` or ``ApplicationCommand``
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
    
    _sub_commands: `None` or `dict` of (`str`, ``SlashCommandFunction`` or ``SlashSubCommand``) items
        Sub-commands of the slash command.
        
        Mutually exclusive with the ``._command`` parameter.
    allow_by_default : `bool`
        Whether the command is enabled by default for everyone who has `use_application_commands` permission.
    description : `str`
        Application command description. It's length can be in range [2:100].
    guild_ids : `None` or `set` of `int`
        The ``Guild``'s id to which the command is bound to.
    is_default : `bool`
        Whether the command is the default command in it's category.
    is_global : `bool`
        Whether the command is a global command.
        
        Guild commands have ``.guild_ids`` set as `None`.
    name : `str`
        Application command name. It's length can be in range [1:32].
    
    Notes
    -----
    ``SlashCommand`` instances are weakreferable.
    """
    __slots__ = ('__weakref__', '_command', '_overwrites', '_registered_application_command_ids', '_schema',
        '_sub_commands', '_unloading_behaviour', 'allow_by_default', 'description', 'guild_ids', 'is_default',
        'is_global', 'name')
    
    def _register_guild_and_application_command_id(self, guild_id, application_command_id):
        """
        Registers an application command's identifier to the ``SlashCommand`.
        
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
        Unregisters an application command's identifier from the ``SlashCommand`.
        
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
                if sync_id > (1<<22):
                    yield sync_id
    
    
    @classmethod
    def from_class(cls, klass):
        """
        Creates a new ``SlashCommand`` instance from the given `klass`.
        
        Parameters
        ----------
        klass : `type`
            The class to create slash command from.
        
        Returns
        -------
        self : ``SlashCommand`` or ``Router``
        
        Raises
        ------
        TypeError
            If any attribute's type is incorrect.
        ValueError
            If any attribute's value is incorrect.
        """
        return create_event_from_class(cls, klass, SLASH_COMMAND_PARAMETER_NAMES, SLASH_COMMAND_NAME_NAME,
            SLASH_COMMAND_COMMAND_NAME)
    
    def __new__(cls, func, name=None, description=None, show_for_invoking_user_only=None, is_global=None,
            guild=None, is_default=None, delete_on_unload=None, allow_by_default=None):
        """
        Creates a new ``SlashCommand`` instance with the given parameters.
        
        Parameters
        ----------
        func : `None` or `async-callable`, Optional
            The function used as the command when using the respective slash command.
        name : `str`, `None`, `tuple` of (`str`, `Ellipsis`, `None`), Optional
            The command's name if applicable. If not given or if given as `None`, the `func`'s name will be use
            instead.
        description : `None`, `Any` or `tuple` of (`None`, `Ellipsis`, `Any`), Optional
            Description to use instead of the function's docstring.
        show_for_invoking_user_only : `None`, `bool` or `tuple` of (`bool`, `Ellipsis`), Optional
            Whether the response message should only be shown for the invoking user. Defaults to `False`.
        is_global : `None`, `bool` or `tuple` of (`None`, `bool`, `Ellipsis`), Optional
            Whether the slash command is global. Defaults to `False`.
        guild : `None`, ``Guild``,  `int`, (`list`, `set`) of (`int`, ``Guild``) or \
                `tuple` of (`None`, ``Guild``,  `int`, `Ellipsis`, (`list`, `set`) of (`int`, ``Guild``)), Optional
            To which guild(s) the command is bound to.
        is_global : `None`, `bool` or `tuple` of (`None`, `bool`, `Ellipsis`), Optional
            Whether the slash command is the default command in it's category.
        delete_on_unload : `None`, `bool` or `tuple` of (`None`, `bool`, `Ellipsis`), Optional
            Whether the command should be deleted from Discord when removed.
        allow_by_default : `None`, `bool` or `tuple` of (`None`, `bool`, `Ellipsis`), Optional
            Whether the command is enabled by default for everyone who has `use_application_commands` permission.
        
        Returns
        -------
        self : ``SlashCommand`` or ``Router``
        
        Raises
        ------
        TypeError
            - If a value is routed but to a bad count amount.
            - If `show_for_invoking_user_only` was not given as `None` or `bool` instance.
            - If `is_global` was not given as `None` or `bool` instance.
            - If `guild` was not given neither as `None`, ``Guild``,  `int`, (`list`, `set`) of (`int`, ``Guild``)
            - If `func` is not async callable, neither cannot be instanced to async.
            - If `func` accepts keyword only parameters.
            - If `func` accepts `*args`.
            - If `func` accepts `**kwargs`.
            - If `func` accepts more than `27` parameters.
            - If `func`'s 0th parameter is annotated, but not as ``Client``.
            - If `func`'s 1th parameter is annotated, but not as ``InteractionEvent``.
            - If `name` was not given neither as `None` or `str` instance.
            - If a parameter's `annotation_value` is `list` instance, but it's elements do not match the
                `tuple` (`str`, `str` or `int`) pattern.
            - If a parameter's `annotation_value` is `dict` instance, but it's items do not match the
                (`str`, `str` or `int`) pattern.
            - If a parameter's `annotation_value` is unexpected.
            - If a parameter's `annotation` is `tuple`, but it's 1th element is neither `None` nor `str` instance.
            - If `is_global` and `guild` contradicts each other.
            - If `is_default` was not given neither as `None`, `bool` or `tuple` of (`None`, `bool`, `Ellipsis`).
            - If `delete_on_unload` was not given neither as `None`, `bool` or `tuple` of (`None`, `bool`, `Ellipsis`).
            - If `allow_by_default` was not given neither as `None`, `bool` or `tuple` of (`None`, `bool`,
                `Ellipsis`).
        ValueError
            - If `guild` is or contains an integer out of uint64 value range.
            - If a parameter's `annotation` is a `tuple`, but it's length is out of the expected range [0:2].
            - If a parameter's `annotation_value` is `str` instance, but not any of the expected ones.
            - If a parameter's `annotation_value` is `type` instance, but not any of the expected ones.
            - If a parameter's `choice` amount is out of the expected range [1:25].
            - If a parameter's `choice` name is duped.
            - If a parameter's `choice` values are mixed types.
            - If `description` length is out of range [2:100].
            - If `guild` is given as an empty container.
            - If `name` length is out of the expected range [1:32].
        """
        if (func is not None) and isinstance(func, SlashCommandWrapper):
            command, wrappers = func.fetch_function_and_wrappers_back()
        else:
            command = func
            wrappers = None
        
        # Check for routing
        
        route_to = 0
        name, route_to = _check_maybe_route('name', name, route_to, _validate_name)
        description, route_to = _check_maybe_route('description', description, route_to, None)
        show_for_invoking_user_only, route_to = _check_maybe_route('show_for_invoking_user_only',
            show_for_invoking_user_only, route_to, _validate_show_for_invoking_user_only)
        is_global, route_to = _check_maybe_route('is_global', is_global, route_to, _validate_is_global)
        guild_ids, route_to = _check_maybe_route('guild', guild, route_to, _validate_guild)
        is_default, route_to = _check_maybe_route('is_default', is_default, route_to, _validate_is_default)
        unloading_behaviour, route_to = _check_maybe_route('delete_on_unload', delete_on_unload, route_to,
            _validate_delete_on_unload)
        allow_by_default, route_to = _check_maybe_route('allow_by_default', allow_by_default, route_to,
            _validate_allow_by_default)
        
        if route_to:
            name = route_name(name, route_to)
            name = [raw_name_to_display(sub_name) for sub_name in name]
            
            default_description = _generate_description_from(command, None, None)
            show_for_invoking_user_only = route_value(show_for_invoking_user_only, route_to)
            is_global = route_value(is_global, route_to)
            guild_ids = route_value(guild_ids, route_to)
            is_default = route_value(is_default, route_to)
            unloading_behaviour = route_value(unloading_behaviour, route_to)
            allow_by_default = route_value(allow_by_default, route_to)
            
            description = [
                _generate_description_from(command, sub_name, description)
                    if ((description is None) or (description is not default_description)) else default_description
                for sub_name, description in zip(name, description)]
        
        else:
            name = check_name(command, name)
            
            sub_name_length = len(name)
            if sub_name_length < APPLICATION_COMMAND_NAME_LENGTH_MIN or \
                    sub_name_length > APPLICATION_COMMAND_NAME_LENGTH_MAX:
                raise ValueError(f'`name` length is out of the expected range '
                    f'[{APPLICATION_COMMAND_NAME_LENGTH_MIN}:'
                    f'{APPLICATION_COMMAND_NAME_LENGTH_MAX}], got {sub_name_length!r}; {name!r}.')
            
            name = raw_name_to_display(name)
            
            description = _generate_description_from(command, name, description)
        
        if command is None:
            parameter_parsers = None
        else:
            parameter_configurers = get_parameter_configurers(wrappers)
            command, parameter_parsers = generate_parameter_parsers(command, parameter_configurers)
        
        if route_to:
            router = []
            
            for name, description, show_for_invoking_user_only, is_global, guild_ids, is_default, unloading_behaviour,\
                    allow_by_default in zip(name, description, show_for_invoking_user_only, is_global, guild_ids,
                        is_default, unloading_behaviour, allow_by_default):
                
                if is_global and (guild_ids is not None):
                    raise TypeError(f'`is_guild` and `guild` contradict each other, got is_global={is_global!r}, '
                        f'guild={guild!r}')
                
                if (command is None):
                    command_function = None
                    sub_commands = {}
                else:
                    command_function = SlashCommandFunction(command, parameter_parsers, name, description,
                        show_for_invoking_user_only, is_default)
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
                self._overwrites = None
                
                if (wrappers is not None):
                    for wrapper in wrappers:
                        wrapper.apply(self)
                
                router.append(self)
            
            return Router(router)
        else:
            if is_global and (guild_ids is not None):
                raise TypeError(f'`is_guild` and `guild` contradict each other, got is_global={is_global!r}, '
                    f'guild={guild!r}')
            
            if (command is None):
                sub_commands = {}
                command_function = None
            else:
                command_function = SlashCommandFunction(command, parameter_parsers, name, description,
                    show_for_invoking_user_only, is_default)
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
            self._overwrites = None
            
            if (wrappers is not None):
                for wrapper in wrappers:
                    wrapper.apply(self)
            
            return self
    
    def __repr__(self):
        """returns the slash command's representation."""
        result = ['<', self.__class__.__name__, ' name=', repr(self.name), ' type=']
        
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
    
    def __str__(self):
        """Returns the slash command's name."""
        return self.name
    
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
        
        Raises
        ------
        SlashCommandParameterConversionError
            Command parameter conversion failed.
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
            raise SlashCommandParameterConversionError(
                None,
                option.name,
                'sub-command',
                list(self._sub_commands.keys()),
            )
        
        await sub_command(client, interaction_event, option.options)
    
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
            parameter_parsers = command._parameter_parsers
            
            options = None
            for parameter_parser in parameter_parsers:
                option = parameter_parser.as_option()
                if (option is not None):
                    if (options is None):
                        options = []
                    
                    options.append(option)
        
        return ApplicationCommand(self.name, self.description, allow_by_default=self.allow_by_default,
            options=options, )
    
    def as_sub(self):
        """
        Returns the slash command as a sub-command or sub-category.
        
        Returns
        -------
        new : ``SlashCommandFunction`` or ``SlashCommandCategory``
        """
        command = self._command
        if command is not None:
            return command
        
        return SlashCommandCategory(self)
        
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
        
        if (sub_commands is not None):
            parent_reference = None
            for sub_command in sub_commands.values():
                if isinstance(sub_command, SlashCommandCategory):
                    if parent_reference is None:
                        parent_reference = WeakReferer(new)
                    sub_command._parent_reference = parent_reference
        
        overwrites = self._overwrites
        if (overwrites is not None):
            overwrites = {guild_id: overwrite.copy() for guild_id, overwrite in overwrites.items()}
        
        new._overwrites = overwrites
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
            The ``SlashCommand`` is not a category.
        """
        if self._command is not None:
            raise RuntimeError(f'The {self.__class__.__name__} is not a category.')
        
        return _EventHandlerManager(self)
    
    def create_event(self, func, *args, **kwargs):
        """
        Adds a sub-command under the slash command.
        
        Parameters
        ----------
        func : `async-callable`
            The function used as the command when using the respective slash command.
        *args : Positional Parameters
            Positional parameters to pass to ``SlashCommand``'s constructor.
        **kwargs : Keyword parameters
            Keyword parameters to pass to the ``SlashCommand``'s constructor.
        
        Returns
        -------
        self : ``SlashCommand``
        
        Raises
        ------
        TypeError
            If Any parameter's type is incorrect.
        ValueError
            If Any parameter's value is incorrect.
        RuntimeError
            - The ``SlashCommand`` is not a category.
            - The ``SlashCommand`` reached the maximal amount of children.
            - If the command to add is a default sub-command meanwhile the category already has one.
        """
        if self._command is not None:
            raise RuntimeError(f'The {self.__class__.__name__} is not a category.')
        
        if isinstance(func, Router):
            func = func[0]
        
        if isinstance(func, type(self)):
            self._add_slash_command(func)
            return self
        
        command = type(self)(func, *args, **kwargs)
        
        if isinstance(command, Router):
            command = command[0]
        
        self._add_slash_command(command)
        return self
    
    def create_event_from_class(self, klass):
        """
        Breaks down the given class to it's class attributes and tries to add it as a sub-command or sub-category.
        
        Parameters
        ----------
        klass : `type`
            The class, from what's attributes the command will be created.
        
        Returns
        -------
        self : ``SlashCommand``
         
        Raises
        ------
        TypeError
            If Any attribute's type is incorrect.
        ValueError
            If Any attribute's value is incorrect.
        RuntimeError
            - The ``SlashCommand`` is not a category.
            - The ``SlashCommand`` reached the maximal amount of children.
            - If the command to add is a default sub-command meanwhile the category already has one.
        """
        command = type(self).from_class(klass)
        
        if isinstance(command, Router):
            command = command[0]
        
        self._add_slash_command(command)
        return self
    
    def _add_slash_command(self, command):
        """
        Adds a sub-command or sub-category to the slash command.
        
        Parameters
        ----------
        command : ``SlashCommand``
            The slash command to add.
        
        Raises
        ------
        RuntimeError
            - The ``SlashCommand`` reached the maximal amount of children.
            - If the command to add is a default sub-command meanwhile the category already has one.
        """
        sub_commands = self._sub_commands
        if len(sub_commands) == APPLICATION_COMMAND_OPTIONS_MAX and (command.name not in sub_commands):
            raise RuntimeError(f'The {self.__class__.__name__} reached the maximal amount of children '
                f'({APPLICATION_COMMAND_OPTIONS_MAX}).')
        
        if command.is_default:
            for sub_command in sub_commands.values():
                if sub_command.is_default:
                    raise RuntimeError(f'The category can have only 1 default command.')
        
        sub_commands[command.name] = command.as_sub()
        self._schema = None
    
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
        
        if self._overwrites != other._overwrites:
            return False
        
        return True
    
    def add_overwrite(self, guild_id, overwrite):
        """
        Adds an overwrite to the slash command.
        
        Parameters
        ----------
        guild_id : `int`
            The guild's id where the overwrite will be applied.
        overwrite : ``ApplicationCommandPermissionOverwrite`` or `None`
            The permission overwrite to add
        
        Raises
        ------
        AssertionError
            - Each command in each guild can have up to `10` overwrite, which is already reached.
        """
        overwrites = self._overwrites
        if overwrites is None:
            self._overwrites = overwrites = {}
        
        overwrites_for_guild = overwrites.get(guild_id, None)
        
        if __debug__:
            if (overwrites_for_guild is not None) and \
                    (len(overwrites_for_guild) >= APPLICATION_COMMAND_PERMISSION_OVERWRITE_MAX):
                raise AssertionError(f'`Each command in each guild can have up to '
                    f'{APPLICATION_COMMAND_PERMISSION_OVERWRITE_MAX} overwrite,s which is already reached.')
        
        if (overwrites_for_guild is not None) and (overwrite is not None):
            target_id = overwrite.target_id
            for index in range(len(overwrites_for_guild)):
                overwrite_ = overwrites_for_guild[index]
                
                if overwrite_.target_id != target_id:
                    continue
                
                if overwrite.allow == overwrite_.allow:
                    return
                
                del overwrites_for_guild[index]
                
                if overwrites_for_guild:
                    return
                
                overwrites[guild_id] = None
                return
        
        if overwrite is None:
            if overwrites_for_guild is None:
                overwrites[guild_id] = None
        else:
            if overwrites_for_guild is None:
                overwrites[guild_id] = overwrites_for_guild = []
            
            overwrites_for_guild.append(overwrite)
    
    def get_overwrites_for(self, guild_id):
        """
        Returns the slash command's overwrites for the given guild.
        
        Returns
        -------
        overwrites : `None` or `list` of ``ApplicationCommandPermissionOverwrite``
            Returns `None` instead of an empty list.
        """
        overwrites = self._overwrites
        if overwrites is None:
            return
        
        return overwrites.get(guild_id, None)

    def _get_sync_permission_ids(self):
        """
        Gets the permission overwrite guild id-s which should be synced.
        """
        permission_sync_ids = set()
        guild_ids = self.guild_ids
        # If the command is guild bound, sync it in every guild, if not, then sync it in every guild where it has an
        # an overwrite.
        if (guild_ids is None):
            overwrites = self._overwrites
            if (overwrites is not None):
                permission_sync_ids.update(guild_ids)
        else:
            permission_sync_ids.update(guild_ids)
        
        return permission_sync_ids


class SlashCommandFunction:
    """
    Represents an application command's backend implementation.
    
    Attributes
    ----------
    _parameter_parsers : `tuple` of ``ParameterConverter``
        Parsers to parse command parameters.
    _command : `async-callable˛
        The command's function to call.
    description : `str`
        The slash command's description.
    is_default : `bool`
        Whether the command is the default command in it's category.
    name : `str`
        The name of the slash command. It's length can be in range [1:32].
    show_for_invoking_user_only : `bool`
        Whether the response message should only be shown for the invoker user.
    """
    __slots__ = ('_parameter_parsers', '_command', 'category', 'description', 'is_default', 'name',
        'show_for_invoking_user_only')
    
    def __new__(cls, command, parameter_parsers, name, description, show_for_invoking_user_only, is_default):
        """
        Creates a new ``SlashCommandFunction`` instance with the given parameters-
        
        Parameters
        ----------
        command : `async-callable`
            The command's function to call.
        parameter_parsers : `tuple` of ``ParameterConverter``
            Parsers to parse command parameters.
        name : `str`
            The name of the slash command.
        description : `str`
            The slash command's description.
        show_for_invoking_user_only : `bool`
            Whether the response message should only be shown for the invoking user.
        is_default : `bool`
            Whether the command is the default command in it's category.
        """
        self = object.__new__(cls)
        self._command = command
        self._parameter_parsers = parameter_parsers
        self.show_for_invoking_user_only = show_for_invoking_user_only
        self.description = description
        self.name = name
        self.is_default = is_default
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
        options : `None` or `list` of ``InteractionEventChoice``
            Options bound to the function.
        
        Raises
        ------
        SlashCommandParameterConversionError
            Exception occurred meanwhile parsing parameter.
        """
        parameters = []
        
        parameter_relation = {}
        if (options is not None):
            for option in options:
                parameter_relation[option.name] = option.value
        
        for parameter_parser in self._parameter_parsers:
            value = parameter_relation.get(parameter_parser.name, None)
            
            parameter = await parameter_parser(client, interaction_event, value)
            parameters.append(parameter)
        
        command_coroutine = self._command(*parameters)
        
        await process_command_coroutine(client, interaction_event, self.show_for_invoking_user_only, command_coroutine)
    
    
    def __repr__(self):
        """Returns the application command option's representation."""
        result = ['<', self.__class__.__name__, ' name=', repr(self.name), ', description=', repr(self.description)]
        if self.is_default:
            result.append(', is_default=True')
        
        if self.show_for_invoking_user_only:
            result.append(', show_for_invoking_user_only=True')
        
        result.append('>')
        
        return ''.join(result)
    
    def as_option(self):
        """
        Returns the slash command function as an application command option.
        
        Returns
        -------
        option : ``ApplicationCommandOption``
        """
        parameter_parsers = self._parameter_parsers
        options = None
        for parameter_parser in parameter_parsers:
            option = parameter_parser.as_option()
            if (option is not None):
                if options is None:
                    options = []
                
                options.append(option)
        
        return ApplicationCommandOption(self.name, self.description, ApplicationCommandOptionType.sub_command,
            options=options, default=self.is_default)
    
    def copy(self):
        """
        Copies the slash command function.
        
        They are not mutable, so just returns itself.
        
        Returns
        -------
        self : ``SlashCommandFunction``
        """
        return self

    def __eq__(self, other):
        """Returns whether the two slash command functions are equal."""
        if type(self) is not type(other):
            return False
        
        if self._command != other._command:
            return False
        
        if self._parameter_parsers != other._parameter_parsers:
            return False
        
        if self.show_for_invoking_user_only != other.show_for_invoking_user_only:
            return False
        
        if self.description != other.description:
            return False
        
        if self.name != other.name:
            return False
        
        if self.is_default != other.is_default:
            return False
        
        return True


class SlashCommandCategory:
    """
    Represents an application command's backend implementation.
    
    Attributes
    ----------
    _sub_commands : `dict` of (`str`, ``SlashCommandFunction``) items
        The sub-commands of the category.
    _parent_reference : `None` or ``WeakReferer`` to ``SlashCommand
        The parent slash command of the category if any.
    description : `str`
        The slash command's description.
    is_default : `bool`
        Whether the command is the default command in it's category.
    name : `str`
        The name of the slash sub-category.
    """
    __slots__ = ('_sub_commands', '_parent_reference', 'description', 'is_default', 'name')
    
    def __new__(cls, slash_command):
        """
        Creates a new ``SlashCommandCategory`` instance with the given parameters.
        
        Parameters
        ----------
        slash_command : ``SlashCommand``
            The parent slash command.
        """
        self = object.__new__(cls)
        self.name = slash_command.name
        self.description = slash_command.description
        self._sub_commands = {}
        self._parent_reference = WeakReferer(slash_command)
        self.is_default = slash_command.is_default
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
        options : `None` or `list` of ``InteractionEventChoice``
            Options bound to the category.
        
        Raises
        ------
        SlashCommandParameterConversionError
            Exception occurred meanwhile parsing parameter.
        """
        if (options is None) or len(options) != 1:
            return
        
        option = options[0]
        
        try:
            sub_command = self._sub_commands[option.name]
        except KeyError:
            raise SlashCommandParameterConversionError(
                None,
                option.name,
                'sub-command',
                list(self._sub_commands.keys()),
            )
        
        await sub_command(client, interaction_event, option.options)
    
    def as_option(self):
        """
        Returns the slash command category as an application command option.
        
        Returns
        -------
        option : ``ApplicationCommandOption``
        """
        sub_commands = self._sub_commands
        if sub_commands:
            options = [sub_command.as_option() for sub_command in sub_commands]
        else:
            options = None
        
        return ApplicationCommandOption(self.name, self.description, ApplicationCommandOptionType.sub_command_group,
            options=options, default=self.is_default)
    
    def copy(self):
        """
        Copies the slash command category.
        
        Returns
        -------
        new : ``SlashCommandCategory``
        """
        sub_commands = {category_name: category.copy() for category_name, category in self._sub_commands.items()}
        
        new = object.__new__(type(self))
        new._sub_commands = sub_commands
        new.description = self.description
        new.name = self.name
        new._parent_reference = None
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
            Positional parameters to pass to ``SlashCommand``'s constructor.
        **kwargs : Keyword parameters
            Keyword parameters to pass to the ``SlashCommand``'s constructor.
        
        Returns
        -------
        self : ``SlashCommandCategory``
        
        Raises
        ------
        TypeError
            If Any parameter's type is incorrect.
        ValueError
            If Any parameter's value is incorrect.
        RuntimeError
            - The ``SlashCommand`` reached the maximal amount of children.
            - Cannot add anymore sub-category under sub-categories.
            - If the command to add is a default sub-command meanwhile the category already has one.
        """
        if isinstance(func, Router):
            func = func[0]
        
        if isinstance(func, SlashCommand):
            self._add_slash_command(func)
            return self
        
        command = SlashCommand(func, *args, **kwargs)
        if isinstance(command, Router):
            command = command[0]
        
        self._add_slash_command(command)
        return self
    
    def create_event_from_class(self, klass):
        """
        Breaks down the given class to it's class attributes and tries to add it as a sub-command.
        
        Parameters
        ----------
        klass : `type`
            The class, from what's attributes the command will be created.
        
        Returns
        -------
        self : ``SlashCommandCategory``
         
        Raises
        ------
        TypeError
            If Any attribute's type is incorrect.
        ValueError
            If Any attribute's value is incorrect.
        RuntimeError
            - The ``SlashCommand`` reached the maximal amount of children.
            - Cannot add anymore sub-category under sub-categories.
            - If the command to add is a default sub-command meanwhile the category already has one.
        """
        command = create_event_from_class(SlashCommand, klass, SLASH_COMMAND_PARAMETER_NAMES, SLASH_COMMAND_NAME_NAME,
            SLASH_COMMAND_COMMAND_NAME)
        
        if isinstance(command, Router):
            command = command[0]
        
        self._add_slash_command(command)
        return self
    
    def _add_slash_command(self, command):
        """
        Adds a sub-command or sub-category to the slash command.
        
        Parameters
        ----------
        command : ``SlashCommand``
            The slash command to add.
        
        Raises
        ------
        RuntimeError
            - The ``SlashCommand`` reached the maximal amount of children.
            - Cannot add anymore sub-category under sub-categories.
            - If the command to add is a default sub-command meanwhile the category already has one.
        """
        sub_commands = self._sub_commands
        if len(sub_commands) == APPLICATION_COMMAND_OPTIONS_MAX and (command.name not in sub_commands):
            raise RuntimeError(f'The {self.__class__.__name__} reached the maximal amount of children '
                f'({APPLICATION_COMMAND_OPTIONS_MAX}).')
        
        as_sub = command.as_sub()
        if isinstance(as_sub, type(self)):
            raise RuntimeError('Cannot add anymore sub-category under sub-categories.')
        
        if command.is_default:
            for sub_command in sub_commands.values():
                if sub_command.is_default:
                    raise RuntimeError(f'The category can have only 1 default command.')
        
        sub_commands[command.name] = as_sub
        
        parent_reference = self._parent_reference
        if (parent_reference is not None):
            parent = parent_reference()
            if (parent is not None):
                parent._schema = None
    
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
        
        return True
