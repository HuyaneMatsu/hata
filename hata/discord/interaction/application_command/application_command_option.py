__all__ = ('ApplicationCommandOption',)

from scarletio import RichAttributeErrorBaseType

from ...localizations.helpers import localized_dictionary_builder
from ...localizations.utils import build_locale_dictionary, destroy_locale_dictionary
from ...preconverters import preconvert_preinstanced_type

from .application_command_option_choice import ApplicationCommandOptionChoice
from .constants import (
    APPLICATION_COMMAND_CHOICES_MAX, APPLICATION_COMMAND_DESCRIPTION_LENGTH_MAX,
    APPLICATION_COMMAND_DESCRIPTION_LENGTH_MIN, APPLICATION_COMMAND_NAME_LENGTH_MAX,
    APPLICATION_COMMAND_NAME_LENGTH_MIN, APPLICATION_COMMAND_OPTIONS_MAX
)
from .helpers import apply_translation_into
from .preinstanced import ApplicationCommandOptionType


class ApplicationCommandOption(RichAttributeErrorBaseType):
    """
    An option of an ``ApplicationCommand``.
    
    Attributes
    ----------
    autocomplete : `bool`
        Whether the option supports auto completion.
        
        Mutually exclusive with the ``.choices``. Only applicable for string type parameters.
    
    channel_types : `None`, `tuple` of `int`
        The accepted channel types by the option.
        
        Only applicable if ``.type`` is set to `ApplicationCommandOptionType.channel`.
    
    choices : `None`, `list` of ``ApplicationCommandOptionChoice``
        Choices for `str` and `int` types for the user to pick from.
        
        Mutually exclusive with the ``.autocomplete``.
    
    default : `bool`
        Whether the option is the default one. Only one option can be `default`.
    
    description : `str`
        The description of the application command option. It's length can be in range [1:100].
    
    description_localizations : `None`, `dict` of (``Locale``, `str`) items
        Localized descriptions of the option.
    
    max_value : `None`, `int`, `float`
        The maximal value permitted for this option.
        
        Only Applicable for integer as `int`, `as float options as `float`.
    
    min_value : `None`, `int`, `float`
        The minimum value permitted for this option.
        
        Only Applicable for integer as `int`, `as float options as `float`.
    
    name : `str`
        The name of the application command option. It's length can be in range [1:32].
    
    name_localizations : `None`, `dict` of (``Locale``, `str`) items
        Localized names of the option.
    
    options : `None`, `list` of ``ApplicationCommandOption``
        If the command's type is sub-command group type, then this nested option will be the parameters of the
        sub-command. It's length can be in range [0:25]. If would be set as empty list, instead is set as `None`.
    
    required : `bool`
        Whether the parameter is required. Defaults to `False`.
    
    type : ``ApplicationCommandOptionType``
        The option's type.
    """
    __slots__ = (
        'autocomplete', 'channel_types', 'choices', 'default', 'description', 'description_localizations', 'max_value',
        'min_value', 'name', 'name_localizations', 'options', 'required', 'type'
    )
    
    def __new__(cls, name, description, type_, *, autocomplete=False, channel_types=None, choices=None, default=False,
            description_localizations=None, max_value=None, min_value=None, name_localizations=None, options=None,
            required=False):
        """
        Creates a new ``ApplicationCommandOption`` with the given parameters.
        
        Parameters
        ----------
        name : `str`
            The name of the command. It's length can be in range [1:32].
        
        description : `str`
            The command's description. It's length can be in range [2:100].
        
        type_ : `int`, ``ApplicationCommandOptionType``
            The application command option's type.
        
        autocomplete : `bool` = `False`, Optional (Keyword only)
            Whether the option supports auto completion.
            
            Mutually exclusive with the `choices` parameter. Only applicable for string type parameters.
        
        channel_types : `None`, `iterable` of `int` = `None`, Optional (Keyword only)
            The accepted channel types by the option.
            
            Only applicable if ``.type`` is set to `ApplicationCommandOptionType.channel`.
        
        choices : `None`, (`list`, `tuple`) of ``ApplicationCommandOptionChoice`` = `None`, Optional (Keyword only)
            The choices of the command for string or integer types. It's length can be in range [0:25].
            
            Mutually exclusive with the `autocomplete` parameter.
        
        default : `bool` = `False`, Optional (Keyword only)
            Whether the option is the default one.
        
        description_localizations : `None`, `dict` of ((`str`, ``Locale``), `str`) items,
                (`list`, `set`, `tuple`) of `tuple` ((`str`, ``Locale``), `str`) = `None`, Optional (Keyword only)
            Localized descriptions of the option.
        
        max_value : `None`, `int`, `float` = `None`, Optional (Keyword only)
            The maximal value permitted for this option.
            
            Only Applicable for integer as `int`, as float options as `float`.
        
        min_value : `None`, `int`, `float` = `None`, Optional (Keyword only)
            The minimum value permitted for this option.
            
            Only Applicable for integer as `int`, as float options as `float`.
        
        name_localizations : `None`, `dict` of ((`str`, ``Locale``), `str`) items,
                (`list`, `set`, `tuple`) of `tuple` ((`str`, ``Locale``), `str`) = `None`, Optional (Keyword only)
            Localized names of the option.
        
        options : `None`, (`list`, `tuple`) of ``ApplicationCommandOption`` = `None`, Optional (Keyword only)
            The parameters of the command. It's length can be in range [0:25]. Only applicable for sub command groups.
        
        required : `bool` = `False`, Optional (Keyword only)
            Whether the parameter is required.
        
        Raises
        ------
        TypeError
            - If `type_` was not given neither as `int` nor ``ApplicationCommandOptionType``.
            - If `choices` was given meanwhile `type_` is neither string nor integer option type.
            - If `options` was given meanwhile `type_` is not a sub-command group option type.
            - If a choice's value's type not matched the expected type described `type_`.
            - If `channel_types` is neither `None` nor `iterable` of `int`.
            - If `max_value` is not the expected type defined by `type_`'s value.
            - If `min_value` is not the expected type defined by `type_`'s value.
            - If `name_localizations`'s or any of it's item's type is incorrect.
            - If `description_localizations`'s or any of it's item's type is incorrect.
        ValueError
            - If `type_` was given as `int`, but it do not matches any of the precreated
                ``ApplicationCommandOptionType``-s.
            - If `channel_types` contains an unknown channel type value.
            - If `max_value` is given, but it is not applicable for the given `type_`.
            - If `min_value` is given, but it is not applicable for the given `type_`.
            - If `name_localizations` has an item with incorrect structure.
            - If `description_localizations` has an item with incorrect structure.
        AssertionError
            - If `name` was not given as `str`.
            - If `name` length is out of range [1:32].
            - If `description` was not given as `str`.
            - If `description` length is out of range [1:100].
            - If `options` was not given neither as `None` nor as (`list`, `tuple`) of ``ApplicationCommandOption``
                instances.
            - If `options`'s length is out of range [0:25].
            - If `default` was not given as `bool`.
            - If `required` was not given as `bool`.
            - If `choices` was not given neither as `None` nor as (`list`, `tuple`) of
                ``ApplicationCommandOptionChoice``s.
            - If `choices`'s length is out of range [0:25].
            - If an option is a sub command group option.
            - If `channel_types` is given, but `type_` is not `ApplicationCommandOptionType.channel`.
            - If `autocomplete` is not `bool`.
            - If both `autocomplete` and `choices` are defined.
            - If `autocomplete` is defined, but the parameters's type is not string.
        """
        
        # autocomplete
        if __debug__:
            if not isinstance(autocomplete, bool):
                raise AssertionError(
                    f'`autocomplete` can be `bool`, got {autocomplete.__class__.__name__}; {autocomplete!r}.'
                )
        
        # channel_types
        if (channel_types is None):
            channel_types_processed = None
        else:
            channel_types_processed = None
            
            iterator = getattr(type(channel_types), '__iter__', None)
            if (iterator is None):
                raise TypeError(
                    f'`channel_types` can be `None`, `iterable`, got '
                    f'{channel_types.__class__.__anme__}; {channel_types!r}.'
                )
            
            for channel_type in iterator(channel_types):
                if type(channel_type) is int:
                    pass
                elif isinstance(channel_type, int):
                    channel_type = int(channel_type)
                else:
                    raise TypeError(
                        f'`channel_types` may include only `int`s, got {channel_type.__class__.__name__}; '
                        f'{channel_type!r}; channel_types={channel_types!r}.'
                    )
                
                if channel_types_processed is None:
                    channel_types_processed = set()
                
                channel_types_processed.add(channel_type)
        
            if channel_types_processed:
                channel_types_processed = tuple(sorted(channel_types_processed))
            else:
                channel_types_processed = None
        
        # choices
        if choices is None:
            choices_processed = None
        else:
            if __debug__:
                if not isinstance(choices, (tuple, list)):
                    raise AssertionError(
                        f'`choices` can be `None`, (`list`, `tuple`) of '
                        f'`{ApplicationCommandOptionChoice.__name__}`, got {choices.__class__.__name__}; {choices!r}.'
                    )
            
            choices_processed = list(choices)
            
            if __debug__:
                if len(choices_processed) > APPLICATION_COMMAND_CHOICES_MAX:
                    raise AssertionError(
                        f'`choices` length can be in range '
                        f'[0:{APPLICATION_COMMAND_CHOICES_MAX}], got {len(choices_processed)!r}; {choices!r}'
                    )
                
                for index, choice in enumerate(choices_processed):
                    if not isinstance(choice, ApplicationCommandOptionChoice):
                        raise AssertionError(
                            f'`choices[{index}]` is not `{ApplicationCommandOptionChoice.__name__}`, got '
                            f'{choice.__class__.__name__}; {choice!r}; choices={choices!r}.'
                        )
            
            if not choices_processed:
                choices_processed = None
        
        # default
        if __debug__:
            if not isinstance(default, bool):
                raise AssertionError(
                    f'`default` can be `bool`, got {default.__class__.__name__}; {default!r}.'
                )
        
        # description
        if __debug__:
            if not isinstance(description, str):
                raise AssertionError(
                    f'`description` can be `str`, got {description.__class__.__name__}; {description!r}.'
                )
            
            description_length = len(description)
            if (
                description_length < APPLICATION_COMMAND_DESCRIPTION_LENGTH_MIN or
                description_length > APPLICATION_COMMAND_DESCRIPTION_LENGTH_MAX
            ):
                raise AssertionError(
                    f'`description` length can be in range '
                    f'[{APPLICATION_COMMAND_DESCRIPTION_LENGTH_MIN}:{APPLICATION_COMMAND_DESCRIPTION_LENGTH_MAX}], '
                    f'got {description_length!r}; {description!r}.'
                )
        
        # description_localizations
        description_localizations = localized_dictionary_builder(description_localizations, 'description_localizations')
        
        # max_value
        # requires `type`
        
        # min_value
        # requires `type`
        
        
        # name
        if __debug__:
            if not isinstance(name, str):
                raise AssertionError(
                    f'`name` can be `str`, got {name.__class__.__name__}; {name!r}.'
                )
            
            name_length = len(name)
            if (
                name_length < APPLICATION_COMMAND_NAME_LENGTH_MIN or
                name_length > APPLICATION_COMMAND_NAME_LENGTH_MAX
            ):
                raise AssertionError(
                    f'`name` length can be in range '
                    f'[{APPLICATION_COMMAND_NAME_LENGTH_MIN}:{APPLICATION_COMMAND_NAME_LENGTH_MAX}], got '
                    f'{name_length!r}; {name!r}.'
                )
        
        # name_localizations
        name_localizations = localized_dictionary_builder(name_localizations, 'name_localizations')
        
        # options

        if options is None:
            options_processed = None
        else:
            if __debug__:
                if not isinstance(options, (tuple, list)):
                    raise AssertionError(
                        f'`options` can be `None`, (`list`, `tuple`) of `{ApplicationCommandOption.__name__}`, got '
                        f'{options.__class__.__name__}; {options!r}.'
                    )
            
            # Copy it
            options_processed = list(options)
            
            if __debug__:
                if len(options_processed) > APPLICATION_COMMAND_OPTIONS_MAX:
                    raise AssertionError(
                        f'`options` length can be in range '
                        f'[0:{APPLICATION_COMMAND_OPTIONS_MAX}], got {len(options_processed)!r}; {options!r}.'
                    )
                
                for index, option in enumerate(options_processed):
                    if not isinstance(option, ApplicationCommandOption):
                        raise AssertionError(
                            f'`options[{index}]` is not `{ApplicationCommandOption.__name__}`, got '
                            f'{option.__class__.__name__}; {options!r}; options={options}.'
                        )
                    
                    if option.type is ApplicationCommandOptionType.sub_command_group:
                        raise AssertionError(
                            f'`options[{index!r}]` element\'s type is cub-command group option, but'
                            f'sub-command groups cannot be added under sub-command groups; got '
                            f'{option!r}; options={options!r}.'
                        )
            
            if not options_processed:
                options_processed = None
        

        # required
        if __debug__:
            if not isinstance(required, bool):
                raise AssertionError(
                    f'`required` can be `bool`, got {required.__class__.__name__}; {required!r}.'
                )
        
        # type
        type_ = preconvert_preinstanced_type(type_, 'type_', ApplicationCommandOptionType)
        
        # Postprocessing
        
        # max_value
        if (max_value is not None):
            if type_ is ApplicationCommandOptionType.integer:
                if not isinstance(max_value, int):
                    raise TypeError(
                        f'`max_value` can be `int`, if `type_` is defined as {type_!r}, got '
                        f'{max_value.__class__.__name__}; {max_value!r}.'
                    )
            
            elif type_ is ApplicationCommandOptionType.float:
                if not isinstance(max_value, float):
                    raise TypeError(
                        f'`max_value` can be `float`, if `type_` is defined as {type_!r}, got '
                        f'{max_value.__class__.__name__}; {max_value!r}.'
                    )
            
            else:
                raise ValueError(
                    f'`max_value` is only meaningful if `type` is either '
                    f'{ApplicationCommandOptionType.integer!r}, or {ApplicationCommandOptionType.float!r}, got '
                    f'type_={type_!r}; max_value={max_value!r}.'
                )
        
        # min_value
        if (min_value is not None):
            if type_ is ApplicationCommandOptionType.integer:
                if not isinstance(min_value, int):
                    raise TypeError(
                        f'`min_value` can be `int` type, if `type_` is defined as {type_!r}, got '
                        f'{min_value.__class__.__name__}; {min_value!r}.'
                    )
            
            elif type_ is ApplicationCommandOptionType.float:
                if not isinstance(min_value, float):
                    raise TypeError(
                        f'`min_value` can be `float` type, if `type_` is defined as {type_!r}, got '
                        f'{min_value.__class__.__name__}; {min_value!r}.'
                    )
            
            else:
                raise ValueError(
                    f'`min_value` is only meaningful if `type` is either '
                    f'{ApplicationCommandOptionType.integer!r}, or {ApplicationCommandOptionType.float!r}, got '
                    f'type_={type_!r}; min_value={min_value!r}.'
                )
        
        # postprocessing | autocomplete
        if __debug__:
            if autocomplete:
                if (choices_processed is not None):
                    raise AssertionError(
                        f'`autocomplete` and `choices` parameters are mutually exclusive, got '
                        f'autocomplete={autocomplete!r}; choices={choices_processed!r}.'
                    )
                
                if (type_ is not ApplicationCommandOptionType.string):
                    raise AssertionError(
                        f'`autocomplete` is only available for string option type, got type={type_!r}.'
                    )
        
        # postprocessing | choices
        if (choices_processed is not None):
            if type_ is ApplicationCommandOptionType.string:
                expected_choice_type = str
            elif type_ is ApplicationCommandOptionType.integer:
                expected_choice_type = int
            elif type_ is ApplicationCommandOptionType.float:
                expected_choice_type = float
            else:
                raise TypeError(
                    f'`choices` can be bound either to string, integer or float option types, got '
                    f'choices={choices!r}, type={type_!r}.'
                )
            
            for index, choice in enumerate(choices):
                if not isinstance(choice.value, expected_choice_type):
                    raise TypeError(
                        f'`choices[{index!r}]` is not `{expected_choice_type.__name__}` as expected from the received'
                        f'command option type, got {choice.__class__.__name__}; {choice!r}; type_={type_!r}; '
                        f'choices={choices!r}.'
                    )
        
        # postprocessing | channel_types
        if __debug__:
            if (channel_types_processed is not None) and (type_ is not ApplicationCommandOptionType.channel):
                raise AssertionError(
                    f'`channel_types` is only meaningful if `type_` is '
                    f'`{ApplicationCommandOptionType.__name__}.channel`, got '
                    f'type_={type_!r}; channel_types={channel_types_processed!r}.'
                )
        
        
        self = object.__new__(cls)
        
        self.autocomplete = autocomplete
        self.channel_types = channel_types_processed
        self.choices = choices_processed
        self.default = default
        self.description = description
        self.description_localizations = description_localizations
        self.max_value = max_value
        self.min_value = min_value
        self.name = name
        self.name_localizations = name_localizations
        self.options = options_processed
        self.required = required
        self.type = type_
        
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
            - If `option` is not ``ApplicationCommandOption``.
            - If the ``ApplicationCommandOption`` has already `25` options.
            - If `option` is a sub command group option.
        """
        if self.type is not ApplicationCommandOptionType.sub_command_group:
            raise TypeError(
                f'`option` can be added only if the command option\s type is sub command option, '
                f'got option={option!r}, self={self!r}.'
            )
        
        if __debug__:
            if not isinstance(option, ApplicationCommandOption):
                raise AssertionError(
                    f'`option` can be `{ApplicationCommandOption.__name__}`, got '
                    f'{option.__class__.__name__}; {option!r}.'
                )
        
            if option.type is ApplicationCommandOptionType.sub_command_group:
                raise AssertionError(
                    f'`option`\'s type is sub-command group option, but sub-command groups cannot be '
                    f'added under sub-command groups; got {option!r}; self={self!r}.'
                )
        
        options = self.options
        if options is None:
            self.options = options = []
        else:
            if __debug__:
                if len(options) >= APPLICATION_COMMAND_OPTIONS_MAX:
                    raise AssertionError(
                        f'`option` cannot be added if the `{ApplicationCommandOption.__name__}` has '
                        f'already `{APPLICATION_COMMAND_OPTIONS_MAX}` options, got {option!r}.'
                    )
        
        options.append(option)
        return self
    
    
    def add_choice(self, choice):
        """
        Adds a ``ApplicationCommandOptionChoice`` to the application command option.
        
        Parameters
        ----------
        choice : ``ApplicationCommandOptionChoice``, `tuple` (`str`, (`str`, `int`, `float`))
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
                raise TypeError(
                    f'`choice` `tuple`\'s length should be `2` representing a '
                    f'`{ApplicationCommandOptionChoice.__name__}`\'s `.name` and `.value`, got {choice!r}.'
                )
            
            choice = ApplicationCommandOptionChoice(*choice)
        else:
            raise TypeError(
                f'`choice` can be `{ApplicationCommandOptionChoice.__name__}`, '
                f'`tuple` (`str`, (`str`, `int`, `float`)), got '
                f'{choice.__class__.__name__}; {choice!r}.'
            )
        
        type_ = self.type
        if type_ is ApplicationCommandOptionType.string:
            expected_choice_type = str
        elif type_ is ApplicationCommandOptionType.integer:
            expected_choice_type = int
        elif type_ is ApplicationCommandOptionType.float:
            expected_choice_type = float
        else:
            raise TypeError(
                f'`choice` is bound to string, integer and float application option types, '
                f'got choice={choice!r}, self={self!r}.'
            )
        
        if not isinstance(choice.value, expected_choice_type):
            raise TypeError(
                f'`choice` value\'s type is not `{expected_choice_type.__name__}` as expected, got '
                f'choice={choice!r}, self={self!r}.'
            )
        
        choices = self.choices
        if choices is None:
            self.choices = choices = []
        else:
            if __debug__:
                if len(choices) >= APPLICATION_COMMAND_CHOICES_MAX:
                    raise AssertionError(
                        f'`choice` cannot be added if the {ApplicationCommandOption.__name__} has '
                        f'already `{APPLICATION_COMMAND_CHOICES_MAX}` choices.'
                    )
        
        choices.append(choice)
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new ``ApplicationCommandOption`` from the received data from Discord.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received application command option data.
        
        Returns
        -------
        self : ``ApplicationCommandOption``
            The created application command option.
        """
        # autocomplete
        autocomplete = data.get('autocomplete', False)
        
        # channel_types
        channel_types = data.get('channel_types', None)
        if (channel_types is None) or (not channel_types):
            channel_types = None
        else:
            channel_types = tuple(sorted(channel_types))
        
        # choices
        choice_datas = data.get('choices', None)
        if (choice_datas is None) or (not choice_datas):
            choices = None
        else:
            choices = [ApplicationCommandOptionChoice.from_data(choice_data) for choice_data in choice_datas]
        
        # default
        default = data.get('default', False)
        
        # description
        description = data['description']
        
        # description_localizations
        description_localizations = build_locale_dictionary(data.get('description_localizations', None))
        
        # max_value
        max_value = data.get('max_value', None)
        
        # min_value
        min_value = data.get('min_value', None)
        
        # name
        name = data['name']
        
        # name_localizations
        name_localizations = build_locale_dictionary(data.get('name_localizations', None))
        
        # options
        option_datas = data.get('options', None)
        if (option_datas is None) or (not option_datas):
            options = None
        else:
            options = [ApplicationCommandOption.from_data(option_data) for option_data in option_datas]
        
        # required
        required = data.get('required', False)
        
        # type
        type_ = ApplicationCommandOptionType.get(data['type'])
        
        
        self = object.__new__(cls)
        
        self.autocomplete = autocomplete
        self.channel_types = channel_types
        self.choices = choices
        self.default = default
        self.description = description
        self.description_localizations = description_localizations
        self.max_value = max_value
        self.min_value = min_value
        self.name = name
        self.name_localizations = name_localizations
        self.options = options
        self.required = required
        self.type = type_
        
        return self
    
    
    def to_data(self):
        """
        Converts the application command option to a json serializable object.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        data = {}
        
        # autocomplete
        if self.autocomplete:
            data['autocomplete'] = True
        
        # channel_types
        channel_types = self.channel_types
        if (channel_types is not None):
            data['channel_types'] = channel_types
        
        # choices
        choices = self.choices
        if (choices is not None):
            data['choices'] = [choice.to_data() for choice in choices]
        
        # default
        if self.default:
            data['default'] = True
        
        # description
        data['description'] = self.description
        
        # description_localizations
        data['description_localizations'] = destroy_locale_dictionary(self.description_localizations)
        
        # max_value
        max_value = self.max_value
        if (max_value is not None):
            data['max_value'] = max_value
        
        # min_value
        min_value = self.min_value
        if (min_value is not None):
            data['min_value'] = min_value
        
        # name
        data['name'] = self.name
        
        # name_localizations
        data['name_localizations'] = destroy_locale_dictionary(self.name_localizations)
        
        # options
        options = self.options
        if (options is not None):
            data['options'] = [option.to_data() for option in options]
        
        # required
        if self.required:
            data['required'] = True
        
        # type
        data['type'] = self.type.value
        
        return data
    
    
    def __repr__(self):
        """Returns the application command option's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        # Descriptive fields `.name`, `.description`, `.type`
        
        # name
        repr_parts.append(' name=')
        repr_parts.append(repr(self.name))
        
        # description
        repr_parts.append(', description=')
        repr_parts.append(repr(self.description))
        
        # type
        repr_parts.append(', type=')
        type_ = self.type
        repr_parts.append(repr(type_.value))
        repr_parts.append(' (')
        repr_parts.append(type_.name)
        repr_parts.append(')')
        
        # Extra fields: `.autocomplete`, `.min_value`, `.max_value`, `.default`, `.required`, `.choices`, `.options`
        #    `.name_localizations`, `.description_localizations`
        
        # autocomplete
        if self.autocomplete:
            repr_parts.append(', autocomplete=True')
        
        # default
        if self.default:
            repr_parts.append(', default=True')
        
        # required
        if self.required:
            repr_parts.append(', required=True')
        
        # min_value
        min_value = self.min_value
        if (min_value is not None):
            repr_parts.append(', min_value=')
            repr_parts.append(repr(min_value))
        
        # max_value
        max_value = self.max_value
        if (max_value is not None):
            repr_parts.append(', max_value=')
            repr_parts.append(repr(max_value))
        
        # channel_types
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
        
        # choices
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
        
        # options
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
        
        # name_localizations
        name_localizations = self.name_localizations
        if (name_localizations is not None):
            repr_parts.append(', name_localizations=')
            repr_parts.append(repr(name_localizations))
        
        # description_localizations
        description_localizations = self.description_localizations
        if (description_localizations is not None):
            repr_parts.append(', description_localizations=')
            repr_parts.append(repr(description_localizations))
        
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
        
        # autocomplete
        new.autocomplete = self.autocomplete
        
        # channel_types
        channel_types = self.channel_types
        if (channel_types is not None):
            channel_types = tuple(channel_types)
        new.channel_types = channel_types
        
        # choices
        choices = self.choices
        if (choices is not None):
            choices = [choice.copy() for choice in choices]
        new.choices = choices
        
        # default
        new.default = self.default
        
        # description
        new.description = self.description
        
        # description_localizations
        description_localizations = self.description_localizations
        if (description_localizations is not None):
            description_localizations = description_localizations.copy()
        new.description_localizations = description_localizations
        
        # max_value
        new.max_value = self.max_value
        
        # min_value
        new.min_value = self.min_value
        
        # name
        new.name = self.name
        
        # name_localizations
        name_localizations = self.name_localizations
        if (name_localizations is not None):
            name_localizations = name_localizations.copy()
        new.name_localizations = name_localizations
        
        # options
        options = self.options
        if (options is not None):
            options = [option.copy() for option in options]
        new.options = options
        
        # required
        new.required = self.required
        
        # type
        new.type = self.type
        
        return new
    
    
    def __eq__(self, other):
        """Returns whether the two options are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # autocomplete
        if self.autocomplete != other.autocomplete:
            return False
        
        # channel_types
        if self.channel_types != other.channel_types:
            return False
        
        # choices
        if self.choices != other.choices:
            return False
        
        # default
        if self.default != other.default:
            return False
        
        # description
        if self.description != other.description:
            return False
        
        # description_localizations
        if self.description_localizations != other.description_localizations:
            return False
        
        # min_value
        if self.min_value != other.min_value:
            return False
        
        # max_value
        if self.max_value != other.max_value:
            return False
        
        # name
        if self.name != other.name:
            return False
        
        # name_localizations
        if self.name_localizations != other.name_localizations:
            return False
        
        # options
        if self.options != other.options:
            return False
        
        # required
        if self.required != other.required:
            return False
        
        # type
        if self.type is not other.type:
            return False
        
        return True
    
    
    def __len__(self):
        """Returns the application command option's length."""
        length = 0
        
        # choices
        choices = self.choices
        if (choices is not None):
            for choice in choices:
                length += len(choice)
        
        # description
        length += len(self.description)
        
        # description_localizations
        description_localizations = self.description_localizations
        if (description_localizations is not None):
            for value in description_localizations.values():
                length += len(value)
        
        # name
        length += len(self.name)
        
        # name_localizations
        name_localizations = self.name_localizations
        if (name_localizations is not None):
            for value in name_localizations.values():
                length += len(value)
        
        # options
        options = self.options
        if (options is not None):
            for option in options:
                length += len(option)
        
        return length
    
    
    def apply_translation(self, translation_table, replace=False):
        """
        Applies translation from the given nested dictionary to the application command option.
        
        Parameters
        ----------
        translation_table : `None`, `dict` of ((``Locale``, `str`),
                (`None`, `dict` (`str`, (`None`, `str`)) items)) items
            Translation table to pull localizations from.
        replace : `bool` = `False`, Optional
            Whether actual translation should be replaced.
        """
        if translation_table is None:
            return
        
        # choices
        choices = self.choices
        if (choices is not None):
            for choice in choices:
                choice.apply_translation(translation_table, replace)
        
        # description
        self.description_localizations = apply_translation_into(
            self.description,
            self.description_localizations,
            translation_table,
            replace,
        )
        
        # name
        self.name_localizations = apply_translation_into(
            self.name,
            self.name_localizations,
            translation_table,
            replace,
        )
        
        # options
        options = self.options
        if (options is not None):
            for option in options:
                option.apply_translation(translation_table, replace)
