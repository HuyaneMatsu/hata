__all__ = ('ApplicationCommandOption',)

import warnings

from scarletio import RichAttributeErrorBaseType, copy_docs, export

from ...localization.helpers import get_localized_length
from ...localization.utils import hash_locale_dictionary

from ..application_command_option_choice import ApplicationCommandOptionChoice
from ..application_command_option_metadata import ApplicationCommandOptionMetadataBase
from ..application_command_option_metadata.constants import (
    APPLICATION_COMMAND_OPTION_CHOICES_MAX, APPLICATION_COMMAND_OPTION_OPTIONS_MAX
)
from ..helpers import with_translation

from .fields import (
    parse_description, parse_description_localizations, parse_name, parse_name_localizations, parse_type,
    put_description_into, put_description_localizations_into, put_name_into, put_name_localizations_into, put_type_into,
    validate_description, validate_description_localizations, validate_name, validate_name_localizations, validate_type
)
from .helpers import _purge_defaults_and_maybe_raise
from .preinstanced import ApplicationCommandOptionType


@export
class ApplicationCommandOption(RichAttributeErrorBaseType):
    """
    An option of an ``ApplicationCommand``.
    
    Attributes
    ----------
    description : `None`, `str`
        The description of the application command option. It's length can be in range [1:100].
    
    description_localizations : `None`, `dict` of (``Locale``, `str`) items
        Localized descriptions of the option.
    
    metadata : ``ApplicationCommandOptionMetadataBase``
        Metadata containing the type specific fields of the option.
    
    name : `str`
        The name of the application command option. It's length can be in range [1:32].
    
    name_localizations : `None`, `dict` of (``Locale``, `str`) items
        Localized names of the option.
    
    type : ``ApplicationCommandOptionType``
        The option's type.
    """
    __slots__ = ('description', 'description_localizations', 'metadata', 'name', 'name_localizations', 'type')
    
    def __new__(
        cls,
        name,
        description,
        option_type,
        *,
        description_localizations = ...,
        name_localizations = ...,
        **keyword_parameters,
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
        
        description_localizations : `None`, `dict` of ((`str`, ``Locale``), `str`) items,
                (`list`, `set`, `tuple`) of `tuple` ((`str`, ``Locale``), `str`), Optional (Keyword only)
            Localized descriptions of the option.
        
        name_localizations : `None`, `dict` of ((`str`, ``Locale``), `str`) items,
                (`list`, `set`, `tuple`) of `tuple` ((`str`, ``Locale``), `str`), Optional (Keyword only)
            Localized names of the option.
        
        **keyword_parameters : Keyword parameters
            Additional option type specific parameters.
        
        Other Parameters
        ----------------
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
        
        options : `None`, `iterable` of ``ApplicationCommandOption``, Optional (Keyword only)
            The parameters or sub-commands of the command option. It's length can be in range [0:25].
        
        required : `bool`, Optional (Keyword only)
            Whether the parameter is required.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
            - Extra parameters given.
        ValueError
            - If a parameter's value is incorrect.
            - if a parameter is not applicable for the given option.
        """
        # option_type
        option_type = validate_type(option_type)
        
        # description
        description = validate_description(description)
        
        # description_localizations
        if description_localizations is ...:
            description_localizations = None
        else:
            description_localizations = validate_description_localizations(description_localizations)
        
        # name
        name = validate_name(name)
        
        # name_localizations
        if name_localizations is ...:
            name_localizations = None
        else:
            name_localizations = validate_name_localizations(name_localizations)
        
        metadata = option_type.metadata_type.from_keyword_parameters(keyword_parameters)
        _purge_defaults_and_maybe_raise(keyword_parameters)
        
        # Construct
        self = object.__new__(cls)
        self.description = description
        self.description_localizations = description_localizations
        self.metadata = metadata
        self.name = name
        self.name_localizations = name_localizations
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
        option_type = parse_type(data)
        metadata = option_type.metadata_type.from_data(data)
        
        self = object.__new__(cls)
        self.description = parse_description(data)
        self.description_localizations = parse_description_localizations(data)
        self.metadata = metadata
        self.name = parse_name(data)
        self.name_localizations = parse_name_localizations(data)
        self.type = option_type
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
        data = self.metadata.to_data(defaults = defaults)
        put_description_into(self.description, data, defaults)
        put_description_localizations_into(self.description_localizations, data, defaults)
        put_name_into(self.name, data, defaults)
        put_name_localizations_into(self.name_localizations, data, defaults)
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
            repr_parts.append(', required = True')
        
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
        
        # description
        if self.description != other.description:
            return False
        
        # description_localizations
        if self.description_localizations != other.description_localizations:
            return False
        
        # metadata
        if self.metadata != other.metadata:
            return False
        
        # name
        if self.name != other.name:
            return False
        
        # name_localizations
        if self.name_localizations != other.name_localizations:
            return False
        
        # type
        if self.type is not other.type:
            return False
        
        return True
    
    
    def __len__(self):
        """Returns the application command option's length."""
        length = 0
        
        # choices
        for choice in self.iter_choices():
            length += len(choice)
        
        # description & description_localizations
        length += get_localized_length(self.description, self.description_localizations)
        
        # name & name_localizations
        length += get_localized_length(self.name, self.name_localizations)
        
        # options
        for option in self.iter_options():
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
        
        new = self.copy()
        
        # choices
        choices = new.choices
        if (choices is not None):
            new.choices = (*(choice.with_translation(translation_table, replace) for choice in choices),)
        
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
    
    
    def copy(self):
        """
        Copies the application command option.
        
        Returns
        -------
        new : `instance<type<cls>>`
        """
        new = object.__new__(type(self))
        
        # description
        new.description = self.description
        
        # description_localizations
        description_localizations = self.description_localizations
        if (description_localizations is not None):
            description_localizations = description_localizations.copy()
        new.description_localizations = description_localizations
        
        # metadata
        new.metadata = self.metadata.copy()
        
        # name
        new.name = self.name
        
        # name_localizations
        name_localizations = self.name_localizations
        if (name_localizations is not None):
            name_localizations = name_localizations.copy()
        new.name_localizations = name_localizations
        
        # type
        new.type = self.type
        
        return new
    

    def copy_with(
        self,
        *,
        description = ...,
        description_localizations = ...,
        name = ...,
        name_localizations = ...,
        option_type = ...,
        **keyword_parameters,
    ):
        """
        Copies the application command option wit the given fields.
        
        Parameters
        ----------
        description : `None`, `str`, Optional (Keyword only)
            The command's description. It's length can be in range [2:100].
        
        description_localizations : `None`, `dict` of ((`str`, ``Locale``), `str`) items,
                (`list`, `set`, `tuple`) of `tuple` ((`str`, ``Locale``), `str`), Optional (Keyword only)
            Localized descriptions of the option.
            
        name : `str`, Optional (Keyword only)
            The name of the command. It's length can be in range [1:32].
        
        name_localizations : `None`, `dict` of ((`str`, ``Locale``), `str`) items,
                (`list`, `set`, `tuple`) of `tuple` ((`str`, ``Locale``), `str`), Optional (Keyword only)
            Localized names of the option.
        
        option_type : `int`, ``ApplicationCommandOptionType``, Optional (Keyword only)
            The application command option's type.
        
        **keyword_parameters : Keyword parameters
            Additional option type specific parameters.
        
        Other Parameters
        ----------------
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
            - Extra parameters given.
        ValueError
            - If a parameter's value is incorrect.
            - if a parameter is not applicable for the given option.
        """
        # option_type
        if (option_type is ...):
            option_type = self.type
        else:
            option_type = validate_type(option_type)
        
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
        
        # metadata
        metadata = self.metadata
        metadata_type = option_type.metadata_type
        if metadata_type is type(metadata):
            metadata = metadata.copy_with_keyword_parameters(keyword_parameters)
        else:
            metadata = metadata_type.from_keyword_parameters(keyword_parameters)
        _purge_defaults_and_maybe_raise(keyword_parameters)
        
        
        # Construct
        new = object.__new__(type(self))
        new.description = description
        new.description_localizations = description_localizations
        new.metadata = metadata
        new.name = name
        new.name_localizations = name_localizations
        new.type = option_type
        return new
    
    # Field proxies
    
    # autocomplete
    @property
    @copy_docs(ApplicationCommandOptionMetadataBase.autocomplete)
    def autocomplete(self):
        return self.metadata.autocomplete
    
    @autocomplete.setter
    def autocomplete(self, autocomplete):
        self.metadata.autocomplete = autocomplete
    
    # channel_types
    @property
    @copy_docs(ApplicationCommandOptionMetadataBase.channel_types)
    def channel_types(self):
        return self.metadata.channel_types
    
    @channel_types.setter
    def channel_types(self, channel_types):
        self.metadata.channel_types = channel_types
    
    # choices
    @property
    @copy_docs(ApplicationCommandOptionMetadataBase.choices)
    def choices(self):
        return self.metadata.choices
    
    @choices.setter
    def choices(self, choices):
        self.metadata.choices = choices
    
    # default
    @property
    @copy_docs(ApplicationCommandOptionMetadataBase.default)
    def default(self):
        return self.metadata.default
    
    @default.setter
    def default(self, default):
        self.metadata.default = default
    
    # max_length
    @property
    @copy_docs(ApplicationCommandOptionMetadataBase.max_length)
    def max_length(self):
        return self.metadata.max_length
    
    @max_length.setter
    def max_length(self, max_length):
        self.metadata.max_length = max_length
    
    # max_value
    @property
    @copy_docs(ApplicationCommandOptionMetadataBase.max_value)
    def max_value(self):
        return self.metadata.max_value
    
    @max_value.setter
    def max_value(self, max_value):
        self.metadata.max_value = max_value
    
    # min_length
    @property
    @copy_docs(ApplicationCommandOptionMetadataBase.min_length)
    def min_length(self):
        return self.metadata.min_length
    
    @min_length.setter
    def min_length(self, min_length):
        self.metadata.min_length = min_length
    
    # min_value
    @property
    @copy_docs(ApplicationCommandOptionMetadataBase.min_value)
    def min_value(self):
        return self.metadata.min_value
    
    @min_value.setter
    def min_value(self, min_value):
        self.metadata.min_value = min_value
    
    # options
    @property
    @copy_docs(ApplicationCommandOptionMetadataBase.options)
    def options(self):
        return self.metadata.options
    
    @options.setter
    def options(self, options):
        self.metadata.options = options
    
    # required
    @property
    @copy_docs(ApplicationCommandOptionMetadataBase.required)
    def required(self):
        return self.metadata.required
    
    @required.setter
    def required(self, required):
        self.metadata.required = required
    
    # Iterators
    
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
        option : ``ApplicationCommandOption``
        """
        options = self.options
        if (options is not None):
            yield from options
    
