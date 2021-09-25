__all__ = ('ApplicationCommand', 'ApplicationCommandOption', 'ApplicationCommandOptionChoice',
     'ApplicationCommandPermission', 'ApplicationCommandPermissionOverwrite', )

import warnings

from ..bases import DiscordEntity, maybe_snowflake
from ..core import APPLICATION_COMMANDS, ROLES
from ..preconverters import preconvert_preinstanced_type
from ..utils import is_valid_application_command_name, DATETIME_FORMAT_CODE
from ..user import User, UserBase, ClientUserBase, create_partial_user_from_id
from ..role import Role, create_partial_role_from_id

from .preinstanced import ApplicationCommandOptionType, ApplicationCommandPermissionOverwriteTargetType, \
    ApplicationCommandTargetType, APPLICATION_COMMAND_CONTEXT_TARGET_TYPES

APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_USER = ApplicationCommandPermissionOverwriteTargetType.user
APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_ROLE = ApplicationCommandPermissionOverwriteTargetType.role

# ApplicationCommand
APPLICATION_COMMAND_LIMIT_GLOBAL = 100
APPLICATION_COMMAND_LIMIT_GUILD = 100
APPLICATION_COMMAND_LENGTH_MAX = 4000

# ApplicationCommand & ApplicationCommandOption
APPLICATION_COMMAND_NAME_LENGTH_MIN = 1
APPLICATION_COMMAND_NAME_LENGTH_MAX = 32
APPLICATION_COMMAND_DESCRIPTION_LENGTH_MIN = 2
APPLICATION_COMMAND_DESCRIPTION_LENGTH_MAX = 100
APPLICATION_COMMAND_OPTIONS_MAX = 25
APPLICATION_COMMAND_CHOICES_MAX = 25

# ApplicationCommandOptionChoice
APPLICATION_COMMAND_CHOICE_NAME_LENGTH_MIN = 1
APPLICATION_COMMAND_CHOICE_NAME_LENGTH_MAX = 100
APPLICATION_COMMAND_CHOICE_VALUE_LENGTH_MIN = 0
APPLICATION_COMMAND_CHOICE_VALUE_LENGTH_MAX = 100

# ApplicationCommandPermissionOverwrite
APPLICATION_COMMAND_PERMISSION_OVERWRITE_MAX = 10

class ApplicationCommand(DiscordEntity, immortal=True):
    """
    Represents a Discord slash command.
    
    Attributes
    ----------
    id : `int`
        The application command's id.
    allow_by_default : `bool`
        Whether the command is enabled by default for everyone who has `use_application_commands` permission.
    application_id : `int`
        The application command's application's id.
    description : `str`
        The command's description. It's length can be in range [2:100].
    name : `str`
        The name of the command. It's length can be in range [1:32].
    options : `None` or `list` of ``ApplicationCommandOption``
        The parameters of the command. It's length can be in range [0:25]. If would be set as empty list, instead is
        set as `None`.
    target_type : ``ApplicationCommandTargetType``
        The application command target's type describing where it shows up.
    
    Notes
    -----
    ``ApplicationCommand`` instances are weakreferable.
    """
    __slots__ = ('allow_by_default', 'application_id', 'description', 'name', 'options', 'target_type',)
    
    def __new__(cls, name, description=None, *, allow_by_default=True, options=None, target_type=None):
        """
        Creates a new ``ApplicationCommand`` instance with the given parameters.
        
        Parameters
        ----------
        name : `str`
            The name of the command. It's length can be in range [1:32].
        
        description : `None` or `str`, Optional
            The command's description. It's length can be in range [2:100].
        
        allow_by_default : `bool`, Optional (Keyword only)
            Whether the command is enabled by default for everyone who has `use_application_commands` permission.
            
            Defaults to `True`.
        
        options : `None` or (`list` or `tuple`) of ``ApplicationCommandOption``, Optional (Keyword only)
            The parameters of the command. It's length can be in range [0:25].
        
        target_type : `int`, ``ApplicationCommandTargetType``, Optional (Keyword only)
            The application command's target type.
            
            Defaults to `ApplicationCommandTargetType.chat`.
        
        Raises
        ------
        TypeError
            If `target_type` is neither `int`, nor ``ApplicationCommandTargetType`` instance.
        ValueError
            `description` cannot be `None` for application commands with non-context target.
        AssertionError
            - If `name` was not given as `str` instance.
            - If `name` length is out of range [1:32].
            - If `name` contains unexpected character.
            - If `description` was not given as `None` nor `str` instance.
            - If `description` length is out of range [1:100].
            - If `options` was not given neither as `None` nor as (`list` or `tuple`) of ``ApplicationCommandOption``
                instances.
            - If `options`'s length is out of range [0:25].
            - If `allow_by_default` was not given as `bool` instance.
        """
        if __debug__:
            if not isinstance(name, str):
                raise AssertionError(f'`name` can be given as `str` instance, got {name.__class__.__name__}.')
            
            name_length = len(name)
            if name_length < APPLICATION_COMMAND_NAME_LENGTH_MIN or name_length > APPLICATION_COMMAND_NAME_LENGTH_MAX:
                raise AssertionError(f'`name` length can be in range '
                    f'[{APPLICATION_COMMAND_NAME_LENGTH_MIN}:{APPLICATION_COMMAND_NAME_LENGTH_MAX}], got '
                    f'{name_length!r}; {name!r}.')
            
            if not is_valid_application_command_name(name):
                raise AssertionError(f'`name` contains an unexpected character; Got {name!r}.')
            
            if (description is not None):
                if not isinstance(description, str):
                    raise AssertionError(f'`description` can be given as `None` or `str` instance, got '
                        f'{description.__class__.__name__}.')
                
                description_length = len(description)
                if description_length < APPLICATION_COMMAND_DESCRIPTION_LENGTH_MIN or \
                        description_length > APPLICATION_COMMAND_DESCRIPTION_LENGTH_MAX:
                    raise AssertionError(f'`description` length can be in range '
                        f'[{APPLICATION_COMMAND_DESCRIPTION_LENGTH_MIN}:{APPLICATION_COMMAND_DESCRIPTION_LENGTH_MAX}], '
                        f'got {description_length!r}; {description!r}.')
            
            if not isinstance(allow_by_default, bool):
                raise AssertionError(f'`allow_by_default` can be given as `bool` instance, got '
                    f'{allow_by_default.__class__.__name__}.')
        
        if options is None:
            options_processed = None
        else:
            if __debug__:
                if not isinstance(options, (tuple, list)):
                    raise AssertionError(f'`options` can be given as `None` or (`list` or `tuple`) of '
                        f'`{ApplicationCommandOption.__name__}`, got {options.__class__.__name__}.')
            
            # Copy it
            options_processed = list(options)
            if options_processed:
                if __debug__:
                    if len(options_processed) > APPLICATION_COMMAND_OPTIONS_MAX:
                        raise AssertionError(f'`options` length can be in range '
                            f'[0:{APPLICATION_COMMAND_OPTIONS_MAX}], got {len(options_processed)!r}; {options!r}')
                    
                    for index, option in enumerate(options_processed):
                        if not isinstance(option, ApplicationCommandOption):
                            raise AssertionError(f'`options` was given either as `list` or `tuple`, but it\'s element '
                                f'At index {index!r} is not {ApplicationCommandOption.__name__} instance, but '
                                f'{option.__class__.__name__}.')
            
            else:
                options_processed = None
        
        if target_type is None:
            target_type = ApplicationCommandTargetType.chat
        else:
            target_type = preconvert_preinstanced_type(target_type, 'target_type', ApplicationCommandTargetType)
        
        if (target_type not in APPLICATION_COMMAND_CONTEXT_TARGET_TYPES):
            if (description is None):
                raise ValueError(f'`description` cannot be `None` for application commands with non-context target.')
        else:
            # We do not really care about them, we can just lose them, no problem.
            description = None
            options_processed = None
        
        self = object.__new__(cls)
        self.id = 0
        self.application_id = 0
        self.name = name
        self.description = description
        self.allow_by_default = allow_by_default
        self.options = options_processed
        self.target_type = target_type
        return self
    
    
    def add_option(self, option):
        """
        Adds a new option to the application command.
        
        Parameters
        ----------
        option : ``ApplicationCommandOption``
            The option to add.
        
        Returns
        -------
        self : ``ApplicationCommand``
        
        Raises
        ------
        AssertionError
            - If the entity is not partial.
            - If `option` is not ``ApplicationCommandOption`` instance.
            - If the ``ApplicationCommand`` has already `25` options.
        """
        if __debug__:
            if self.id != 0:
                raise AssertionError(f'{self.__class__.__name__}.add_option` can be only called on partial '
                    f'`{self.__class__.__name__}`-s, but was called on {self!r}.')
        
        if __debug__:
            if not isinstance(option, ApplicationCommandOption):
                raise AssertionError(f'`option` can be given as {ApplicationCommandOption.__name__} instance, got '
                    f'{option.__class__.__name__}.')
        
        options = self.options
        if options is None:
            self.options = options = []
        else:
            if __debug__:
                if len(options) >= APPLICATION_COMMAND_OPTIONS_MAX:
                    raise AssertionError(f'`option` cannot be added if the {ApplicationCommandOption.__name__} has '
                        f'already `{APPLICATION_COMMAND_OPTIONS_MAX}` options.')
        
        options.append(option)
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new ``ApplicationCommand`` from requested data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received application command data.
        
        Returns
        -------
        self : ``ApplicationCommand``
            The created application command instance.
        """
        application_command_id = int(data['id'])
        try:
            self = APPLICATION_COMMANDS[application_command_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = application_command_id
            self.application_id = int(data['application_id'])
            APPLICATION_COMMANDS[application_command_id] = self
        
            # Discord might not include attributes in edit data, so we will set them first to avoid unset attributes.
            self.description = None
            self.name = ''
            self.options = None
            self.allow_by_default = True
            self.target_type = ApplicationCommandTargetType.none
        
        self._update_attributes(data)
        return self
    
    
    def _update_attributes(self, data):
        """
        Updates the application command with the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received application command data.
        """
        try:
            description = data['description']
        except KeyError:
            pass
        else:
            if (description is not None) and (not description):
                description = None
            self.description = description
        
        try:
            self.name = data['name']
        except KeyError:
            pass
        
        try:
            option_datas = data['options']
        except KeyError:
            pass
        else:
            if (option_datas is None) or (not option_datas):
                options = None
            else:
                options = [ApplicationCommandOption.from_data(option_data) for option_data in option_datas]
            self.options = options
        
        try:
            self.allow_by_default = data['default_permission']
        except KeyError:
            pass
        
        try:
            target_type = data['type']
        except KeyError:
            pass
        else:
            self.target_type = ApplicationCommandTargetType.get(target_type)
    
    
    def _difference_update_attributes(self, data):
        """
        Updates the application command with the given data and returns the updated attributes in a dictionary with the
        attribute names as the keys and their old value as the values.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received application command data.
        
        Returns
        -------
        old_attributes : `dict` of (`str`, `Any`) items
            The updated attributes.
            
            Every item in the returned dict is optional and can contain the following ones:
            
            +-----------------------+---------------------------------------------------+
            | Keys                  | Values                                            |
            +=======================+===================================================+
            | description           | `None` or `str`                                   |
            +-----------------------+---------------------------------------------------+
            | allow_by_default      | `bool`                                            |
            +-----------------------+---------------------------------------------------+
            | name                  | `str`                                             |
            +-----------------------+---------------------------------------------------+
            | options               | `None` or `list` of ``ApplicationCommandOption``  |
            +-----------------------+---------------------------------------------------+
            | target_type           | ``ApplicationCommandTargetType``                  |
            +-----------------------+---------------------------------------------------+
        """
        old_attributes = {}
        
        try:
            description = data['description']
        except KeyError:
            pass
        else:
            if (description is not None) and (not description):
                description = None
            if self.description != description:
                old_attributes['description'] = self.description
                self.description = description
        
        try:
            name = data['name']
        except KeyError:
            pass
        else:
            if self.name != name:
                old_attributes['name'] = self.name
                self.name = name
        
        try:
            option_datas = data['options']
        except KeyError:
            pass
        else:
            if (option_datas is None) or (not option_datas):
                options = None
            else:
                options = [ApplicationCommandOption.from_data(option_data) for option_data in option_datas]
            
            if self.options != options:
                old_attributes['options'] = self.options
                self.options = options
        
        try:
            allow_by_default = data['default_permission']
        except KeyError:
            pass
        else:
            if self.allow_by_default != self.allow_by_default:
                old_attributes['allow_by_default'] = allow_by_default
                self.allow_by_default = allow_by_default
        
        try:
            target_type = data['type']
        except KeyError:
            pass
        else:
            target_type = ApplicationCommandTargetType.get(target_type)
            if (self.target_type is not target_type):
                old_attributes['target_type'] = self.target_type
                self.target_type = target_type
        
        
        return old_attributes
    
    
    def to_data(self):
        """
        Converts the application command to a json serializable object.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        data = {
            'name': self.name,
        }
        
        description = self.description
        if (description is not None):
            data['description'] = description
        
        options = self.options
        if (options is None):
            option_datas = []
        else:
            option_datas = [option.to_data() for option in options]
        
        data['options'] = option_datas
        
        # Always add this to data, so if we update the command with it, will be always updated.
        data['default_permission'] = self.allow_by_default
        
        data['type'] = self.target_type.value
        
        return data
    
    def __repr__(self):
        """Returns the application command's representation."""
        repr_parts = [
            '<', self.__class__.__name__,
        ]
        
        id_ = self.id
        if id_ == 0:
            repr_parts.append(' (partial)')
        else:
            repr_parts.append(' id=')
            repr_parts.append(repr(id_))
            repr_parts.append(', application_id=')
            repr_parts.append(repr(self.application_id))
        
        repr_parts.append(', name=')
        repr_parts.append(repr(self.name))
        
        target_type = self.target_type
        if (target_type is not ApplicationCommandTargetType.none):
            repr_parts.append(', target_type=')
            repr_parts.append(target_type.name)
            repr_parts.append(' (')
            repr_parts.append(repr(target_type.value))
            repr_parts.append(')')
        
        description = self.description
        if (description is not None):
            repr_parts.append(', description=')
            repr_parts.append(repr(self.description))
        
        if not self.allow_by_default:
            repr_parts.append(', allow_by_default=False')
        
        options = self.options
        if (options is not None):
            repr_parts.append(', options=[')
            
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
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    @property
    def partial(self):
        """
        Returns whether the application command is partial.
        
        Returns
        -------
        partial : `bool`
        """
        if self.id == 0:
            return True
        
        return False
    
    
    def __hash__(self):
        """Returns the application's hash value."""
        id_ = self.id
        if id_:
            return id_
        
        raise TypeError(f'Cannot hash partial {self.__class__.__name__} object.')
    
    
    @classmethod
    def _from_edit_data(cls, data, interaction_id, application_id):
        """
        Creates an application command with the given parameters after an application command edition took place.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Application command data returned by it's ``.to_data`` method.
        interaction_id : `int`
            The unique identifier number of the newly created application command.
        application_id : `int`
            The new application identifier number of the newly created application command.
        
        Returns
        -------
        self : ``ApplicationCommand``
            The newly created or updated application command.
        """
        try:
            self = APPLICATION_COMMANDS[interaction_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = interaction_id
            self.application_id = application_id
            APPLICATION_COMMANDS[interaction_id] = self
            
            # Discord might not include attributes in edit data, so we will set them first to avoid unset attributes.
            self.description = None
            self.name = ''
            self.options = None
            self.target_type = ApplicationCommandTargetType.none
        
        self._update_attributes(data)
        
        return self
    
    
    def copy(self):
        """
        Copies the ``ApplicationCommand`` instance.
        
        Returns
        -------
        new : ``ApplicationCommand``
            A copied new partial application command.
        """
        new = object.__new__(type(self))
        new.id = 0
        new.application_id = 0
        new.name = self.name
        new.description = self.description
        new.allow_by_default = self.allow_by_default
        
        options = self.options
        if (options is not None):
            options = [option.copy() for option in options]
        new.options = options
        
        new.target_type = self.target_type
        
        return new
    
    def __eq__(self, other):
        """Returns whether the two application commands are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # If both entity is not partial, leave instantly by comparing id.
        self_id = self.id
        other_id = other.id
        if self_id and other_id:
            if self_id == other_id:
                return True
            
            return False
        
        if self.name != other.name:
            return False
        
        if self.description != other.description:
            return False
        
        if self.allow_by_default != other.allow_by_default:
            return False
        
        if self.options != other.options:
            return False
        
        if (self.target_type is not other.target_type):
            return False
        
        return True
    
    
    def __ne__(self, other):
        """Returns whether the two application commands are different."""
        if type(self) is not type(other):
            return NotImplemented
        
        self_id = self.id
        other_id = other.id
        if self_id and other_id:
            if self_id == other_id:
                return False
            
            return True
        
        if self.name != other.name:
            return True
        
        if self.description != other.description:
            return True
        
        if self.allow_by_default != other.allow_by_default:
            return True
        
        if self.options != other.options:
            return True
        
        if (self.target_type is not other.target_type):
            return True
        
        return False
    
    
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
        <ApplicationCommand partial name='cake-lover', description='Sends a random cake recipe OwO'>
        >>> # no code stands for `application_command.name`.
        >>> f'{application_command}'
        'CakeLover'
        >>> # 'd' stands for display name.
        >>> f'{application_command:d}'
        'cake-lover'
        >>> # 'm' stands for mention.
        >>> f'{application_command:m}'
        '</cake-lover:0>'
        >>> # 'c' stands for created at.
        >>> f'{application_command:c}'
        '2021-01-03 20:17:36'
        ```
        """
        if not code:
            return self.name
        
        if code == 'm':
            return self.mention
        
        if code == 'd':
            return self.display_name
        
        if code == 'c':
            return self.created_at.__format__(DATETIME_FORMAT_CODE)
        
        raise ValueError(f'Unknown format code {code!r} for object of type {self.__class__.__name__!r}')
    
    
    def __len__(self):
        """Returns the application command's length."""
        length = len(self.name) + len(self.description)
        
        options = self.options
        if (options is not None):
            for option in options:
                length += len(option)
        
        return length
    
    
    def is_context_command(self):
        """
        Returns whether the application command is a context command.
        
        Returns
        -------
        is_context_command : `bool`
        """
        return (self.target_type in APPLICATION_COMMAND_CONTEXT_TARGET_TYPES)
    
    
    def is_slash_command(self):
        """
        Returns whether the application command is a slash command.
        
        Returns
        -------
        is_slash_command : `bool`
        """
        return (self.target_type is ApplicationCommandTargetType.chat)


class ApplicationCommandOption:
    """
    An option of an ``ApplicationCommand``.
    
    Attributes
    ----------
    autocomplete : `bool`
        Whether the option supports auto completion.
        
        Mutually exclusive with the ``.choices``. Only applicable for string type parameters.
    
    channel_types : `None` or `tuple` of `int`
        The accepted channel types by the option.
        
        Only applicable if ``.type`` is set to `ApplicationCommandOptionType.channel`.
    
    choices : `None` or `list` of ``ApplicationCommandOptionChoice``
        Choices for `str` and `int` types for the user to pick from.
        
        Mutually exclusive with the ``.autocomplete``.
    
    default : `bool`
        Whether the option is the default one. Only one option can be `default`.
    description : `str`
        The description of the application command option. It's length can be in range [1:100].
    name : `str`
        The name of the application command option. It's length can be in range [1:32].
    options : `None` or `list` of ``ApplicationCommandOption``
        If the command's type is sub-command group type, then this nested option will be the parameters of the
        sub-command. It's length can be in range [0:25]. If would be set as empty list, instead is set as `None`.
    required : `bool`
        Whether the parameter is required. Defaults to `False`.
    type : ``ApplicationCommandOptionType``
        The option's type.
    """
    __slots__ = ('autocomplete', 'channel_types', 'choices', 'default', 'description', 'name', 'options', 'required',
        'type')
    
    def __new__(cls, name, description, type_, *, autocomplete=False, channel_types=None, default=False,
            required=False, choices=None, options=None):
        """
        Creates a new ``ApplicationCommandOption`` instance with the given parameters.
        
        Parameters
        ----------
        name : `str`
            The name of the command. It's length can be in range [1:32].
        description : `str`
            The command's description. It's length can be in range [2:100].
        type_ : `int` or ``ApplicationCommandOptionType``
            The application command option's type.
        autocomplete : `bool`
            Whether the option supports auto completion.
            
            Mutually exclusive with the `choices` parameter. Only applicable for string type parameters.
        
        channel_types : `None` or `iterable` of `int`, Optional (Keyword only)
            The accepted channel types by the option.
            
            Only applicable if ``.type`` is set to `ApplicationCommandOptionType.channel`.
        
        default : `bool`, Optional (Keyword only)
            Whether the option is the default one. Defaults to `False`.
        required : `bool`, Optional (Keyword only)
            Whether the parameter is required. Defaults to `False`.
        choices : `None` or (`list` or `tuple`) of ``ApplicationCommandOptionChoice``, Optional (Keyword only)
            The choices of the command for string or integer types. It's length can be in range [0:25].
            
            Mutually exclusive with the `autocomplete` parameter.
            
        options : `None` or (`list` or `tuple`) of ``ApplicationCommandOption``, Optional (Keyword only)
            The parameters of the command. It's length can be in range [0:25]. Only applicable for sub command groups.
        
        Raises
        ------
        TypeError
            - If `type_` was not given neither as `int` nor ``ApplicationCommandOptionType`` instance.
            - If `choices` was given meanwhile `type_` is neither string nor integer option type.
            - If `options` was given meanwhile `type_` is not a sub-command group option type.
            - If a choice's value's type not matched the expected type described `type_`.
            - If `channel_types` is neither `None` nor `iterable` of `int`.
        ValueError
            - If `type_` was given as `int` instance, but it do not matches any of the precreated
                ``ApplicationCommandOptionType``-s.
            - If `channel_types` contains an unknown channel type value.
        AssertionError
            - If `name` was not given as `str` instance.
            - If `name` length is out of range [1:32].
            - If `description` was not given as `str` instance.
            - If `description` length is out of range [1:100].
            - If `options` was not given neither as `None` nor as (`list` or `tuple`) of ``ApplicationCommandOption``
                instances.
            - If `options`'s length is out of range [0:25].
            - If `default` was not given as `bool` instance.
            - If `required` was not given as `bool` instance.
            - If `choices` was not given neither as `None` nor as (`list` or `tuple`) of
                ``ApplicationCommandOptionChoice`` instances.
            - If `choices`'s length is out of range [0:25].
            - If an option is a sub command group option.
            - If `channel_types` is given, but `type_` is not `ApplicationCommandOptionType.channel`.
            - If `autocomplete` is not `bool` instance.
            - If both `autocomplete` and `choices` are defined.
            - If `autocomplete` is defined, but the parameters's type is not string.
        """
        if __debug__:
            if not isinstance(name, str):
                raise AssertionError(f'`name` can be given as `str` instance, got {name.__class__.__name__}.')
            
            name_length = len(name)
            if name_length < APPLICATION_COMMAND_NAME_LENGTH_MIN or \
                    name_length > APPLICATION_COMMAND_NAME_LENGTH_MAX:
                raise AssertionError(f'`name` length can be in range '
                    f'[{APPLICATION_COMMAND_NAME_LENGTH_MIN}:{APPLICATION_COMMAND_NAME_LENGTH_MAX}], got '
                    f'{name_length!r}; {name!r}.')
        
            if not isinstance(description, str):
                raise AssertionError(f'`description` can be given as `str` instance, got '
                    f'{description.__class__.__name__}.')
            
            description_length = len(description)
            if description_length < APPLICATION_COMMAND_DESCRIPTION_LENGTH_MIN or \
                    description_length > APPLICATION_COMMAND_DESCRIPTION_LENGTH_MAX:
                raise AssertionError(f'`description` length can be in range '
                    f'[{APPLICATION_COMMAND_DESCRIPTION_LENGTH_MIN}:'
                    f'{APPLICATION_COMMAND_DESCRIPTION_LENGTH_MAX}], got {description_length!r}; '
                    f'{description!r}.')
        
        type_ = preconvert_preinstanced_type(type_, 'type_', ApplicationCommandOptionType)
        
        if __debug__:
            if not isinstance(default, bool):
                raise AssertionError(f'`default` can be given as `bool` instance, got {default.__class__.__name__}.')
            
            if not isinstance(required, bool):
                raise AssertionError(f'`required` can be given as `bool` instance, got {required.__class__.__name__}.')
        
        if choices is None:
            choices_processed = None
        else:
            if __debug__:
                if not isinstance(choices, (tuple, list)):
                    raise AssertionError(f'`choices` can be given as `None` or (`list` or `tuple`) of '
                        f'`{ApplicationCommandOptionChoice.__name__}`, got {choices.__class__.__name__}.')
            
            choices_processed = list(choices)
            
            if __debug__:
                if len(choices_processed) > APPLICATION_COMMAND_CHOICES_MAX:
                    raise AssertionError(f'`choices` length can be in range '
                        f'[0:{APPLICATION_COMMAND_CHOICES_MAX}], got {len(choices_processed)!r}; '
                        f'{choices!r}')
                
                for index, choice in enumerate(choices_processed):
                    if not isinstance(choice, ApplicationCommandOptionChoice):
                        raise AssertionError(f'`choices` was given either as `list` or `tuple`, but it\'s element '
                            f'At index {index!r} is not {ApplicationCommandOptionChoice.__name__} instance, but '
                            f'{choice.__class__.__name__}; got {choices!r}.')
            
            if not choices_processed:
                choices_processed = None
        
        if options is None:
            options_processed = None
        else:
            if __debug__:
                if not isinstance(options, (tuple, list)):
                    raise AssertionError(f'`options` can be given as `None` or (`list` or `tuple`) of '
                        f'`{ApplicationCommandOption.__name__}`, got {options.__class__.__name__}.')
            
            # Copy it
            options_processed = list(options)
            
            if __debug__:
                if len(options_processed) > APPLICATION_COMMAND_OPTIONS_MAX:
                    raise AssertionError(f'`options` length can be in range '
                        f'[0:{APPLICATION_COMMAND_OPTIONS_MAX}], got {len(options_processed)!r}; {options!r}')
                
                for index, option in enumerate(options_processed):
                    if not isinstance(option, ApplicationCommandOption):
                        raise AssertionError(f'`options` was given either as `list` or `tuple`, but it\'s element '
                            f'At index {index!r} is not {ApplicationCommandOption.__name__} instance, but '
                            f'{option.__class__.__name__}; got {options!r}.')
                    
                    if option.type is ApplicationCommandOptionType.sub_command_group:
                        raise AssertionError(f'`options` element {index}\'s type is cub-command group option, but'
                             f'sub-command groups cannot be added under sub-command groups; got {options!r}.')
            
            if not options_processed:
                options_processed = None
        
        if (choices_processed is not None):
            if type_ is ApplicationCommandOptionType.string:
                expected_choice_type = str
            elif type_ is ApplicationCommandOptionType.integer:
                expected_choice_type = int
            elif type_ is ApplicationCommandOptionType.float:
                expected_choice_type = float
            else:
                raise TypeError(f'`choices` is bound to string, integer and float option type, got '
                    f'choices={choices!r}, type={type_!r}.')
            
            for index, choice in enumerate(choices):
                if not isinstance(choice.value, expected_choice_type):
                    raise TypeError(f'`choices` element\'s {index!r} value\'s type is not '
                        f'`{expected_choice_type.__name__}` as expected from the received command option type: '
                        f'{type_!r}')
                pass
        
        if (channel_types is None):
            channel_types_processed = None
        else:
            channel_types_processed = None
            
            iterator = getattr(type(channel_types), '__iter__', None)
            if (iterator is None):
                raise TypeError(f'`channel_types` is neither `None` nor `iterable`, got '
                    f'{channel_types.__class__.__anme__}.')
            
            for channel_type in iterator(channel_types):
                if type(channel_type) is int:
                    pass
                elif isinstance(channel_type, int):
                    channel_type = int(channel_type)
                else:
                    raise TypeError(f'`channel_types` may include only `int` instances, got '
                        f'{channel_type.__class__.__name__}; {channel_type!r}.')
                
                if channel_types_processed is None:
                    channel_types_processed = set()
                
                channel_types_processed.add(channel_type)
        
            if channel_types_processed:
                channel_types_processed = tuple(sorted(channel_types_processed))
            else:
                channel_types_processed = None
        
        if __debug__:
            if (channel_types_processed is not None) and (type_ is not ApplicationCommandOptionType.channel):
                raise AssertionError(f'`channel_types` is only meaningful if `type_` is '
                    f'`{ApplicationCommandOptionType.__name__}.channel`.')
        
            if not isinstance(autocomplete, bool):
                raise AssertionError(f'`autocomplete` can be `bool` instance, got {autocomplete.__class__.__name__}.')
            
            if autocomplete:
                if (choices_processed is not None):
                    raise AssertionError(f'`autocomplete` and `choices` parameters are mutually exclusive.')
                
                if (type_ is not ApplicationCommandOptionType.string):
                    raise AssertionError(f'`autocomplete` is only available for string option type, got {type_!r}')
        
        self = object.__new__(cls)
        self.name = name
        self.description = description
        self.type = type_
        self.default = default
        self.required = required
        self.choices = choices_processed
        self.options = options_processed
        self.channel_types = channel_types_processed
        self.autocomplete = autocomplete
        return self
    
    
    def add_option(self, option):
        """
        Adds a new option to the application command option.
        
        Parameters
        ----------
        option : ``ApplicationCommandOption``
            The option to add.
        
        Returns
        -------
        self : ``ApplicationCommandOption``
        
        Raises
        ------
        TypeError
            If the source application command's type is not a sub-command group type.
        AssertionError
            - If `option` is not ``ApplicationCommandOption`` instance.
            - If the ``ApplicationCommandOption`` has already `25` options.
            - If `option` is a sub command group option.
        """
        if self.type is not ApplicationCommandOptionType.sub_command_group:
            raise TypeError(f'`option` can be added only if the command option\s type is sub command option, '
                f'got option={option!r}, self={self!r}.')
        
        if __debug__:
            if not isinstance(option, ApplicationCommandOption):
                raise AssertionError(f'`option` can be given as {ApplicationCommandOption.__name__} instance, got '
                    f'{option.__class__.__name__}.')
        
            if option.type is ApplicationCommandOptionType.sub_command_group:
                raise AssertionError(f'`option`\'s type is sub-command group option, but sub-command groups cannot be '
                    f'added under sub-command groups; got {option!r}.')
        
        options = self.options
        if options is None:
            self.options = options = []
        else:
            if __debug__:
                if len(options) >= APPLICATION_COMMAND_OPTIONS_MAX:
                    raise AssertionError(f'`option` cannot be added if the {ApplicationCommandOption.__name__} has '
                        f'already `{APPLICATION_COMMAND_OPTIONS_MAX}` options.')
        
        options.append(option)
        return self
    
    
    def add_choice(self, choice):
        """
        Adds a ``ApplicationCommandOptionChoice`` to the application command option.
        
        Parameters
        ----------
        choice : ``ApplicationCommandOptionChoice`` or `tuple` (`str`, (`str`, `int`, `float`))
            The choice to add.
        
        Returns
        -------
        self : ``ApplicationCommandOption``
        
        Raises
        ------
        TypeError
            - If the source application command's type is not a string, int nor float group type.
            - If the `choice`'s value's type is not the expected one by the command option's type.
            - If `choice`'s type is neither ``ApplicationCommandOptionChoice`` nor a `tuple` representing it's `.name`
                nad `.value`.
        AssertionError
            If the application command option has already `25` choices.
        """
        if isinstance(choice, ApplicationCommandOptionChoice):
            pass
        elif isinstance(choice, tuple):
            if len(choice) != 2:
                raise TypeError(f'If `choice` is given as `tuple` it\'s length should be `2` representing a '
                    f'{ApplicationCommandOptionChoice.__name__}\s `.name` and `.value`.')
            
            choice = ApplicationCommandOptionChoice(*choice)
        else:
            raise TypeError(f'`choice` can be given as {ApplicationCommandOptionChoice.__name__} instance or a `tuple` '
                f'representing one with i\'s respective `.name` and `.value` as it\'s elements, got '
                f'{choice.__class__.__name__}.')
        
        type_ = self.type
        if type_ is ApplicationCommandOptionType.string:
            expected_choice_type = str
        elif type_ is ApplicationCommandOptionType.integer:
            expected_choice_type = int
        elif type_ is ApplicationCommandOptionType.float:
            expected_choice_type = float
        else:
            raise TypeError(f'`choice` is bound to string, integer and float choice type, got choice={choice!r}, '
                f'self={self!r}.')
        
        if not isinstance(choice.value, expected_choice_type):
            raise TypeError(f'`choice` value\'s type is not `{expected_choice_type.__name__}` as expected from the '
                f'received command choice type: {type_!r}')
        
        choices = self.choices
        if choices is None:
            self.choices = choices = []
        else:
            if __debug__:
                if len(choices) >= APPLICATION_COMMAND_CHOICES_MAX:
                    raise AssertionError(f'`choice` cannot be added if the {ApplicationCommandOption.__name__} has '
                        f'already `{APPLICATION_COMMAND_CHOICES_MAX}` choices.')
        
        choices.append(choice)
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new ``ApplicationCommandOption`` instance from the received data from Discord.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received application command option data.
        
        Returns
        -------
        self : ``ApplicationCommandOption``
            The created application command option.
        """
        self = object.__new__(cls)
        choice_datas = data.get('choices', None)
        if (choice_datas is None) or (not choice_datas):
            choices = None
        else:
            choices = [ApplicationCommandOptionChoice.from_data(choice_data) for choice_data in choice_datas]
        self.choices = choices
        
        self.default = data.get('default', False)
        
        self.description = data['description']
        self.name = data['name']
        
        option_datas = data.get('options', None)
        if (option_datas is None) or (not option_datas):
            options = None
        else:
            options = [ApplicationCommandOption.from_data(option_data) for option_data in option_datas]
        self.options = options
        
        self.required = data.get('required', False)
        
        channel_types = data.get('channel_types', None)
        if (channel_types is None) or (not channel_types):
            channel_types = None
        else:
            channel_types = tuple(sorted(channel_types))
        self.channel_types = channel_types
        
        self.autocomplete = data.get('autocomplete', False)
        
        self.type = ApplicationCommandOptionType.get(data['type'])
        return self
    
    
    def to_data(self):
        """
        Converts the application command option to a json serializable object.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        data = {
            'description' : self.description,
            'name' : self.name,
            'type' : self.type.value,
        }
        
        choices = self.choices
        if (choices is not None):
            data['choices'] = [choice.to_data() for choice in choices]
        
        
        if self.default:
            data['default'] = True
        
        options = self.options
        if (options is not None):
            data['options'] = [option.to_data() for option in options]
        
        if self.required:
            data['required'] = True
        
        channel_types = self.channel_types
        if (channel_types is not None):
            data['channel_types'] = channel_types
        
        if self.autocomplete:
            data['autocomplete'] = True
        
        return data
    
    
    def __repr__(self):
        """Returns the application command option's representation."""
        repr_parts = [
            '<', self.__class__.__name__,
            ', name=', repr(self.name),
        ]
        
        if self.autocomplete:
            repr_parts.append(' (auto completed)')
        
        repr_parts.append(', description=')
        repr_parts.append(repr(self.description))
        repr_parts.append(', type=')
        
        type_ = self.type
        repr_parts.append(repr(type_.value))
        repr_parts.append(' (')
        repr_parts.append(type_.name)
        repr_parts.append(')')
        
        if self.default:
            repr_parts.append(', default=True')
        
        if self.required:
            repr_parts.append(', required=True')
        
        choices = self.choices
        if (choices is not None):
            repr_parts.append(', choices=[')
            
            index = 0
            limit = len(choices)
            
            while True:
                choice = choices[index]
                index += 1
                repr_parts.append(repr(choice))
                
                if index == limit:
                    break
                
                repr_parts.append(', ')
                continue
        
        options = self.options
        if (options is not None):
            repr_parts.append(', options=[')
            
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
        
        channel_types = self.channel_types
        if (channel_types is not None):
            repr_parts.append(', channel_types=[')
            
            index = 0
            limit = len(channel_types)
            
            while True:
                channel_type = channel_types[index]
                index += 1
                repr_parts.append(repr(channel_type))
                
                if index == limit:
                    break
                
                repr_parts.append(', ')
                continue
            
            repr_parts.append(']')
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    def copy(self):
        """
        Copies the ``ApplicationCommandOption``.
        
        Returns
        -------
        new : ``ApplicationCommandOption``
        """
        new = object.__new__(type(self))
        
        choices = self.choices
        if (choices is not None):
            choices = choices.copy()
        new.choices = choices
        
        new.default = self.default
        new.description = self.description
        new.name = self.name
        
        options = self.options
        if (options is not None):
            options = [option.copy() for option in options]
        new.options = options
        
        new.required = self.required
        new.type = self.type
        
        channel_types = self.channel_types
        if (channel_types is not None):
            channel_types = tuple(channel_types)
        new.channel_types = channel_types
        
        new.autocomplete = self.autocomplete
        
        return new
    
    def __eq__(self, other):
        """Returns whether the two options are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.choices != other.choices:
            return False
        
        if self.default != other.default:
            return False
        
        if self.description != other.description:
            return False
        
        if self.name != other.name:
            return False
        
        if self.options != other.options:
            return False
        
        if self.required != other.required:
            return False
        
        if self.type is not other.type:
            return False
        
        if self.channel_types != other.channel_types:
            return False
        
        if self.autocomplete != other.autocomplete:
            return False
        
        return True
    
    def __len__(self):
        """Returns the application command option's length."""
        length = len(self.name) + len(self.description)
        
        choices = self.choices
        if (choices is not None):
            for choice in choices:
                length += len(choice)
        
        options = self.options
        if (options is not None):
            for option in options:
                length += len(option)
        
        return length


class ApplicationCommandOptionChoice:
    """
    A choice of a ``ApplicationCommandOption``.
    
    Attributes
    ----------
    name : `str`
        The choice's name. It's length can be in range [1:100].
    value : `str`, `int` or `float`
        The choice's value.
    """
    __slots__ = ('name', 'value')
    
    def __new__(cls, name, value):
        """
        Creates a new ``ApplicationCommandOptionChoice`` instance with the given parameters.
        
        Parameters
        ----------
        name : `str`
            The choice's name. It's length can be in range [1:100].
        value : `str`, `int` or `float`
            The choice's value.
        
        Raises
        ------
        AssertionError
            - If `name` is not `str` instance.
            - If `name`'s length is out of range [1:100].
            - If `value` is neither `str`, `int` nor `float` instance.
            - If `value` is `str` and it's length is out of range [0:100].
        """
        if __debug__:
            if not isinstance(name, str):
                raise AssertionError(f'`name` can be given as `str` instance, got {name.__class__.__name__}.')
            
            name_length = len(name)
            if name_length < APPLICATION_COMMAND_CHOICE_NAME_LENGTH_MIN or \
                    name_length > APPLICATION_COMMAND_CHOICE_NAME_LENGTH_MAX:
                raise AssertionError(f'`name` length can be in range '
                    f'[{APPLICATION_COMMAND_CHOICE_NAME_LENGTH_MIN}:{APPLICATION_COMMAND_CHOICE_NAME_LENGTH_MAX}], '
                    f'got {name_length!r}; {name!r}.')
            
            if isinstance(value, int):
                pass
            elif isinstance(value, str):
                value_length = len(value)
                if value_length < APPLICATION_COMMAND_CHOICE_VALUE_LENGTH_MIN or \
                        value_length > APPLICATION_COMMAND_CHOICE_VALUE_LENGTH_MAX:
                    raise AssertionError(f'`value` length` can be in range '
                        f'[{APPLICATION_COMMAND_CHOICE_VALUE_LENGTH_MIN}:{APPLICATION_COMMAND_CHOICE_NAME_LENGTH_MAX}]'
                        f'got {value_length!r}; {value!r}.')
            elif isinstance(value, float):
                pass
            else:
                raise AssertionError(f'`value` type can be either `str`, `int` or `float`, '
                    f'got {value.__class__.__name__}.')
        
        self = object.__new__(cls)
        self.name = name
        self.value = value
        return self
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new ``ApplicationCommandOptionChoice`` instance from the received data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            The received application command option choice data.
        
        Returns
        -------
        self : ``ApplicationCommandOptionChoice``
            The created choice.
        """
        self = object.__new__(cls)
        self.name = data['name']
        self.value = data['value']
        return self
    
    def to_data(self):
        """
        Converts the application command option choice to a json serializable object.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        return {
            'name': self.name,
            'value': self.value,
        }
    
    def __repr__(self):
        """Returns the application command option choice's representation."""
        return f'<{self.__class__.__name__} name={self.name!r}, value={self.value!r}>'
    
    def __eq__(self, other):
        """Returns whether the two choices are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.name != other.name:
            return False
        
        if self.value != other.value:
            return False
        
        return True
    
    def __len__(self):
        """Returns the application command choice's length."""
        length = len(self.name)
        value = self.value
        if isinstance(value, str):
            length += len(value)
        
        return length


class ApplicationCommandPermission:
    """
    Stores am ``ApplicationCommand``'s overwrites.
    
    Attributes
    ----------
    application_command_id : `int`
        The identifier of the respective ``ApplicationCommand``.
    application_id : `int`
        The application command's application's identifier.
    guild_id : `int`
        The identifier of the respective guild.
    permission_overwrites : `None` or `list` of ``ApplicationCommandPermissionOverwrite``
        The application command permissions overwrites relating to the respective application command in the guild.
    """
    __slots__ = ('application_command_id', 'application_id', 'guild_id', 'permission_overwrites')
    
    def __new__(cls, application_command, *, permission_overwrites=None, overwrites=None):
        """
        Creates a new ``ApplicationCommandPermission`` instance from the given parameters.
        
        Parameters
        ----------
        application_command : ``ApplicationCommand`` or `int`
            The application command's identifier.
        permission_overwrites : `None` or (`list`, `set`, `tuple`) of ``ApplicationCommandPermissionOverwrite`
                , Optional (Keyword only)
            Overwrites for the application command.
        
        Raises
        ------
        TypeError
            - If `application_command` was not given neither as ``ApplicationCommand`` nor as `int` instance.
        AssertionError
            - If `permission_overwrites` was not give neither as `None`, `list`, `set` or `tuple`.
            - If `permission_overwrites` contains a non ``ApplicationCommandPermissionOverwrite`` element.
            - If `permission_overwrites` length is over `10`.
        """
        if (overwrites is not None):
            warnings.warn(
                f'`ApplicationCommandPermission.__new__`\'s `overwrites` parameter is deprecated, '
                f'and will be removed in 2021 November. '
                f'Please use `permission_overwrites` instead.',
                FutureWarning)
            
            permission_overwrites = overwrites
        
        if isinstance(application_command, ApplicationCommand):
            application_command_id = application_command.id
        else:
            application_command_id = maybe_snowflake(application_command)
            if application_command_id is None:
                raise TypeError(f'`application_command` can be given as `{ApplicationCommand.__name__}`, or as `int` '
                    f'instance, got {application_command.__class__.__name__}.')
        
        if permission_overwrites is None:
            permission_overwrites_processed = None
        else:
            if __debug__:
                if not isinstance(permission_overwrites, (list, set, tuple)):
                    raise AssertionError(f'`permission_overwrites` can be given either as `None` or as `list`, '
                        f'`set`, `tuple`instance, got {permission_overwrites.__class__.__name__}.')
            
            permission_overwrites_processed = []
            
            for permission_overwrite in permission_overwrites:
                if __debug__:
                    if not isinstance(permission_overwrite, ApplicationCommandPermissionOverwrite):
                        raise AssertionError(f'`permission_overwrites` contains a non '
                            f'{ApplicationCommandPermissionOverwrite.__name__} element, got '
                            f'{overwrite.__class__.__name__}.')
                
                permission_overwrites_processed.append(permission_overwrite)
                
            
            if permission_overwrites_processed:
                if __debug__:
                    if len(overwrites) >= APPLICATION_COMMAND_PERMISSION_OVERWRITE_MAX:
                        raise AssertionError(f'`permission_overwrites` can contain up to '
                            f'`{APPLICATION_COMMAND_PERMISSION_OVERWRITE_MAX}` permission_overwrites, which is passed, '
                            f'got {len(permission_overwrites)!r}.')
            else:
                permission_overwrites_processed = None
        
        self = object.__new__(cls)
        self.application_command_id = application_command_id
        self.application_id = 0
        self.guild_id = 0
        self.permission_overwrites = permission_overwrites_processed
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new ``ApplicationCommandPermission`` instance.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Application command data.
        
        Returns
        -------
        self : ``ApplicationCommandPermission``
        """
        permission_overwrite_datas = data['permissions']
        if permission_overwrite_datas:
            permission_overwrites = [
                ApplicationCommandPermissionOverwrite.from_data(permission_overwrite_data) for
                permission_overwrite_data in permission_overwrite_datas
            ]
            
        else:
            permission_overwrites = None
        
        self = object.__new__(cls)
        self.application_command_id = int(data['id'])
        self.application_id = int(data['application_id'])
        self.guild_id = int(data['guild_id'])
        self.permission_overwrites = permission_overwrites
        return self
    
    
    def to_data(self):
        """
        Converts the application command permission to a json serializable object.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        data = {
            'id': self.application_command_id,
            'application_id': self.application_id,
            'guild_id': self.guild_id,
        }
        
        permission_overwrites = self.permission_overwrites
        if permission_overwrites is None:
            permission_overwrite_datas = []
        else:
            permission_overwrite_datas = [
                permission_overwrite.to_data() for permission_overwrite in permission_overwrites
            ]
        
        data['permissions'] = permission_overwrite_datas
        
        return data
    
    def __repr__(self):
        """Returns the application command permission's representation."""
        repr_parts = ['<', self.__class__.__name__, ' application_command_id=', repr(self.application_command_id),
            ' guild_id=', repr(self.guild_id), ', permission overwrite count=']
        
        permission_overwrites = self.overwrites
        if permission_overwrites is None:
            permission_overwrite_count = '0'
        else:
            permission_overwrite_count = repr(len(permission_overwrites))
        
        repr_parts.append(permission_overwrite_count)
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    def __eq__(self, other):
        """Returns whether the two application command permission's are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # No need to compare application_id, since `application_command_id` are already unique.
        if self.application_command_id != other.application_command_id:
            return False
        
        if self.guild_id != other.guild_id:
            return False
        
        if self.permission_overwrites != other.permission_overwrites:
            return False
        
        return True
    
    def __hash__(self):
        """Returns the application command overwrite's hash value."""
        hash_ = self.application_command_id ^ self.guild_id
        permission_overwrites = self.permission_overwrites
        if (permission_overwrites is not None):
            for permission_overwrite in permission_overwrites:
                hash_ ^= hash(permission_overwrite)
        
        return hash_
    
    def copy(self):
        """
        Copies the application command permission.
        
        Returns
        -------
        new : ``ApplicationCommandPermission``
        """
        new = object.__new__(type(self))
        
        new.application_id = self.application_id
        new.application_command_id = self.application_command_id
        new.guild_id = self.guild_id
        
        permission_overwrites = self.permission_overwrites
        if (permission_overwrites is not None):
            permission_overwrites = [permission_overwrite.copy() for permission_overwrite in permission_overwrites]
        
        new.permission_overwrites = permission_overwrites
        
        return new
    
    def add_permission_overwrite(self, permission_overwrite):
        """
        Adds an application command permission overwrite to the overwrites of the application command permission.
        
        Parameters
        ----------
        permission_overwrite : ``ApplicationCommandPermissionOverwrite``
            The overwrite to add.
        
        Raises
        ------
        AssertionError
            - If `overwrite` is not ``ApplicationCommandPermissionOverwrite`` instance.
            - If the application command permission has `10` overwrites already.
        """
        if __debug__:
            if not isinstance(permission_overwrite, ApplicationCommandPermissionOverwrite):
                raise AssertionError(f'`permission_overwrite` can be given as '
                    f'{ApplicationCommandPermissionOverwrite.__name__}  instance, got '
                    f'{permission_overwrite.__class__.__name__}.')
        
        permission_overwrites = self.permission_overwrites
        if permission_overwrites is None:
            self.permission_overwrites = permission_overwrites = []
        else:
            if __debug__:
                if len(permission_overwrites) >= APPLICATION_COMMAND_PERMISSION_OVERWRITE_MAX:
                    raise AssertionError(f'`permission_overwrites` can contain up to '
                        f'`{APPLICATION_COMMAND_PERMISSION_OVERWRITE_MAX}` permission_overwrites, which is already '
                        f'reached.')
        
        permission_overwrites.append(permission_overwrite)


class ApplicationCommandPermissionOverwrite:
    """
    Represents an application command's allow/disallow overwrite for the given entity.
    
    Attributes
    ----------
    allow : `bool`
        Whether the respective command is allowed for the represented entity.
    target_id : `int`
        The represented entity's identifier.
    target_type : ``ApplicationCommandPermissionOverwriteTargetType`
        The target entity's type.
    """
    __slots__ = ('allow', 'target_id', 'target_type')
    
    def __new__(cls, target, allow):
        """
        Creates a new ``ApplicationCommandPermission`` instance with the given parameters.
        
        Parameters
        ----------
        target : ``ClientUserBase`` or ``Role``, `tuple` ((``ClientUserBase``, ``Role`` type) or \
                `str` (`'Role'`, `'role'`, `'User'`, `'user'`), `int`)
            The target entity of the application command permission overwrite.
            
            The expected type & value might be pretty confusing, but the target was it to allow relaxing creation.
            To avoid confusing, here is a list of the expected structures:
            
            - ``Role`` instance
            - ``ClientUserBase`` instance
            - `tuple` (``Role`` type, `int`)
            - `tuple` (``ClientUserBase`` instance, `int`)
            - `tuple` (`'Role'`, `int`)
            - `tuple` (`'role'`, `int`)
            - `tuple` (`'User'`, `int`)
            - `tuple` (`'user'`, `int`)
        
        allow : `bool`
            Whether the respective application command should be enabled for the respective entity.
        
        Raises
        ------
        TypeError
            If `target` was not given as any of the expected types & values.
        AssertionError
            If `allow` was not given as `bool` instance.
        """
        # GOTO
        while True:
            if isinstance(target, Role):
                target_type = APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_ROLE
                target_id = target.id
                target_lookup_failed = False
                break
            
            if isinstance(target, ClientUserBase):
                target_type = APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_USER
                target_id = target.id
                target_lookup_failed = False
                break
            
            if isinstance(target, tuple) and len(target) == 2:
                target_maybe, target_id_maybe = target
                
                if isinstance(target_maybe, type):
                    if issubclass(target_maybe, Role):
                        target_type = APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_ROLE
                    elif issubclass(target_maybe, ClientUserBase):
                        target_type = APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_USER
                    else:
                        target_lookup_failed = True
                        break
                
                elif isinstance(target_maybe, str):
                    if target_maybe in ('Role', 'role'):
                        target_type = APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_ROLE
                    elif target_maybe in ('User', 'user'):
                        target_type = APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_USER
                    else:
                        target_lookup_failed = True
                        break
                
                else:
                    target_lookup_failed = True
                    break
                
                if type(target_id_maybe) is int:
                    target_id = target_id_maybe
                elif isinstance(target_id_maybe, int):
                    target_id = int(target_id_maybe)
                else:
                    target_lookup_failed = True
                    break
                
                target_lookup_failed = False
                break
            
            target_lookup_failed = True
            break
        
        if target_lookup_failed:
            raise TypeError(f'`target` can be given either as {Role.__name__}, {ClientUserBase.__name__}, '
                f'or as a `tuple` (({Role.__name__}, {User.__name__}, {UserBase.__name__} type or `str` '
                f'(`\'Role\'`, `\'role\'`, `\'User\'`, `\'user\'`)), `int`), got {target.__class__.__name__}: '
                f'{target!r}.')
        
        if __debug__:
            if not isinstance(allow, bool):
                raise AssertionError(f'`allow` can be given as `bool` instance, got {allow.__class__.__name__}.')
        
        self = object.__new__(cls)
        self.allow = allow
        self.target_id = target_id
        self.target_type = target_type
        return self
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new ``ApplicationCommandPermissionOverwrite`` instance from the received data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            The received application command permission overwrite data.
        
        Returns
        -------
        self : ``ApplicationCommandPermission``
            The created application command option.
        """
        self = object.__new__(cls)
        self.allow = data['permission']
        self.target_id = int(data['id'])
        self.target_type = ApplicationCommandPermissionOverwriteTargetType.get(data['type'])
        return self
    
    
    def to_data(self):
        """
        Converts the application command permission overwrite to a json serializable object.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        return {
            'permission': self.allow,
            'id': self.target_id,
            'type': self.target_type.value,
        }
    
    
    @property
    def target(self):
        """
        Returns the application command overwrite's target entity.
        
        Returns
        -------
        target : `None`, ``Role``, ``ClientUserBase``
        """
        target_type = self.target_type
        target_id = self.target_id
        
        if target_type is APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_ROLE:
            target = create_partial_role_from_id(target_id)
        
        elif target_type is APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_USER:
            target = create_partial_user_from_id(target_id)
        
        else:
            target = None
        
        return target
    
    
    def __repr__(self):
        """Returns the application command permission overwrite's representation."""
        return (
            f'<{self.__class__.__name__} target_type={self.target_type.name}, target_id={self.target_id!r}, '
            f'allow={self.allow!r}>'
        )
    
    
    def __eq__(self, other):
        """Returns whether the two application command overwrites are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.allow != other.allow:
            return False
        
        if self.target_type is not other.target_type:
            return False
        
        if self.target_id != other.target_id:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the application command permission overwrite's hash value."""
        return self.target_type.value^(self.allow<<8)^self.target_id
    
    
    def copy(self):
        """
        Copies the application command permission overwrite.
        
        Returns
        -------
        new : ``ApplicationCommandPermissionOverwrite``
        """
        new = object.__new__(type(self))
        
        new.allow = self.allow
        new.target_type = self.target_type
        new.target_id = self.target_id
        
        return new
    
    
    def __gt__(self, other):
        """Returns whether self is greater than other."""
        if type(self) is not type(other):
            return NotImplemented
        
        self_type_value = self.target_type.value
        other_type_value = other.target_type.value
        
        if self_type_value > other_type_value:
            return True
        
        if self_type_value < other_type_value:
            return False
        
        if self_type_value == APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_ROLE:
            self_target_id = self.target_id
            other_target_id = other.target_id
            
            self_role = ROLES.get(self_target_id, None)
            other_role = ROLES.get(other_target_id, None)
            if self_role is None:
                if other_role is None:
                    return (self_target_id > other_target_id)
                else:
                    return False
            else:
                if other_role is None:
                    return True
                else:
                    return (self_role > other_role)
        
        if self_type_value == APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_USER:
            return (self.target_id > other.target_id)
        
        # Should not happen
        return False
    
    
    def __lt__(self, other):
        """Returns whether self is greater than other."""
        if type(self) is not type(other):
            return NotImplemented
        
        self_type_value = self.target_type.value
        other_type_value = other.target_type.value
        
        if self_type_value > other_type_value:
            return False
        
        if self_type_value < other_type_value:
            return True
        
        if self_type_value == APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_ROLE:
            self_target_id = self.target_id
            other_target_id = other.target_id
            
            self_role = ROLES.get(self_target_id, None)
            other_role = ROLES.get(other_target_id, None)
            if self_role is None:
                if other_role is None:
                    return (self_target_id < other_target_id)
                else:
                    return True
            else:
                if other_role is None:
                    return False
                else:
                    return (self_role < other_role)
        
        if self_type_value == APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_USER:
            return (self.target_id < other.target_id)
        
        # Should not happen
        return True
