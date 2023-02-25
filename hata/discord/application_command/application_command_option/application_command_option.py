__all__ = ('ApplicationCommandOption',)

import warnings

from scarletio import RichAttributeErrorBaseType, export

from ...localization.helpers import get_localized_length
from ...localization.utils import hash_locale_dictionary

from ..application_command_option_choice import ApplicationCommandOptionChoice
from ..helpers import with_translation

from .constants import (
    APPLICATION_COMMAND_OPTION_CHOICES_MAX, APPLICATION_COMMAND_OPTION_MAX_LENGTH_DEFAULT,
    APPLICATION_COMMAND_OPTION_MIN_LENGTH_DEFAULT, APPLICATION_COMMAND_OPTION_OPTIONS_MAX
)
from .fields import (
    parse_autocomplete, parse_channel_types, parse_choices, parse_default, parse_description,
    parse_description_localizations, parse_max_length, parse_max_value, parse_min_length, parse_min_value, parse_name,
    parse_name_localizations, parse_options, parse_required, parse_type, put_autocomplete_into, put_channel_types_into,
    put_choices_into, put_default_into, put_description_into, put_description_localizations_into, put_max_length_into,
    put_max_value_into, put_min_length_into, put_min_value_into, put_name_into, put_name_localizations_into,
    put_options_into, put_required_into, put_type_into, validate_autocomplete, validate_channel_types, validate_choices,
    validate_default, validate_description, validate_description_localizations, validate_max_length, validate_max_value,
    validate_min_length, validate_min_value, validate_name, validate_name_localizations, validate_options,
    validate_required, validate_type
)
from .preinstanced import ApplicationCommandOptionType


@export
class ApplicationCommandOption(RichAttributeErrorBaseType):
    """
    An option of an ``ApplicationCommand``.
    
    Attributes
    ----------
    autocomplete : `bool`
        Whether the option supports auto completion.
        
        Mutually exclusive with the ``.choices``. Only applicable for string type parameters.
    
    channel_types : `None`, `tuple` of ``ChannelType``
        The accepted channel types by the option.
        
        Only applicable if ``.type`` is set to `ApplicationCommandOptionType.channel`.
    
    choices : `None`, `tuple` of ``ApplicationCommandOptionChoice``
        Choices for `str` and `int` types for the user to pick from.
        
        Mutually exclusive with the ``.autocomplete``.
    
    default : `bool`
        Whether the option is the default one. Only one option can be `default`.
    
    description : `None`, `str`
        The description of the application command option. It's length can be in range [1:100].
    
    description_localizations : `None`, `dict` of (``Locale``, `str`) items
        Localized descriptions of the option.
    
    max_length : `int`
        The maximum input length allowed for this option.
        
        Only applicable for string options.
    
    max_value : `None`, `int`, `float`
        The maximal value permitted for this option.
        
        Only applicable for integer as `int`, and for float options as `float`.
    
    min_length : `int`
        The minimum input length allowed for this option.
        
        Only applicable for string options.
    
    min_value : `None`, `int`, `float`
        The minimum value permitted for this option.
        
        Only applicable for integer as `int`, and for float options as `float`.
    
    name : `str`
        The name of the application command option. It's length can be in range [1:32].
    
    name_localizations : `None`, `dict` of (``Locale``, `str`) items
        Localized names of the option.
    
    options : `None`, `tuple` of ``ApplicationCommandOption``
        If the command's type is sub-command group type, then this nested option will be the parameters of the
        sub-command. It's length can be in range [0:25]. If would be set as empty list, instead is set as `None`.
    
    required : `bool`
        Whether the parameter is required. Defaults to `False`.
    
    type : ``ApplicationCommandOptionType``
        The option's type.
    """
    __slots__ = (
        'autocomplete', 'channel_types', 'choices', 'default', 'description', 'description_localizations',
        'max_length', 'max_value', 'min_length', 'min_value', 'name', 'name_localizations', 'options', 'required',
        'type'
    )
    
    def __new__(
        cls,
        name,
        description,
        option_type,
        *,
        autocomplete = ...,
        channel_types = ...,
        choices = ...,
        default = ...,
        description_localizations = ...,
        max_length = ...,
        max_value = ...,
        min_length = ...,
        min_value = ...,
        name_localizations = ...,
        options = ...,
        required = ...,
    ):
        """
        Creates a new application command option with the given parameters.
        
        Parameters
        ----------
        name : `str`
            The name of the command. It's length can be in range [1:32].
        
        description : `None`, `str`
            The command's description. It's length can be in range [2:100].
        
        option_type : `int`, ``ApplicationCommandOptionType``
            The application command option's type.
        
        autocomplete : `bool`, Optional (Keyword only)
            Whether the option supports auto completion.
            
            Mutually exclusive with the `choices` parameter. Only applicable for string type parameters.
        
        channel_types : `None`, `iterable` of (``ChannelType``, `int`), Optional (Keyword only)
            The accepted channel types by the option.
            
            Only applicable if ``.type`` is set to `ApplicationCommandOptionType.channel`.
        
        choices : `None`, `iterable` of ``ApplicationCommandOptionChoice``, Optional (Keyword only)
            The choices of the command for string or integer types. It's length can be in range [0:25].
            
            Mutually exclusive with the `autocomplete` parameter.
        
        default : `bool` = `False`, Optional (Keyword only)
            Whether the option is the default one.
        
        description_localizations : `None`, `dict` of ((`str`, ``Locale``), `str`) items,
                (`list`, `set`, `tuple`) of `tuple` ((`str`, ``Locale``), `str`), Optional (Keyword only)
            Localized descriptions of the option.
            
        max_length : `None`, `int`, Optional (Keyword only)
            The maximum input length allowed for this option.
            
            Only applicable for string options.
        
        max_value : `None`, `int`, `float`, Optional (Keyword only)
            The maximal value permitted for this option.
            
            Only applicable for integer as `int`, and for float options as `float`.
        
        min_length : `None`, `int`, Optional (Keyword only)
            The minimum input length allowed for this option.
            
            Only applicable for string options.
            
        min_value : `None`, `int`, `float`, Optional (Keyword only)
            The minimum value permitted for this option.
            
            Only applicable for integer as `int`, and for float options as `float`.
        
        name_localizations : `None`, `dict` of ((`str`, ``Locale``), `str`) items,
                (`list`, `set`, `tuple`) of `tuple` ((`str`, ``Locale``), `str`), Optional (Keyword only)
            Localized names of the option.
        
        options : `None`, `iterable` of ``ApplicationCommandOption``, Optional (Keyword only)
            The parameters or sub-commands of the command option. It's length can be in range [0:25].
        
        required : `bool`, Optional (Keyword only)
            Whether the parameter is required.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
            - if a parameter is not applicable for the given option.
        """
        # option_type
        option_type = validate_type(option_type)
        
        # autocomplete
        if autocomplete is ...:
            autocomplete = False
        else:
            autocomplete = validate_autocomplete(autocomplete, option_type)
        
        # channel_types
        if channel_types is ...:
            channel_types = None
        else:
            channel_types = validate_channel_types(channel_types, option_type)
        
        # choices
        if choices is ...:
            choices = None
        else:
            choices = validate_choices(choices, option_type)
        
        # default
        if default is ...:
            default = False
        else:
            default = validate_default(default, option_type)
        
        # description
        description = validate_description(description)
        
        # description_localizations
        if description_localizations is ...:
            description_localizations = None
        else:
            description_localizations = validate_description_localizations(description_localizations)
        
        # max_length
        if max_length is ...:
            max_length = APPLICATION_COMMAND_OPTION_MAX_LENGTH_DEFAULT
        else:
            max_length = validate_max_length(max_length, option_type)
        
        # max_value
        if max_value is ...:
            max_value = None
        else:
            max_value = validate_max_value(max_value, option_type)
        
        # min_length
        if min_length is ...:
            min_length = APPLICATION_COMMAND_OPTION_MIN_LENGTH_DEFAULT
        else:
            min_length = validate_min_length(min_length, option_type)
        
        # min_value
        if min_value is ...:
            min_value = None
        else:
            min_value = validate_min_value(min_value, option_type)
        
        # name
        name = validate_name(name)
        
        # name_localizations
        if name_localizations is ...:
            name_localizations = None
        else:
            name_localizations = validate_name_localizations(name_localizations)
        
        # options
        if options is ...:
            options = None
        else:
            options = validate_options(options)
        
        # required
        if required is ...:
            required = False
        else:
            required = validate_required(required)
        
        # Construct
        self = object.__new__(cls)
        self.autocomplete = autocomplete
        self.channel_types = channel_types
        self.choices = choices
        self.default = default
        self.description = description
        self.description_localizations = description_localizations
        self.max_length = max_length
        self.max_value = max_value
        self.min_length = min_length
        self.min_value = min_value
        self.name = name
        self.name_localizations = name_localizations
        self.options = options
        self.required = required
        self.type = option_type
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new application command option from the received data from Discord.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Received application command option data.
        
        Returns
        -------
        self : `instance<type<cls>>`
            The created application command option.
        """
        self = object.__new__(cls)
        self.autocomplete = parse_autocomplete(data)
        self.channel_types = parse_channel_types(data)
        self.choices = parse_choices(data)
        self.default = parse_default(data)
        self.description = parse_description(data)
        self.description_localizations = parse_description_localizations(data)
        self.max_length = parse_max_length(data)
        self.max_value = parse_max_value(data)
        self.min_length = parse_min_length(data)
        self.min_value = parse_min_value(data)
        self.name = parse_name(data)
        self.name_localizations = parse_name_localizations(data)
        self.options = parse_options(data)
        self.required = parse_required(data)
        self.type = parse_type(data)
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the application command option to a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether fields with their default value should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        data = {}
        
        put_autocomplete_into(self.autocomplete, data, defaults)
        put_channel_types_into(self.channel_types, data, defaults)
        put_choices_into(self.choices, data, defaults)
        put_default_into(self.default, data, defaults)
        put_description_into(self.description, data, defaults)
        put_description_localizations_into(self.description_localizations, data, defaults)
        put_max_length_into(self.max_length, data, defaults)
        put_max_value_into(self.max_value, data, defaults)
        put_min_length_into(self.min_length, data, defaults)
        put_min_value_into(self.min_value, data, defaults)
        put_name_into(self.name, data, defaults)
        put_name_localizations_into(self.name_localizations, data, defaults)
        put_options_into(self.options, data, defaults)
        put_required_into(self.required, data, defaults)
        put_type_into(self.type, data, defaults)
        return data
    
    
    def __repr__(self):
        """Returns the application command option's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        # Descriptive fields `.name`, `.description`, `.type`
        
        # name
        repr_parts.append(' name = ')
        repr_parts.append(repr(self.name))
        
        # description
        repr_parts.append(', description = ')
        repr_parts.append(repr(self.description))
        
        # type
        repr_parts.append(', type = ')
        option_type = self.type
        repr_parts.append(option_type.name)
        repr_parts.append(' ~ ')
        repr_parts.append(repr(option_type.value))
        
        # Extra fields: `.autocomplete`, `.min_value`, `.max_value`, `.default`, `.required`, `.choices`, `.options`
        #    `.name_localizations`, `.description_localizations`, `.min_length`, `.max_length`
        
        # autocomplete
        if self.autocomplete:
            repr_parts.append(', autocomplete = True')
        
        # default
        if self.default:
            repr_parts.append(', default = True')
        
        # required
        if self.required:
            repr_parts.append(', required=True')
        
        if option_type is ApplicationCommandOptionType.string:
            # min_length
            min_length = self.min_length
            if (min_length != 0):
                repr_parts.append(', min_length = ')
                repr_parts.append(repr(min_length))
            
            # max_length
            max_length = self.max_length
            if (max_length != 0):
                repr_parts.append(', max_length = ')
                repr_parts.append(repr(max_length))
        
        
        if option_type is ApplicationCommandOptionType.integer or option_type is ApplicationCommandOptionType.float:
            # min_value
            min_value = self.min_value
            if (min_value is not None):
                repr_parts.append(', min_value = ')
                repr_parts.append(repr(min_value))
            
            # max_value
            max_value = self.max_value
            if (max_value is not None):
                repr_parts.append(', max_value = ')
                repr_parts.append(repr(max_value))
        
        # channel_types
        channel_types = self.channel_types
        if (channel_types is not None):
            repr_parts.append(', channel_types = [')
            
            index = 0
            limit = len(channel_types)
            
            while True:
                channel_type = channel_types[index]
                index += 1
                repr_parts.append(channel_type.name)
                repr_parts.append(' ~ ')
                repr_parts.append(repr(channel_type.value))
                
                if index == limit:
                    break
                
                repr_parts.append(', ')
                continue
            
            repr_parts.append(']')
        
        # choices
        choices = self.choices
        if (choices is not None):
            repr_parts.append(', choices = [')
            
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
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
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
        
        # max_length
        if self.max_length != other.max_length:
            return False
        
        # max_value
        if self.max_value != other.max_value:
            return False
        
        # min_length
        if self.min_value != other.min_value:
            return False
        
        # min_value
        if self.min_value != other.min_value:
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
    
    
    def __hash__(self):
        """Returns the hash value of the application command option."""
        hash_value = 0
        
        # autocomplete
        hash_value ^= self.autocomplete
        
        # channel_types
        channel_types = self.channel_types
        if (channel_types is not None):
            hash_value ^= hash(channel_types)
        
        # choices
        choices = self.choices
        if (choices is not None):
            hash_value ^= len(choices) << 1
            
            for choice in choices:
                hash_value ^= hash(choice)
        
        # default
        hash_value ^= self.default << 5
        
        # description
        # Do not hash `.description` if equals to `.name`.
        description = self.description
        if (description != self.name):
            hash_value ^= hash(description)
        
        # description_localizations
        # Do not hash `.description_localizations` if equals to `.name_localizations`.
        description_localizations = self.description_localizations
        if (description_localizations is not None) and (description_localizations != self.name_localizations):
            hash_value ^= hash_locale_dictionary(description_localizations)
        
        # max_length
        hash_value ^= self.max_length << 9
        
        # max_value
        hash_value ^= hash(self.max_value)
        
        # min_length
        hash_value ^= self.min_length << 13
        
        # min_value
        hash_value ^= hash(self.min_value)
        
        # name
        hash_value ^= hash(self.name)
        
        # name_localizations
        name_localizations = self.name_localizations
        if (name_localizations is not None):
            hash_value ^= hash_locale_dictionary(name_localizations)
        
        # options
        options = self.options
        if (options is not None):
            hash_value ^= len(options) << 1
            
            for option in options:
                hash_value ^= hash(option)
        
        # required
        hash_value ^= self.required << 17
        
        # type
        hash_value ^= self.type.value << 18
        
        return hash_value
    
    
    
    def add_option(self, option):
        """
        Adds a new option to the application command option.
        
        Parameters
        ----------
        option : ``ApplicationCommandOption``
            The option to add.
        
        Returns
        -------
        self : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If the source application command's type is not a sub-command group type.
            - If `option` is not ``ApplicationCommandOption``.
            - If `option` is a sub command group option.
        """
        warnings.warn(
            f'`{self.__class__.__name__}.add_option` is deprecated and will be removed in 2023 Jul.',
            FutureWarning,
            stacklevel = 2,
        )
    
        if self.type is not ApplicationCommandOptionType.sub_command_group:
            raise TypeError(
                f'`option` can be added only if the command option\s type is sub command option, '
                f'got option = {option!r}, self = {self!r}.'
            )
        
        if not isinstance(option, ApplicationCommandOption):
            raise TypeError(
                f'`option` can be `{ApplicationCommandOption.__name__}`, got '
                f'{option.__class__.__name__}; {option!r}.'
            )
    
        if option.type is ApplicationCommandOptionType.sub_command_group:
            raise TypeError(
                f'`option`\'s type is sub-command group option, but sub-command groups cannot be '
                f'added under sub-command groups; got {option!r}; self = {self!r}.'
            )
        
        self.options = (*self.iter_options(), option)[:APPLICATION_COMMAND_OPTION_OPTIONS_MAX]
        
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
        self : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If the source application command's type is not a string, int nor float group type.
            - If the `choice`'s value's type is not the expected one by the command option's type.
            - If `choice`'s type is neither ``ApplicationCommandOptionChoice`` nor a `tuple` representing it's `.name`
                and `.value`.
        """
        warnings.warn(
            f'`{self.__class__.__name__}.add_option` is deprecated and will be removed in 2023 Jul.',
            FutureWarning,
            stacklevel = 2,
        )
        
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
                f'choice = {choice!r}, self = {self!r}.'
            )
        
        self.choices = (*self.iter_choices(), choice)[:APPLICATION_COMMAND_OPTION_CHOICES_MAX]
        return self
    
    
    def apply_translation(self, translation_table, replace = False):
        """
        Applies translation from the given nested dictionary to the application command option.
        
        Parameters
        ----------
        translation_table : `None`, `dict` of ((``Locale``, `str`),
                (`None`, `dict` (`str`, (`None`, `str`)) items)) items
            Translation table to pull localization. from.
        replace : `bool` = `False`, Optional
            Whether actual translation should be replaced.
        """
        warnings.warn(
            (
                f'`{self.__class__.__name__}.apply_translation` is deprecated and will be removed in 2023 Jul. '
                f'Please use `.with_translation` instead.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        
        if translation_table is None:
            return
        
        # choices
        choices = self.choices
        if (choices is not None):
            for choice in choices:
                choice.apply_translation(translation_table, replace)
        
        # description
        self.description_localizations = with_translation(
            self.description,
            self.description_localizations,
            translation_table,
            replace,
        )
        
        # name
        self.name_localizations = with_translation(
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
    
    
    def with_translation(self, translation_table, replace = False):
        """
        Returns a new application command option with the given translation table applied.
        
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
        
        new = object.__new__(type(self))
        
        # autocomplete
        new.autocomplete = self.autocomplete
        
        # channel_types
        channel_types = self.channel_types
        if (channel_types is not None):
            channel_types = (*channel_types,)
        new.channel_types = channel_types
        
        # choices
        choices = self.choices
        if (choices is not None):
            choices = (*(choice.with_translation(translation_table, replace) for choice in choices),)
        new.choices = choices
        
        # default
        new.default = self.default
        
        # description
        new.description = self.description
        
        # description_localizations
        new.description_localizations = with_translation(
            self.description,
            self.description_localizations,
            translation_table,
            replace,
        )
        
        # max_length
        new.max_length = self.max_length
        
        # max_value
        new.max_value = self.max_value
        
        # min_length
        new.min_length = self.min_length
        
        # min_value
        new.min_value = self.min_value
        
        # name
        new.name = self.name
        
        # name_localizations
        new.name_localizations = with_translation(
            self.name,
            self.name_localizations,
            translation_table,
            replace,
        )
        
        # options
        options = self.options
        if (options is not None):
            options = (*(option.with_translation(translation_table, replace) for option in options),)
        new.options = options
        
        # required
        new.required = self.required
        
        # type
        new.type = self.type
        
        return new
    
    
    def copy(self):
        """
        Copies the application command option.
        
        Returns
        -------
        new : `instance<type<cls>>`
        """
        new = object.__new__(type(self))
        
        # autocomplete
        new.autocomplete = self.autocomplete
        
        # channel_types
        channel_types = self.channel_types
        if (channel_types is not None):
            channel_types = (*channel_types,)
        new.channel_types = channel_types
        
        # choices
        choices = self.choices
        if (choices is not None):
            choices = (*(choice.copy() for choice in choices),)
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
        
        # max_length
        new.max_length = self.max_length
        
        # max_value
        new.max_value = self.max_value
        
        # min_length
        new.min_length = self.min_length
        
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
            options = (*(option.copy() for option in options),)
        new.options = options
        
        # required
        new.required = self.required
        
        # type
        new.type = self.type
        
        return new
    

    def copy_with(
        self,
        *,
        autocomplete = ...,
        channel_types = ...,
        choices = ...,
        default = ...,
        description = ...,
        description_localizations = ...,
        max_length = ...,
        max_value = ...,
        min_length = ...,
        min_value = ...,
        name = ...,
        name_localizations = ...,
        option_type = ...,
        options = ...,
        required = ...,
    ):
        """
        Copies the application command option wit the given fields.
        
        Parameters
        ----------
        autocomplete : `bool`, Optional (Keyword only)
            Whether the option supports auto completion.
            
            Mutually exclusive with the `choices` parameter. Only applicable for string type parameters.
        
        channel_types : `None`, `iterable` of (``ChannelType``, `int`), Optional (Keyword only)
            The accepted channel types by the option.
            
            Only applicable if ``.type`` is set to `ApplicationCommandOptionType.channel`.
        
        choices : `None`, `iterable` of ``ApplicationCommandOptionChoice``, Optional (Keyword only)
            The choices of the command for string or integer types. It's length can be in range [0:25].
            
            Mutually exclusive with the `autocomplete` parameter.
        
        default : `bool` = `False`, Optional (Keyword only)
            Whether the option is the default one.
        
        description : `None`, `str`, Optional (Keyword only)
            The command's description. It's length can be in range [2:100].
        
        description_localizations : `None`, `dict` of ((`str`, ``Locale``), `str`) items,
                (`list`, `set`, `tuple`) of `tuple` ((`str`, ``Locale``), `str`), Optional (Keyword only)
            Localized descriptions of the option.
            
        max_length : `None`, `int`, Optional (Keyword only)
            The maximum input length allowed for this option.
            
            Only applicable for string options.
        
        max_value : `None`, `int`, `float`, Optional (Keyword only)
            The maximal value permitted for this option.
            
            Only applicable for integer as `int`, and for float options as `float`.
        
        min_length : `None`, `int`, Optional (Keyword only)
            The minimum input length allowed for this option.
            
            Only applicable for string options.
            
        min_value : `None`, `int`, `float`, Optional (Keyword only)
            The minimum value permitted for this option.
            
            Only applicable for integer as `int`, and for float options as `float`.
        
        name : `str`, Optional (Keyword only)
            The name of the command. It's length can be in range [1:32].
        
        name_localizations : `None`, `dict` of ((`str`, ``Locale``), `str`) items,
                (`list`, `set`, `tuple`) of `tuple` ((`str`, ``Locale``), `str`), Optional (Keyword only)
            Localized names of the option.
        
        option_type : `int`, ``ApplicationCommandOptionType``, Optional (Keyword only)
            The application command option's type.
        
        options : `None`, `iterable` of ``ApplicationCommandOption``, Optional (Keyword only)
            The parameters or sub-commands of the command option. It's length can be in range [0:25].
        
        required : `bool`, Optional (Keyword only)
            Whether the parameter is required.
        
        Returns
        -------
        new : `instance<type<cls>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
            - if a parameter is not applicable for the given option.
        """
        # option_type
        if (option_type is ...):
            option_type = self.type
        else:
            option_type = validate_type(option_type)
        
        # autocomplete
        if autocomplete is ...:
            autocomplete = self.autocomplete
        else:
            autocomplete = validate_autocomplete(autocomplete, option_type)
        
        # channel_types
        if channel_types is ...:
            channel_types = self.channel_types
            if (channel_types is not None):
                channel_types = (*channel_types,)
        else:
            channel_types = validate_channel_types(channel_types, option_type)
        
        # choices
        if choices is ...:
            choices = self.choices
            if (choices is not None):
                choices = (*(choice.copy() for choice in choices),)
        else:
            choices = validate_choices(choices, option_type)
        
        # default
        if default is ...:
            default = self.default
        else:
            default = validate_default(default, option_type)
        
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
        
        # max_length
        if max_length is ...:
            max_length = self.max_length
        else:
            max_length = validate_max_length(max_length, option_type)
        
        # max_value
        if max_value is ...:
            max_value = self.max_value
        else:
            max_value = validate_max_value(max_value, option_type)
        
        # min_length
        if min_length is ...:
            min_length = self.min_length
        else:
            min_length = validate_min_length(min_length, option_type)
        
        # min_value
        if min_value is ...:
            min_value = self.min_value
        else:
            min_value = validate_min_value(min_value, option_type)
        
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
        
        # options
        if options is ...:
            options = self.options
            if (options is not None):
                options = (*(option.copy() for option in options),)
        else:
            options = validate_options(options)
        
        # required
        if required is ...:
            required = self.required
        else:
            required = validate_required(required)
        
        
        # Construct
        new = object.__new__(type(self))
        new.autocomplete = autocomplete
        new.channel_types = channel_types
        new.choices = choices
        new.default = default
        new.description = description
        new.description_localizations = description_localizations
        new.max_length = max_length
        new.max_value = max_value
        new.min_length = min_length
        new.min_value = min_value
        new.name = name
        new.name_localizations = name_localizations
        new.options = options
        new.required = required
        new.type = option_type
        return new
    
    
    def iter_choices(self):
        """
        Iterates over the choices of the application command option.
        
        This method is an iterable generator.
        
        Yields
        ------
        choice : ``ApplicationCommandOptionChoice``
        """
        choices = self.choices
        if (choices is not None):
            yield from choices
    
    
    def iter_options(self):
        """
        Iterates over the options of the application command option.
        
        This method is an iterable generator.
        
        Yields
        ------
        choice : ``ApplicationCommandOption``
        """
        options = self.options
        if (options is not None):
            yield from options
