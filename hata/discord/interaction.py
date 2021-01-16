# -*- coding: utf-8 -*-
__all__ = ('ApplicationCommand', 'ApplicationCommandInteraction', 'ApplicationCommandInteractionOption',
    'ApplicationCommandOption', 'ApplicationCommandOptionChoice', 'InteractionResponseTypes')

from .bases import DiscordEntity
from .preinstanced import ApplicationCommandOptionType
from .client_core import APPLICATION_COMMANDS
from .preconverters import preconvert_preinstanced_type
from .utils import is_valid_application_command_name, DATETIME_FORMAT_CODE

from ..backend.utils import modulize

class ApplicationCommand(DiscordEntity, immortal=True):
    """
    Represents a Discord slash command.
    
    Attributes
    ----------
    id : `int`
        The application command's id.
    application_id : `int`
        The application command's application's id.
    description : `str`
        The command's description. It's length can be in range [2:100].
    name : `str`
        The name of the command. It's length can be in range [1:32].
    options : `None` or `list` of ``ApplicationCommandOption``
        The parameters of the command. It's length can be in range [0:10]. If would be set as empty list, instead is
        set as `None`.
    
    Notes
    -----
    ``ApplicationCommand`` instances are weakreferable.
    """
    __slots__ = ('application_id', 'description', 'name', 'options')
    
    def __new__(cls, name, description, *, options=None):
        """
        Creates a new ``ApplicationCommand`` instance with the given parameters.
        
        Parameters
        ----------
        name : `str`
            The name of the command. It's length can be in range [1:32].
        description : `str`
            The command's description. It's length can be in range [2:100].
        options : `None` or (`list` or `tuple`) of ``ApplicationCommandOption``, Optional
            The parameters of the command. It's length can be in range [0:10].
        
        Raises
        ------
        AssertionError
            - If `name` was not given as `str` instance.
            - If `name` length is out of range [3:32].
            - If `name` contains unexpected character.
            - If `description` was not given as `str` instance.
            - If `description` length is out of range [1:100].
            - If `options` was not given neither as `None` nor as (`list` or `tuple`) of ``ApplicationCommandOption``
                instances.
            - If `options`'s length is out of range [0:10].
        """
        if __debug__:
            if not isinstance(name, str):
                raise AssertionError(f'`name` can be given as `str` instance, got {name.__class__.__name__}.')
            
            name_ln = len(name)
            if name_ln < 3 or name_ln > 32:
                raise AssertionError(f'`name` length can be in range [3:32], got {name_ln!r}; {name!r}.')
            
            if not is_valid_application_command_name(name):
                raise AssertionError(f'`name` contains an unexpected character; Expected pattern: '
                    f'{APPLICATION_COMMAND_NAME_RP.pattern!r}; Got {name!r}.')
            
            if not isinstance(description, str):
                raise AssertionError(f'`description` can be given as `str` instance, got '
                    f'{description.__class__.__name__}.')
            
            description_ln = len(description)
            if description_ln < 2 or description_ln > 100:
                raise AssertionError(f'`description` length can be in range [2:100], got {description_ln!r}; '
                    f'{description!r}.')
            
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
                    if len(options_processed) > 10:
                        raise AssertionError(f'`options` length can be in range [0:10], got '
                            f'{len(options_processed)!r}; {options!r}')
                    
                    for index, option in enumerate(options_processed):
                        if not isinstance(option, ApplicationCommandOption):
                            raise AssertionError(f'`options` was given either as `list` or `tuple`, but it\'s element '
                                f'At index {index!r} is not {ApplicationCommandOption.__name__} instance, but '
                                f'{option.__class__.__name__}.')
            
            else:
                options_processed = None
        
        self = object.__new__(cls)
        self.id = 0
        self.application_id = 0
        self.name = name
        self.description = description
        self.options = options_processed
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
            - If the ``ApplicationCommand`` has already `10` options.
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
                if len(options) >= 10:
                    raise AssertionError(f'`option` cannot be added if the {ApplicationCommandOption.__name__} has '
                        f'already `10` options.')
        
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
        
        self._update_no_return(data)
        return self
    
    def _update_no_return(self, data):
        """
        Updates the application command with the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received application command data.
        """
        self.description = data['description']
        self.name = data['name']
        
        option_datas = data.get('options')
        if (option_datas is None) or (not option_datas):
            options = None
        else:
            options = [ApplicationCommandOption.from_data(option_data) for option_data in option_datas]
        self.options = options
    
    def _update(self, data):
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
            
            +---------------+---------------------------------------------------+
            | Keys          | Values                                            |
            +===============+===================================================+
            | description   | `str`                                             |
            +---------------+---------------------------------------------------+
            | name          | `str`                                             |
            +---------------+---------------------------------------------------+
            | options       | `None` or `list` of ``ApplicationCommandOption``  |
            +---------------+---------------------------------------------------+
        """
        old_attributes = {}
        
        description = data['description']
        if self.description != description:
            old_attributes['description'] = self.description
            self.description = description
        
        name = data['name']
        if self.name != name:
            old_attributes['name'] = self.name
            self.name = name
        
        option_datas = data.get('options')
        if (option_datas is None) or (not option_datas):
            options = None
        else:
            options = [ApplicationCommandOption.from_data(option_data) for option_data in option_datas]
        
        if self.options != options:
            old_attributes['options'] = self.options
            self.options = options
        
        return old_attributes
    
    def to_data(self):
        """
        Converts the application command to a json serializable object.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        data = {
            'description' : self.description,
            'name' : self.name,
                }
    
        options = self.options
        if (options is not None):
            data['options'] = [option.to_data() for option in options]
        
        return data
    
    def __repr__(self):
        """Returns the application command's representation."""
        result = [
            '<', self.__class__.__name__,
                ]
        
        id_ = self.id
        if id_ == 0:
            result.append(' partial')
        else:
            result.append(' id=')
            result.append(repr(id_))
            result.append(', application_id=')
            result.append(repr(self.application_id))
        
        result.append(' name=')
        result.append(repr(self.name))
        result.append(', description=')
        result.append(repr(self.description))
        
        options = self.options
        if (options is not None):
            result.append(', options=[')
            
            index = 0
            limit = len(options)
            
            while True:
                option = options[index]
                index += 1
                result.append(repr(option))
                
                if index == limit:
                    break
                
                result.append(', ')
                continue
            
            result.append(']')
        
        result.append('>')
        
        return ''.join(result)
    
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
    def _from_edit_data(cls, data, id_, application_id):
        """
        Creates an application command with the given parameters after an application command edition took place.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Application command data returned by it's ``.to_data`` method.
        id_ : `int`
            The unique identifier number of the newly created application command.
        application_id : `int`
            The new application identifier number of the newly created application command.
        
        Returns
        -------
        self : ``ApplicationCommand``
            The newly created or updated application command.
        """
        try:
            self = APPLICATION_COMMANDS[id_]
        except KeyError:
            self = object.__new__(cls)
            self.id = id_
            self.application_id = application_id
            APPLICATION_COMMANDS[id_] = self
        
        self._update_no_return(data)
        
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
        
        options = self.options
        if (options is not None):
            options = [option.copy() for option in options]
        new.options = options
        
        return new
    
    def __eq__(self, other):
        """Returns whether the two application commands are equal."""
        if not isinstance(other, ApplicationCommand):
            return NotImplemented
        
        # If both entity is not partial, leave instantly by comparing id.
        self_id = self.id
        other_id = other.id
        if self_id and other_id:
            if self_id == other_id:
                return True
            
            return False
        
        if self.description != other.description:
            return False
        
        if self.name != other.name:
            return False
        
        if self.options != other.options:
            return False
        
        return True
    
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
    
    def __str__(self):
        """Returns the application command's name."""
        return self.name
    
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
        ```
        >>> from hata import ApplicationCommand
        >>> application_command = ApplicationCommand('CakeLover', 'Sends a random cake recipe OwO')
        >>> application_command
        <ApplicationCommand partial name='CakeLover', description='Sends a random cake recipe OwO'>
        >>> # no code stands for str(application_command).
        >>> f'{application_command}'
        'CakeLover'
        >>> # 'd' stands for display name.
        >>> f'{application_command:d}'
        'cakelover'
        >>> # 'm' stands for mention.
        >>> f'{application_command:m}'
        '</CakeLover:0>'
        >>> # 'c' stands for created at.
        >>> f'{application_command:c}'
        '2021-01-03 20:17:36'
        ```
        """
        if not code:
            return self.__str__()
        
        if code == 'm':
            return f'</{self.name}:{self.id}>'
        
        if code == 'd':
            return self.display_name
        
        if code == 'c':
            return self.created_at.__format__(DATETIME_FORMAT_CODE)
        
        raise ValueError(f'Unknown format code {code!r} for object of type {self.__class__.__name__!r}')


class ApplicationCommandOption(object):
    """
    An option of an ``ApplicationCommand``.
    
    Attributes
    ----------
    choices : `None` or `list` of ``ApplicationCommandOptionChoice``
        Choices for `str` and `int` types for the user to pick from.
    default : `bool`
        Whether the option is the default one. Only one option can be `default`.
    description : `str`
        The description of the application command option. It's length can be in range [1:100].
    name : `str`
        The name of the application command option. It's length can be in range [1:32].
    options : `None` or `list` of ``ApplicationCommandOption``
        If the command's type is sub-command group type, then this nested option will be the parameters of the
        sub-command. It's length can be in range [0:10]. If would be set as empty list, instead is set as `None`.
    required : `bool`
        Whether the parameter is required. Defaults to `False`.
    type : ``ApplicationCommandOptionType``
        The option's type.
    """
    __slots__ = ('choices', 'default', 'description', 'name', 'options', 'required', 'type')
    
    def __new__(cls, name, description, type_, *, default=False, required=False, choices=None, options=None):
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
        default : `bool`, Optional
            Whether the option is the default one. Defaults to `False`.
        required : `bool`, Optional
            Whether the parameter is required. Defaults to `False`.
        choices : `None` or (`list` or `tuple`) of ``ApplicationCommandOptionChoice``, Optional
            The choices of the command for string or integer types. It's length can be in range [0:10].
        options : `None` or (`list` or `tuple`) of ``ApplicationCommandOption``, Optional
            The parameters of the command. It's length can be in range [0:10]. Only applicable for sub command groups.
        
        Raises
        ------
        TypeError
            - If `type_` was not given neither as `int` nor ``ApplicationCommandOptionType`` instance.
            - If `choices` was given meanwhile `type_` is neither string nor integer option type.
            - If `options` was given meanwhile `type_` is not a sub-command group option type.
            - If a choice's value's type not matched the expected type described `type_`.
        ValueError
            - If `type_` was given as `int` instance, but it do not matches any of the precreated
                ``ApplicationCommandOptionType``-s.
        AssertionError
            - If `name` was not given as `str` instance.
            - If `name` length is out of range [1:32].
            - If `description` was not given as `str` instance.
            - If `description` length is out of range [1:100].
            - If `options` was not given neither as `None` nor as (`list` or `tuple`) of ``ApplicationCommandOption``
                instances.
            - If `options`'s length is out of range [0:10].
            - If `default` was not given as `bool` instance.
            - If `required` was not given as `bool` instance.
            - If `choices` was not given neither as `None` nor as (`list` or `tuple`) of
                ``ApplicationCommandOptionChoice`` instances.
            - If an option is a sub command group option.
        """
        if __debug__:
            if not isinstance(name, str):
                raise AssertionError(f'`name` can be given as `str` instance, got {name.__class__.__name__}.')
            
            name_ln = len(name)
            if name_ln < 1 or name_ln > 32:
                raise AssertionError(f'`name` length can be in range [1:32], got {name_ln!r}; {name!r}.')
        
            if not isinstance(description, str):
                raise AssertionError(f'`description` can be given as `str` instance, got '
                    f'{description.__class__.__name__}.')
            
            description_ln = len(description)
            if description_ln < 2 or description_ln > 100:
                raise AssertionError(f'`description` length can be in range [2:100], got {description_ln!r}; '
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
                if len(choices_processed) > 10:
                    raise AssertionError(f'`choices` length can be in range [0:10], got {len(choices_processed)!r}; '
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
                if len(options_processed) > 10:
                    raise AssertionError(f'`options` length can be in range [0:10], got {len(options_processed)!r}; '
                        f'{options!r}')
                
                for index, option in enumerate(options_processed):
                    if not isinstance(option, ApplicationCommandOption):
                        raise AssertionError(f'`options` was given either as `list` or `tuple`, but it\'s element '
                            f'At index {index!r} is not {ApplicationCommandOption.__name__} instance, but '
                            f'{option.__class__.__name__}; got {options!r}.')
                    
                    if option.type is ApplicationCommandOptionType.SUB_COMMAND_GROUP:
                        raise AssertionError(f'`options` element {index}\'s type is cub-command group option, but'
                             f'sub-command groups cannot be added under sub-command groups; got {options!r}.')
            
            if not options_processed:
                options_processed = None
        
        if (choices_processed is not None):
            if type_ is ApplicationCommandOptionType.STRING:
                expected_choice_type = str
            elif type_ is ApplicationCommandOptionType.INTEGER:
                expected_choice_type = int
            else:
                raise TypeError(f'`choices` is bound to string and integer option type, got choices={choices!r}, '
                    f'type={type_!r}.')
            
            for index, choice in enumerate(choices):
                if not isinstance(choice.value, expected_choice_type):
                    raise TypeError(f'`choices` element\'s {index!r} value\'s type is not '
                        f'`{expected_choice_type.__name__}` as expected from the received command option type: '
                        f'{type_!r}')
                pass
        
        self = object.__new__(cls)
        self.name = name
        self.description = description
        self.type = type_
        self.default = default
        self.required = required
        self.choices = choices_processed
        self.options = options_processed
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
            - If the ``ApplicationCommandOption`` has already `10` options.
            - If `option` is a sub command group option.
        """
        if self.type is not ApplicationCommandOptionType.SUB_COMMAND_GROUP:
            raise TypeError(f'`option` can be added only if the command option\s type is sub command option, '
                f'got option={option!r}, self={self!r}.')
        
        if __debug__:
            if not isinstance(option, ApplicationCommandOption):
                raise AssertionError(f'`option` can be given as {ApplicationCommandOption.__name__} instance, got '
                    f'{option.__class__.__name__}.')
        
            if option.type is ApplicationCommandOptionType.SUB_COMMAND_GROUP:
                raise AssertionError(f'`option`\'s type is sub-command group option, but sub-command groups cannot be '
                    f'added under sub-command groups; got {options!r}.')
        
        options = self.options
        if options is None:
            self.options = options = []
        else:
            if __debug__:
                if len(options) >= 10:
                    raise AssertionError(f'`option` cannot be added if the {ApplicationCommandOption.__name__} has '
                        f'already `10` options.')
        
        options.append(option)
        return self
    
    def add_choice(self, choice):
        """
        Adds a ``ApplicationCommandOptionChoice`` to the application command option.
        
        Parameters
        ----------
        choice : ``ApplicationCommandOptionChoice`` or `tuple` (`str`, `str` or `int`)
            The choice to add.
        
        Returns
        -------
        self : ``ApplicationCommandOption``
        
        Raises
        ------
        TypeError
            - If the source application command's type is not a string nor int group type.
            - If the `choice`'s value's type is not the expected one by the command option's type.
            - If `choice`'s type is neither ``ApplicationCommandOptionChoice`` nor a `tuple` representing it's `.name`
                nad `.value`.
        AssertionError
            If the application command option has already 10 choices.
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
        if type_ is ApplicationCommandOptionType.STRING:
            expected_choice_type = str
        elif type_ is ApplicationCommandOptionType.INTEGER:
            expected_choice_type = int
        else:
            raise TypeError(f'`choice` is bound to string and integer choice type, got choice={choice!r}, '
                f'self={self!r}.')
        
        if not isinstance(choice.value, expected_choice_type):
            raise TypeError(f'`choice` value\'s type is not `{expected_choice_type.__name__}` as expected from the '
                f'received command choice type: {type_!r}')
        
        choices = self.choices
        if choices is None:
            self.choices = choices = []
        else:
            if __debug__:
                if len(choices) >= 10:
                    raise AssertionError(f'`choice` cannot be added if the {ApplicationCommandOption.__name__} has '
                        f'already `10` choices.')
        
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
        choice_datas = data.get('choices')
        if (choice_datas is None) or (not choice_datas):
            choices = None
        else:
            choices = [ApplicationCommandOptionChoice.from_data(choice_data) for choice_data in choice_datas]
        self.choices = choices
        
        self.default = data.get('default', False)
        self.description = data['description']
        self.name = data['name']
        
        option_datas = data.get('options')
        if (option_datas is None) or (not option_datas):
            options = None
        else:
            options = [ApplicationCommandOption.from_data(option_data) for option_data in option_datas]
        self.options = options
        
        self.required = data.get('required', False)
        
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
        
        return data
    
    def __repr__(self):
        """Returns the application command option's representation."""
        result = [
            '<', self.__class__.__name__,
            ', name=', repr(self.name),
            ', description=', repr(self.description),
            ', type=',
                ]
        
        type_ = self.type
        result.append(repr(type_.value))
        result.append(' (')
        result.append(type_.name)
        result.append(')')
        
        if self.default:
            result.append(', default=True')
        
        if self.required:
            result.append(', required=True')
        
        choices = self.choices
        if (choices is not None):
            result.append(', choices=[')
            
            index = 0
            limit = len(choices)
            
            while True:
                choice = choices[index]
                index += 1
                result.append(repr(choice))
                
                if index == limit:
                    break
                
                result.append(', ')
                continue
        
        options = self.options
        if (options is not None):
            result.append(', options=[')
            
            index = 0
            limit = len(options)
            
            while True:
                option = options[index]
                index += 1
                result.append(repr(option))
                
                if index == limit:
                    break
                
                result.append(', ')
                continue
            
            result.append(']')
        
        result.append('>')
        
        return ''.join(result)
    
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
        new.name = self.description
        
        options = self.options
        if (options is not None):
            options = [option.copy() for option in options]
        new.options = options
        
        new.required = self.required
        new.type = self.type
    
    def __eq__(self, other):
        """Returns whether the two options are equal."""
        if not isinstance(other, ApplicationCommandOption):
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
        
        return True


class ApplicationCommandOptionChoice(object):
    """
    A choice of a ``ApplicationCommandOption``.
    
    Attributes
    ----------
    name : `str`
        The choice's name. It's length can be in range [1:100].
    value : `str` or `int`
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
        value : `str` or `int`
            The choice's value.
        
        Raises
        ------
        AssertionError
            - If `name` is not `str` instance.
            - If `name`'s length is out of range [1:100].
            - If `value` is neither `str` nor `int` instance.
        """
        if __debug__:
            if not isinstance(name, str):
                raise AssertionError(f'`name` can be given as `str` instance, got {name.__class__.__name__}.')
            
            name_ln = len(name)
            if name_ln < 1 or name_ln > 100:
                raise AssertionError(f'`name` length can be in range [1:100], got {name_ln!r}; {name!r}.')
            
            if not isinstance(value, (str, int)):
                raise AssertionError(f'`value` type can be either `str` or `int`, got {value.__class__.__name__}.')
        
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
            The received application command option choice data
        
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
            'name' : self.name,
            'value' : self.value,
                }
    
    def __repr__(self):
        """Returns the application command option choice's representation."""
        return f'<{self.__class__.__name__} name={self.name!r}, value={self.value!r}>'
    
    def __eq__(self, other):
        """Returns whether the two choices are equal."""
        if not isinstance(other, ApplicationCommandOptionChoice):
            return NotImplemented
        
        if self.name != other.name:
            return False
        
        if self.value != other.value:
            return False
        
        return True

@modulize
class InteractionResponseTypes:
    """
    Contains the interaction response type's, which are the following:
    
    +-----------------------+-------+
    | Respective name       | Value |
    +=======================+=======+
    | none                  | 0     |
    +-----------------------+-------+
    | pong                  | 1     |
    +-----------------------+-------+
    | acknowledge           | 2     |
    +-----------------------+-------+
    | message               | 3     |
    +-----------------------+-------+
    | message_and_source    | 4     |
    +-----------------------+-------+
    | source                | 5     |
    +-----------------------+-------+
    """
    none = 0
    pong = 1
    acknowledge = 2
    message = 3
    message_and_source = 4
    source = 5


class ApplicationCommandInteraction(DiscordEntity):
    """
    Represents an ``ApplicationCommand`` invoked by a user.
    
    Attributes
    ----------
    id : int`
        The represented application command's identifier number.
    name : `str`
        The name of the command. It's length can be in range [1:32].
    options : `None` or `list` of ApplicationCommandInteractionOption
        The parameters and values from the user if any. Defaults to `None` if non is received.
    """
    __slots__ = ('id', 'name', 'options')
    def __init__(self, data):
        """
        Creates a new ``ApplicationCommandInteraction`` from the data received from Discord.
        
        Parameters
        ----------
        data : `dict of (`str`, `Any`) items
            The received application command interaction data.
        """
        self.id = int(data['id'])
        self.name = data['name']
        
        option_datas = data.get('options')
        if (option_datas is None) or (not option_datas):
            options = None
        else:
            options = [ApplicationCommandInteractionOption(option_data) for option_data in option_datas]
        self.options = options
    
    def __repr__(self):
        """Returns the application command interaction's representation."""
        result = [
            '<', self.__class__.__name__,
            ' id=', repr(self.id),
            ', name=', repr(self.name),
                ]
        
        options = self.options
        if (options is not None):
            result.append(', options=[')
            
            index = 0
            limit = len(options)
            
            while True:
                option = options[index]
                index += 1
                result.append(repr(option))
                
                if index == limit:
                    break
                
                result.append(', ')
                continue
            
            result.append(']')
        
        result.append('>')
        
        return ''.join(result)

class ApplicationCommandInteractionOption(object):
    """
    Represents an option of a ``ApplicationCommandInteraction``.
    
    Attributes
    ----------
    name : `str`
        The option's name.
    options : `None` or `list` of ApplicationCommandInteractionOption
        The parameters and values from the user. Present if a sub-command was used. Defaults to `None` if non is
        received.
        
        Mutually exclusive with the `value` attribute.
    value : `None`, `str`
        The given value by the user. Should be always converted to the expected type.
    """
    __slots__ = ('name', 'options', 'value')
    def __init__(self, data):
        """
        Creates a new ``ApplicationCommandInteractionOption`` instance from the data received from Discord.
        
        Attributes
        ----------
        data : `dict` of (`str`, `Any`) items
            The received application command interaction option data.
        """
        self.name = data['name']
        
        option_datas = data.get('options')
        if (option_datas is None) or (not option_datas):
            options = None
        else:
            options = [ApplicationCommandInteractionOption(option_data) for option_data in option_datas]
        self.options = options
        
        value = data.get('value')
        if value is not None:
            value = str(value)
        
        self.value = value
    
    def __repr__(self):
        """Returns the application command interaction option's representation."""
        result = [
            '<', self.__class__.__name__,
            ', name=', repr(self.name),
                ]
        
        options = self.options
        if (options is not None):
            result.append(', options=[')
            
            index = 0
            limit = len(options)
            
            while True:
                option = options[index]
                index += 1
                result.append(repr(option))
                
                if index == limit:
                    break
                
                result.append(', ')
                continue
            
            result.append(']')
        
        value = self.value
        if (value is not None):
            result.append(', value=')
            result.append(repr(value))
        
        result.append('>')
        
        return ''.join(result)

del DiscordEntity
del modulize
