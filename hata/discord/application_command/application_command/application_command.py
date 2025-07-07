__all__ = ('ApplicationCommand',)

from ...bases import DiscordEntity
from ...core import APPLICATION_COMMANDS, GUILDS
from ...localization.helpers import get_localized_length
from ...localization.utils import hash_locale_dictionary
from ...permission import Permission
from ...precreate_helpers import process_precreate_parameters_and_raise_extra
from ...utils import DATETIME_FORMAT_CODE, id_to_datetime

from ..helpers import with_translation

from .fields import (
    parse_application_id, parse_description, parse_description_localizations, parse_guild_id, parse_handler_type,
    parse_id, parse_integration_context_types, parse_integration_types, parse_name, parse_name_localizations,
    parse_nsfw, parse_options, parse_required_permissions, parse_target_type, parse_version, put_application_id,
    put_description, put_description_localizations, put_guild_id, put_handler_type, put_id,
    put_integration_context_types, put_integration_types, put_name, put_name_localizations,
    put_nsfw, put_options, put_required_permissions, put_target_type, put_version,
    validate_application_id, validate_description, validate_description_localizations, validate_guild_id,
    validate_handler_type, validate_id, validate_integration_context_types, validate_integration_types, validate_name,
    validate_name_localizations, validate_nsfw, validate_options, validate_required_permissions, validate_target_type,
    validate_version
)
from .preinstanced import (
    ApplicationCommandHandlerType, ApplicationCommandTargetType, CONTEXT_TARGET_TYPES, INTEGRATION_CONTEXT_TYPES_ALL
)


PRECREATE_FIELDS = {
    'application': ('application_id', validate_application_id),
    'application_id': ('application_id', validate_application_id),
    'description': ('description', validate_description),
    'description_localizations': ('description_localizations', validate_description_localizations),
    'guild': ('guild_id', validate_guild_id),
    'guild_id': ('guild_id', validate_guild_id),
    'handler_type': ('handler_type', validate_handler_type),
    'integration_context_types': ('integration_context_types', validate_integration_context_types),
    'integration_types': ('integration_types', validate_integration_types),
    'name': ('name', validate_name),
    'name_localizations': ('name_localizations', validate_name_localizations),
    'nsfw': ('nsfw', validate_nsfw),
    'options': ('options', validate_options),
    'required_permissions': ('required_permissions', validate_required_permissions),
    'target_type': ('target_type', validate_target_type),
    'version': ('version', validate_version),
}


class ApplicationCommand(DiscordEntity, immortal = True):
    """
    Represents a Discord slash command.
    
    Attributes
    ----------
    application_id : `int`
        The application command's application's id.
    
    description : `None`, `str`
        The command's description. It's length can be in range [2:100].
        
        Set as `None` for context commands.
    
    description_localizations : ``None | dict<Locale, str>``
        Localized descriptions of the application command.
        
        Set as `None` for context commands.
    
    guild_id : `int`
        The guild's identifier to which the command is bound to.
        
        Set as `0` if the command is global.
    
    handler_type : ``ApplicationCommandHandlerType``
        Represents what handles an application command.
    
    id : `int`
        The application command's id.
    
    integration_context_types : `None | tuple<ApplicationCommandIntegrationContextType>`
        The places where the application command shows up.
    
    integration_types : `None | tuple<ApplicationIntegrationType>`
        The options where the application command can be integrated to.
    
    name : `str`
        The name of the command. It's length can be in range [1:32].
    
    name_localizations : ``None | dict<Locale, str>``
        Localized names of the application command.
    
    nsfw : `bool`
        Whether the application command is only allowed in nsfw channels.
    
    options : `None`, `tuple` of ``ApplicationCommandOption``
        The parameters of the command. It's length can be in range [0:25]. If would be set as empty list, instead is
        set as `None`.
    
    required_permissions : ``Permission``
        The required permissions to use the application command inside of a guild.
    
    target_type : ``ApplicationCommandTargetType``
        The application command target's type describing where it shows up.
    
    version : `int`
        The time when the command was last edited in snowflake.
    
    Notes
    -----
    Application command instances are weakreferable.
    """
    __slots__ = (
        'application_id', 'description', 'description_localizations', 'guild_id', 'handler_type',
        'integration_context_types', 'integration_types', 'name', 'name_localizations', 'nsfw', 'options',
        'required_permissions', 'target_type', 'version'
    )
    
    def __new__(
        cls,
        name,
        description = None,
        *,
        description_localizations = ...,
        handler_type = ...,
        integration_context_types = ...,
        integration_types = ...,
        name_localizations = ...,
        nsfw = ...,
        options = ...,
        required_permissions = ...,
        target_type = ...,
    ):
        """
        Creates a new application command with the given parameters.
        
        Parameters
        ----------
        name : `str`
            The name of the command. It's length can be in range [1:32].
        
        description : `None`, `str` = `None`, Optional
            The command's description. It's length can be in range [2:100].
            
            Defaults to the `name` parameter if not given.
        
        description_localizations : ``None | dict<str | Locale, str> | (list | set | tuple<(str | Locale, str>)`` \
                , Optional (Keyword only)
            Localized descriptions of the application command.
        
        handler_type : `ApplicationCommandHandlerType | None | int`, Optional (Keyword only)
            Represents what handles an application command.
        
        integration_context_types : `None | iterable<ApplicationCommandIntegrationContextType | int>` \
                , Optional (Keyword only)
            The places where the application command shows up.
        
        integration_types : `None | iterable<ApplicationIntegrationType | int>`, Optional (Keyword only)
            The options where the application command can be integrated to.
        
        name_localizations : ``None | dict<str | Locale, str> | (list | set | tuple<(str | Locale, str>)`` \
                , Optional (Keyword only)
            Localized names of the application command.
        
        nsfw : `None`, `bool`, Optional (Keyword only)
            Whether the application command is allowed in nsfw channels.
        
        options : `None`, `iterable` of ``ApplicationCommandOption``, Optional (Keyword only)
            The parameters of the command. It's length can be in range [0:25].
        
        required_permissions : `None`, ``Permission``, `int`, Optional (Keyword only)
            The required permissions to use the application command inside of a guild.
        
        target_type : ``None | ApplicationCommandTargetType | int``, Optional (Keyword only)
            The application command's target type.
            
            Defaults to `ApplicationCommandTargetType.chat`.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # description
        description = validate_description(description)
        
        # description_localizations
        if description_localizations is ...:
            description_localizations = None
        else:
            description_localizations = validate_description_localizations(description_localizations)
        
        # handler_type
        if handler_type is ...:
            handler_type = ApplicationCommandHandlerType.none
        else:
            handler_type = validate_handler_type(handler_type)
        
        # integration_context_types
        if integration_context_types is ...:
            integration_context_types = INTEGRATION_CONTEXT_TYPES_ALL
        else:
            integration_context_types = validate_integration_context_types(integration_context_types)
        
        # integration_types
        if integration_types is ...:
            integration_types = None
        else:
            integration_types = validate_integration_types(integration_types)
        
        # name
        name = validate_name(name)
        
        # name_localizations
        if name_localizations is ...:
            name_localizations = None
        else:
            name_localizations = validate_name_localizations(name_localizations)
        
        # nsfw
        if nsfw is ...:
            nsfw = False
        else:
            nsfw = validate_nsfw(nsfw)
        
        # options
        if options is ...:
            options = None
        else:
            options = validate_options(options)
        
        # required_permissions
        if required_permissions is ...:
            required_permissions = Permission()
        else:
            required_permissions = validate_required_permissions(required_permissions)
        
        # target_type
        if target_type is ...:
            target_type = ApplicationCommandTargetType.chat
        else:
            target_type = validate_target_type(target_type)
        
        
        # Post checks
        if (target_type in CONTEXT_TARGET_TYPES):
            # Context commands cannot have description and options, so we clear them.
            description = None
            description_localizations = None
            options = None
        
        else:
            # For non context commands description is required.
            if (description is None):
                description = validate_description(name)
        
        # Construct
        self = object.__new__(cls)
        self.application_id = 0
        self.description = description
        self.description_localizations = description_localizations
        self.guild_id = 0
        self.handler_type = handler_type
        self.id = 0
        self.integration_context_types = integration_context_types
        self.integration_types = integration_types
        self.name = name
        self.name_localizations = name_localizations
        self.nsfw = nsfw
        self.options = options
        self.required_permissions = required_permissions
        self.target_type = target_type
        self.version = 0
        return self
    
    
    @classmethod
    def precreate(cls, application_command_id, **keyword_parameters):
        """
        Creates a new application command. If it already exists pick that up.
        
        Parameters
        ----------
        application_command_id : `int`
            The application command's identifier.
        
        **keyword_parameters : Keyword parameters
            Additional parameter to set the application command's fields with.
        
        Other Parameters
        ----------------
        application : `int`, ``Application``, Optional (Keyword only)
            Alternative for `application_id`.
        
        application_id : `int`, ``Application``, Optional (Keyword only)
            The application command's application's id.
        
        description : `None`, `str` = `None`, Optional
            The command's description. It's length can be in range [2:100].
        
        description_localizations : ``None | dict<str | Locale, str> | (list | set | tuple<(str | Locale, str>)`` \
                , Optional (Keyword only)
            Localized descriptions of the application command.
        
        guild : `int`, ``Guild``, Optional (Keyword only)
            Alternative for `guild_id`.
        
        guild_id : `int`, ``Guild``, Optional (Keyword only)
            The guild's identifier to which the command is bound to.
        
        handler_type : `ApplicationCommandHandlerType | None | int`, Optional (Keyword only)
            Represents what handles an application command.
        
        integration_context_types : `None | iterable<ApplicationCommandIntegrationContextType | int>` \
                , Optional (Keyword only)
            The places where the application command shows up.
        
        integration_types : `None | iterable<ApplicationIntegrationType | int>`, Optional (Keyword only)
            The options where the application command can be integrated to.
        
        name : `str`
            The name of the command. It's length can be in range [1:32].
        
        name_localizations : ``None | dict<str | Locale, str> | (list | set | tuple<(str | Locale, str>)`` \
                , Optional (Keyword only)
            Localized names of the application command.
        
        nsfw : `None`, `bool`, Optional (Keyword only)
            Whether the application command is allowed in nsfw channels.
        
        options : `None`, `iterable` of ``ApplicationCommandOption``, Optional (Keyword only)
            The parameters of the command. It's length can be in range [0:25].
        
        required_permissions : `None`, ``Permission``, `int`, Optional (Keyword only)
            The required permissions to use the application command inside of a guild.
        
        target_type : ``None | ApplicationCommandTargetType | int``, Optional (Keyword only)
            The application command's target type.
        
        version : `int`, Optional (Keyword only)
            The time when the command was last edited in snowflake.
        
        Returns
        -------
        self : `instance<cls>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
    
        application_command_id = validate_id(application_command_id)
        
        if keyword_parameters:
            processed = process_precreate_parameters_and_raise_extra(keyword_parameters, PRECREATE_FIELDS)
        else:
            processed = None
        
        try:
            self = APPLICATION_COMMANDS[application_command_id]
        except KeyError:
            self = cls._create_empty(application_command_id, 0)
            APPLICATION_COMMANDS[application_command_id] = self
        
        if (processed is not None):
            for item in processed:
                setattr(self, *item)
        
        return self
    
    @classmethod
    def _create_empty(cls, application_command_id, application_id):
        """
        Creates an empty application command with the default attributes set.
        
        Parameters
        ----------
        application_command_id : `int`
            The application command's identifier.
        application_id : `int`
            The application command's owner application's identifier.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.application_id = application_id
        self.description = None
        self.description_localizations = None
        self.guild_id = 0
        self.handler_type = ApplicationCommandHandlerType.none
        self.id = application_command_id
        self.integration_context_types = None
        self.integration_types = None
        self.name = ''
        self.name_localizations = None
        self.nsfw = False
        self.options = None
        self.required_permissions = Permission()
        self.target_type = ApplicationCommandTargetType.none
        self.version = 0
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new Application command from the given data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Received application command data.
        
        Returns
        -------
        self : `instance<cls>`
            The created application command instance.
        """
        application_command_id = parse_id(data)
        try:
            self = APPLICATION_COMMANDS[application_command_id]
        except KeyError:
            self = cls._create_empty(application_command_id, parse_application_id(data))
            
            # guild_id
            self.guild_id = parse_guild_id(data)
            
            APPLICATION_COMMANDS[application_command_id] = self
        
        self._update_attributes(data)
        return self
    
    
    @classmethod
    def _from_edit_data(cls, data, application_command_id, application_id):
        """
        Creates an application command with the given parameters after an application command edition took place.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Application command data returned by it's ``.to_data`` method.
        application_command_id : `int`
            The unique identifier number of the newly created application command.
        application_id : `int`
            The new application identifier number of the newly created application command.
        
        Returns
        -------
        self : `instance<cls>`
            The newly created or updated application command.
        """
        try:
            self = APPLICATION_COMMANDS[application_command_id]
        except KeyError:
            self = cls._create_empty(application_command_id, application_id)
            APPLICATION_COMMANDS[application_command_id] = self
        
        self._update_attributes(data)
        
        return self
    
    
    def to_data(self, * , defaults = False, include_internals = False):
        """
        Converts the application command to a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether internal fields should be included as well.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        
        put_description(self.description, data, defaults)
        put_description_localizations(self.description_localizations, data, defaults)
        put_handler_type(self.handler_type, data, defaults)
        put_integration_context_types(self.integration_context_types, data, defaults)
        put_integration_types(self.integration_types, data, defaults)
        put_name(self.name, data, defaults)
        put_name_localizations(self.name_localizations, data, defaults)
        put_nsfw(self.nsfw, data, defaults)
        put_options(self.options, data, defaults)
        put_required_permissions(self.required_permissions, data, defaults)
        put_target_type(self.target_type, data, defaults)
        
        if include_internals:
            put_application_id(self.application_id, data, defaults)
            put_guild_id(self.guild_id, data, defaults)
            put_id(self.id, data, defaults)
            put_version(self.version, data, defaults)
        
        return data
    
    
    def _update_attributes(self, data):
        """
        Updates the application command with the given data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Received application command data.
        """
        self.description = parse_description(data)
        self.description_localizations = parse_description_localizations(data)
        self.handler_type = parse_handler_type(data)
        self.integration_context_types = parse_integration_context_types(data)
        self.integration_types = parse_integration_types(data)
        self.name = parse_name(data)
        self.name_localizations = parse_name_localizations(data)
        self.nsfw = parse_nsfw(data)
        self.options = parse_options(data)
        self.required_permissions = parse_required_permissions(data)
        self.target_type = parse_target_type(data)
        self.version = parse_version(data)

    
    def _difference_update_attributes(self, data):
        """
        Updates the application command with the given data and returns the updated attributes in a dictionary with the
        attribute names as the keys and their old value as the values.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Received application command data.
        
        Returns
        -------
        old_attributes : `dict<str, object>`
            The updated attributes.
            
            Every item in the returned dict is optional and can contain the following ones:
            
            +---------------------------+-------------------------------------------------------------------+
            | Keys                      | Values                                                            |
            +===========================+===================================================================+
            | description               | `None`, `str`                                                     |
            +---------------------------+-------------------------------------------------------------------+
            | description_localizations | ``None | dict<Locale, str>``                       |
            +---------------------------+-------------------------------------------------------------------+
            | handler_type              | ``ApplicationCommandHandlerType``                                 |
            +---------------------------+-------------------------------------------------------------------+
            | integration_context_types | `None`, `tuple` of ``ApplicationCommandIntegrationContextType``   |
            +---------------------------+-------------------------------------------------------------------+
            | integration_types         | `None`, `tuple` of ``ApplicationIntegrationType``                 |
            +---------------------------+-------------------------------------------------------------------+
            | name                      | `str`                                                             |
            +---------------------------+-------------------------------------------------------------------+
            | name_localizations        | ``None | dict<Locale, str>``                       |
            +---------------------------+-------------------------------------------------------------------+
            | nsfw                      | `bool`                                                            |
            +---------------------------+-------------------------------------------------------------------+
            | options                   | `None`, `list` of ``ApplicationCommandOption``                    |
            +---------------------------+-------------------------------------------------------------------+
            | required_permissions      | ``Permission``                                                    |
            +---------------------------+-------------------------------------------------------------------+
            | target_type               | ``ApplicationCommandTargetType``                                  |
            +---------------------------+-------------------------------------------------------------------+
            | version                   | `int`                                                             |
            +---------------------------+-------------------------------------------------------------------+
        """
        old_attributes = {}
        
        # description
        description = parse_description(data)
        if self.description != description:
            old_attributes['description'] = self.description
            self.description = description
        
        # description_localizations
        description_localizations = parse_description_localizations(data)
        if self.description_localizations != description_localizations:
            old_attributes['description_localizations'] = self.description_localizations
            self.description_localizations = description_localizations
        
        # handler_type
        handler_type = parse_handler_type(data)
        if self.handler_type != handler_type:
            old_attributes['handler_type'] = self.handler_type
            self.handler_type = handler_type
        
        # integration_context_types
        integration_context_types = parse_integration_context_types(data)
        if self.integration_context_types != integration_context_types:
            old_attributes['integration_context_types'] = self.integration_context_types
            self.integration_context_types = integration_context_types
        
        # integration_types
        integration_types = parse_integration_types(data)
        if self.integration_types != integration_types:
            old_attributes['integration_types'] = self.integration_types
            self.integration_types = integration_types
        
        # name
        name = parse_name(data)
        if self.name != name:
            old_attributes['name'] = self.name
            self.name = name
        
        # name_localizations
        name_localizations = parse_name_localizations(data)
        if self.name_localizations != name_localizations:
            old_attributes['name_localizations'] = self.name_localizations
            self.name_localizations = name_localizations
        
        # nsfw
        nsfw = parse_nsfw(data)
        if self.nsfw != nsfw:
            old_attributes['nsfw'] = self.nsfw
            self.nsfw = nsfw
        
        # options
        options = parse_options(data)
        if self.options != options:
            old_attributes['options'] = self.options
            self.options = options
        
        # required_permissions
        required_permissions = parse_required_permissions(data)
        if self.required_permissions != required_permissions:
            old_attributes['required_permissions'] = self.required_permissions
            self.required_permissions = required_permissions
        
        # target_type
        target_type = parse_target_type(data)
        if (self.target_type is not target_type):
            old_attributes['target_type'] = self.target_type
            self.target_type = target_type
        
        # version
        version = parse_version(data)
        if self.version != version:
            old_attributes['version'] = self.version
            self.version = version
        
        return old_attributes
    
    
    def __repr__(self):
        """Returns the application command's representation."""
        repr_parts = ['<', type(self).__name__]
        
        # if the application command is partial, mention that, else add  `.id` and `.application_id` fields.
        if self.partial:
            repr_parts.append(' (partial)')
        
        else:
            # id
            repr_parts.append(' id = ')
            repr_parts.append(repr(self.id))
            
            # application_id
            repr_parts.append(', application_id = ')
            repr_parts.append(repr(self.application_id))
            
            # guild_id
            guild_id = self.guild_id
            if guild_id:
                repr_parts.append(', guild_id = ')
                repr_parts.append(repr(guild_id))
        
        # Required fields are `.name` and `.type`
        
        # name
        repr_parts.append(', name = ')
        repr_parts.append(repr(self.name))
        
        # target_type
        target_type = self.target_type
        if (target_type is not ApplicationCommandTargetType.none):
            repr_parts.append(', target_type = ')
            repr_parts.append(target_type.name)
            repr_parts.append(' ~ ')
            repr_parts.append(repr(target_type.value))
        
        # Extra fields: `.description`, `.options`, `.required_permissions`, `.nsfw`,
        # `.name_localizations`, `.description_localizations`, `.integration_context_types`, `.integration_types`,
        # `.handler_type`
        
        # description
        description = self.description
        if (description is not None):
            repr_parts.append(', description = ')
            repr_parts.append(repr(self.description))
        
        # handler_type
        handler_type = self.handler_type
        if (handler_type is not ApplicationCommandHandlerType.none):
            repr_parts.append(', handler_type = ')
            repr_parts.append(handler_type.name)
            repr_parts.append(' ~ ')
            repr_parts.append(repr(handler_type.value))
        
        # integration_context_types
        integration_context_types = self.integration_context_types
        if (integration_context_types is not None):
            repr_parts.append(', integration_context_types = ')
            repr_parts.append(repr(integration_context_types))
        
        # integration_types
        integration_types = self.integration_types
        if (integration_types is not None):
            repr_parts.append(', integration_types = ')
            repr_parts.append(repr(integration_types))
        
        # required_permissions
        required_permissions = self.required_permissions
        if required_permissions:
            repr_parts.append(', required_permissions = ')
            repr_parts.append(required_permissions.__format__('d'))
        
        if self.nsfw:
            repr_parts.append(', nsfw = True')
        
        # options
        options = self.options
        if (options is not None):
            repr_parts.append(', options = [')
            
            index = 0
            limit = len(options)
            
            while True:
                option = options[index]
                index += 1
                repr_parts.append(repr(option))
                
                if index == limit:
                    break
                
                repr_parts.append(', ')
                continue
            
            repr_parts.append(']')
        
        # name_localizations
        name_localizations = self.name_localizations
        if (name_localizations is not None):
            repr_parts.append(', name_localizations = ')
            repr_parts.append(repr(name_localizations))
        
        # description_localizations
        description_localizations = self.description_localizations
        if (description_localizations is not None):
            repr_parts.append(', description_localizations = ')
            repr_parts.append(repr(description_localizations))
        
        # Ignore extra fields: `.version`
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the application's hash value."""
        application_command_id = self.id
        if application_command_id:
            return application_command_id
        
        return self._get_hash_partial()
    
    
    def _get_hash_partial(self):
        """
        Hashes the fields of the application command.
        
        Called by ``.__hash__` when the application command is partial.
        
        Returns
        -------
        hash_value : `int`
        """
        hash_value = 0
        
        # id
        # non-partial field
        
        # application_id
        # non-partial field
        
        # description
        # Do not hash `.description` if same as `.name`
        description = self.description
        if (description is not None) and (description != self.name):
            hash_value ^= hash(description)
        
        # description_localizations
        # Do not hash `.description_localizations` if same as `.name_localizations`
        description_localizations = self.description_localizations
        if (description_localizations is not None) and (description_localizations != self.name_localizations):
            hash_value ^= hash_locale_dictionary(description_localizations)
        
        # guild_id
        # non-partial field
        
        # handler_type
        hash_value ^= hash(self.handler_type) << 15
        
        # integration_context_types
        integration_context_types = self.integration_context_types
        if (integration_context_types is not None):
            hash_value ^= len(integration_context_types) << 9
            for integration_context_type in integration_context_types:
                hash_value ^= integration_context_type.value << 13
        
        # integration_types
        integration_types = self.integration_types
        if (integration_types is not None):
            hash_value ^= len(integration_types) << 7
            for integration_type in integration_types:
                hash_value ^= integration_type.value << 11
        
        # name
        hash_value ^= hash(self.name)
        
        # name_localizations
        name_localizations = self.name_localizations
        if (name_localizations is not None):
            hash_value ^= hash_locale_dictionary(name_localizations)
        
        # nsfw
        hash_value ^= self.nsfw << 2
        
        # options
        options = self.options
        if (options is not None):
            hash_value ^= len(options) << 3
            
            for option in options:
                hash_value ^= hash(option)
        
        # required_permissions
        required_permissions = self.required_permissions
        if required_permissions:
            hash_value ^= hash(required_permissions << 7)
        
        # target_type
        hash_value ^= self.target_type.value << 11
        
        # version
        hash_value ^= self.version << 15
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two application commands are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self._is_equal_same_type(other)
    
    
    def __ne__(self, other):
        """Returns whether the two application commands are different."""
        if type(self) is not type(other):
            return NotImplemented
        
        return not self._is_equal_same_type(other)
    
    
    def _is_equal_same_type(self, other):
        """
        Returns whether the two instances are equal.
        
        Helper method for ``.__eq__``
        
        Parameters
        ----------
        other : `type<self>`
            The other instance. Must be from the same type.
        
        Returns
        -------
        is_equal : `bool`
        """
        # If both entity is not partial, leave instantly by comparing id.
        self_id = self.id
        other_id = other.id
        if self_id and other_id:
            if self_id == other_id:
                return True
            
            return False
        
        # description
        if self.description != other.description:
            return False
        
        # description_localizations
        if self.description_localizations != other.description_localizations:
            return False
        
        # handler_type
        if self.handler_type != other.handler_type:
            return False
        
        # integration_context_types
        if self.integration_context_types != other.integration_context_types:
            return False
        
        # integration_types
        if self.integration_types != other.integration_types:
            return False
        
        # name
        if self.name != other.name:
            return False
        
        # name_localizations
        if self.name_localizations != other.name_localizations:
            return False
        
        # nsfw
        if self.nsfw != other.nsfw:
            return False
        
        # required_permissions
        if self.required_permissions != other.required_permissions:
            return False
        
        # options
        if self.options != other.options:
            return False
        
        # target_type
        if (self.target_type is not other.target_type):
            return False
        
        return True
    
    
    def __format__(self, code):
        """
        Formats the application command in a format string.
        
        Parameters
        ----------
        code : `str`
            The option on based the result will be formatted.
        
        Returns
        -------
        application_command : `str`
        
        Raises
        ------
        ValueError
            Unknown format code.
        
        Examples
        --------
        ```py
        >>> from hata import ApplicationCommand
        >>> application_command = ApplicationCommand('cake-lover', 'Sends a random cake recipe OwO')
        >>> application_command
        <ApplicationCommand partial name = 'cake-lover', description = 'Sends a random cake recipe OwO'>
        >>> # no code stands for `application_command.name`.
        >>> f'{application_command}'
        'CakeLover'
        >>> # 'd' stands for display name.
        >>> f'{application_command:d}'
        'cake-lover'
        >>> # 'm' stands for mention.
        >>> f'{application_command:m}'
        '</cake-lover:0>'
        >>> # To mention a sub command, use @sub-command's name.
        >>> f'{application_command:m@eat}'
        '</cake-lover eat:0>'
        >>> # 'c' stands for created at.
        >>> f'{application_command:c}'
        '2021-01-03 20:17:36'
        >>> # 'e' stands for edited at.
        >>> f'{application_command:e}'
        'never'
        ```
        """
        if not code:
            return self.name
        
        if code == 'm' or code == 'm@':
            return self.mention
        
        if code.startswith('m@'):
            return self.mention_with(code[2:])
        
        if code == 'd':
            return self.display_name
        
        if code == 'c':
            return format(self.created_at, DATETIME_FORMAT_CODE)
        
        if code == 'e':
            edited_at = self.edited_at
            if edited_at is None:
                edited_at = 'never'
            else:
                edited_at = format(edited_at, DATETIME_FORMAT_CODE)
            return edited_at
        
        raise ValueError(
            f'Unknown format code {code!r} for {self.__class__.__name__}; {self!r}. '
            f'Available format codes: {""!r}, {"c"!r}, {"d"!r}, {"e"!r}, {"m"!r}, {"m@..."!r}.'
        )
    
    
    def __len__(self):
        """Returns the application command's length."""
        length = 0
        
        # description & description_localizations
        length += get_localized_length(self.description, self.description_localizations)
        
        # name & name_localizations
        length += get_localized_length(self.name, self.name_localizations)
        
        # options
        options = self.options
        if (options is not None):
            for option in options:
                length += len(option)
        
        return length
    
    
    def copy(self):
        """
        Copies the application command.
        
        The copy is always a partial application command.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        
        # application_id
        new.application_id = 0
        
        # description
        new.description = self.description
        
        # description_localizations
        description_localizations = self.description_localizations
        if (description_localizations is not None):
            description_localizations = description_localizations.copy()
        new.description_localizations = description_localizations
        
        # guild_id
        new.guild_id = 0
        
        # handler_type
        new.handler_type = self.handler_type
        
        # id
        new.id = 0
        
        # integration_context_types
        integration_context_types = self.integration_context_types
        if (integration_context_types is not None):
            integration_context_types = (*integration_context_types,)
        new.integration_context_types = integration_context_types
        
        # integration_types
        integration_types = self.integration_types
        if (integration_types is not None):
            integration_types = (*integration_types,)
        new.integration_types = integration_types
        
        # name
        new.name = self.name
        
        # name_localizations
        name_localizations = self.name_localizations
        if (name_localizations is not None):
            name_localizations = name_localizations.copy()
        new.name_localizations = name_localizations
        
        # nsfw
        new.nsfw = self.nsfw
        
        # options
        options = self.options
        if (options is not None):
            options = (*(option.copy() for option in options),)
        new.options = options
        
        # required_permissions
        new.required_permissions = self.required_permissions
        
        # target_type
        new.target_type = self.target_type
        
        # version
        new.version = 0
        
        return new
    
    
    def copy_with(
        self,
        *,
        description = ...,
        description_localizations = ...,
        handler_type = ...,
        integration_context_types = ...,
        integration_types = ...,
        name = ...,
        name_localizations = ...,
        nsfw = ...,
        options = ...,
        required_permissions = ...,
        target_type = ...,
    ):        
        """
        Copies the application command with the given fields.
        
        Parameters
        ----------
        description : `None`, `str` = `None`, Optional
            The command's description. It's length can be in range [2:100].
        
        description_localizations : ``None | dict<str | Locale, str> | (list | set | tuple<(str | Locale, str>)`` \
                , Optional (Keyword only)
            Localized descriptions of the application command.
        
        handler_type : `ApplicationCommandHandlerType | None | int`, Optional (Keyword only)
            Represents what handles an application command.
        
        integration_context_types : `None | iterable<ApplicationCommandIntegrationContextType | int>` \
                , Optional (Keyword only)
            The places where the application command shows up.
        
        integration_types : `None | iterable<ApplicationIntegrationType | int>`, Optional (Keyword only)
            The options where the application command can be integrated to.
        
        name : `str`, Optional (Keyword only)
            The name of the command. It's length can be in range [1:32].
        
        name_localizations : ``None | dict<str | Locale, str> | (list | set | tuple<(str | Locale, str>)`` \
                , Optional (Keyword only)
            Localized names of the application command.
        
        nsfw : `None`, `bool`, Optional (Keyword only)
            Whether the application command is allowed in nsfw channels.
        
        options : `None`, `iterable` of ``ApplicationCommandOption``, Optional (Keyword only)
            The parameters of the command. It's length can be in range [0:25].
        
        required_permissions : `None`, ``Permission``, `int`, Optional (Keyword only)
            The required permissions to use the application command inside of a guild.
        
        target_type : ``None | ApplicationCommandTargetType | int``, Optional (Keyword only)
            The application command's target type.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # description
        if description is ...:
            description = self.description
        else:
            description = validate_description(description)
        
        # description_localizations
        if description_localizations is ...:
            description_localizations = self.description_localizations
            if (description_localizations is not None):
                description_localizations = description_localizations.copy()
        else:
            description_localizations = validate_description_localizations(description_localizations)
        
        # handler_type
        if handler_type is ...:
            handler_type = self.handler_type
        else:
            handler_type = validate_handler_type(handler_type)
        
        # integration_context_types
        if integration_context_types is ...:
            integration_context_types = self.integration_context_types
            if (integration_context_types is not None):
                integration_context_types = (*integration_context_types,)
        else:
            integration_context_types = validate_integration_context_types(integration_context_types)
        
        # integration_types
        if integration_types is ...:
            integration_types = self.integration_types
            if (integration_types is not None):
                integration_types = (*integration_types,)
        else:
            integration_types = validate_integration_types(integration_types)
        
        # name
        if name is ...:
            name = self.name
        else:
            name = validate_name(name)
        
        # name_localizations
        if name_localizations is ...:
            name_localizations = self.name_localizations
            if (name_localizations is not None):
                name_localizations = name_localizations.copy()
        else:
            name_localizations = validate_name_localizations(name_localizations)
        
        # nsfw
        if nsfw is ...:
            nsfw = self.nsfw
        else:
            nsfw = validate_nsfw(nsfw)
        
        # options
        if options is ...:
            options = self.options
            if (options is not None):
                options = (*(option.copy() for option in options),)
        else:
            options = validate_options(options)
        
        # required_permissions
        if required_permissions is ...:
            required_permissions = self.required_permissions
        else:
            required_permissions = validate_required_permissions(required_permissions)
        
        # target_type
        if target_type is ...:
            target_type = ApplicationCommandTargetType.chat
        else:
            target_type = validate_target_type(target_type)
        
        
        # Post checks
        if (target_type in CONTEXT_TARGET_TYPES):
            # Context commands cannot have description and options, so we clear them.
            description = None
            description_localizations = None
            options = None
        
        else:
            # For non context commands description is required.
            if (description is None):
                description = validate_description(name)
        
        # Construct
        new = object.__new__(type(self))
        new.application_id = 0
        new.name = name
        new.name_localizations = name_localizations
        new.nsfw = nsfw
        new.description = description
        new.description_localizations = description_localizations
        new.guild_id = 0
        new.handler_type = handler_type
        new.id = 0
        new.integration_context_types = integration_context_types
        new.integration_types = integration_types
        new.options = options
        new.required_permissions = required_permissions
        new.target_type = target_type
        new.version = 0
        return new
    
    
    def with_translation(self, translation_table, replace = False):
        """
        Returns a new application command with the given translation table applied.
        
        Parameters
        ----------
        translation_table : `None`, `dict` of ((``Locale``, `str`),
                (`None`, `dict` (`str`, (`None`, `str`)) items)) items
            Translation table to pull localization. from.
        replace : `bool` = `False`, Optional
            Whether actual translation should be replaced.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        if translation_table is None:
            return self
        
        new = self.copy()
        
        # description_localizations
        new.description_localizations = with_translation(
            new.description,
            new.description_localizations,
            translation_table,
            replace,
        )
        
        # name_localizations
        new.name_localizations = with_translation(
            new.name,
            new.name_localizations,
            translation_table,
            replace,
        )
        
        # options
        options = new.options
        if (options is not None):
            new.options = (*(option.with_translation(translation_table, replace) for option in options),)
        
        return new
    
    
    def mention_sub_command(self, *sub_command_names):
        """
        Returns the application command's mention extended with the given sub-command names..
        
        Parameters
        ----------
        *sub_command_names : `str`
            The sub commands' names to mention.
        
        Returns
        -------
        mention : `str`
        """
        mention_parts = ['</', self.name]
        
        for sub_command_name in sub_command_names:
            mention_parts.append(' ')
            mention_parts.append(sub_command_name)
        
        mention_parts.append(':')
        mention_parts.append(str(self.id))
        mention_parts.append('>')
        
        return ''.join(mention_parts)
    
    
    def mention_with(self, with_):
        """
        Returns the application command's mention with the added string.
        
        Parameters
        ----------
        with_ : `str`
            Additional string to mention the command with. It should be sub commands' name.
        
        Returns
        -------
        mention : `str`
        """
        return f'</{self.name} {with_}:{self.id}>'
    
    
    @property
    def mention(self):
        """
        Returns the application command's mention.
        
        Returns
        -------
        mention : `str`
        """
        return f'</{self.name}:{self.id}>'
    
    
    @property
    def display_name(self):
        """
        Returns the application command's display name.
        
        Returns
        -------
        display_name : `str`
        """
        return self.name.lower().replace('_', '-')
    
    
    @property
    def edited_at(self):
        """
        Returns when the command was last edited / modified. If the command was not edited yet, returns `None`.
        
        Returns
        -------
        edited_at : `None`, `edited_at`
        """
        version = self.version
        if version:
            return id_to_datetime(version)
    
    
    @property
    def partial(self):
        """
        Returns whether the application command is partial.
        
        Returns
        -------
        partial : `bool`
        """
        return not self.id
    
    
    def is_context_command(self):
        """
        Returns whether the application command is a context command.
        
        Returns
        -------
        is_context_command : `bool`
        """
        return (self.target_type in CONTEXT_TARGET_TYPES)
    
    
    def is_slash_command(self):
        """
        Returns whether the application command is a slash command.
        
        Returns
        -------
        is_slash_command : `bool`
        """
        return (self.target_type is ApplicationCommandTargetType.chat)
    
    
    @property
    def guild(self):
        """
        Returns the application command's guild.
        
        Returns
        -------
        guild : ``None | Guild``
        """
        guild_id = self.guild_id
        if guild_id:
            return GUILDS.get(guild_id, None)
    
    
    def iter_options(self):
        """
        Iterates over the options of the application command.
        
        This method is an iterable generator.
        
        Yields
        ------
        option : ``ApplicationCommandOption``
        """
        options = self.options
        if (options is not None):
            yield from options
    
    
    def has_integration_type(self, integration_type):
        """
        Returns whether the application command is allowed the given integration type.
        
        Parameters
        ----------
        integration_type : `int`, ``ApplicationIntegrationType``
            The integration type to check.
        
        Returns
        -------
        hash_integration_type : `bool`
        """
        integration_types = self.integration_types
        if integration_types is None:
            return False
        
        return integration_type in integration_types
    
    
    def iter_integration_types(self):
        """
        Iterates over the integration types that the application command is allowed for.
        
        Yields
        ------
        integration_type : ``ApplicationIntegrationType``
        """
        integration_types = self.integration_types
        if (integration_types is not None):
            yield from integration_types


    def has_integration_context_type(self, integration_context_type):
        """
        Returns whether the application command is allowed the given integration context type.
        
        Parameters
        ----------
        integration_context_type : `int`, ``ApplicationCommandIntegrationContextType``
            The integration_context type to check.
        
        Returns
        -------
        hash_integration_context_type : `bool`
        """
        integration_context_types = self.integration_context_types
        if integration_context_types is None:
            return False
        
        return integration_context_type in integration_context_types
    
    
    def iter_integration_context_types(self):
        """
        Iterates over the integration context types that the application command is allowed for.
        
        Yields
        ------
        integration_context_type : ``ApplicationCommandIntegrationContextType``
        """
        integration_context_types = self.integration_context_types
        if (integration_context_types is not None):
            yield from integration_context_types
