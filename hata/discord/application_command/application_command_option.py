__all__ = ('ApplicationCommandOption',)

from scarletio import RichAttributeErrorBaseType

from ..channel import ChannelType
from ..localization.helpers import get_localized_length, localized_dictionary_builder
from ..localization.utils import build_locale_dictionary, destroy_locale_dictionary, hash_locale_dictionary
from ..preconverters import preconvert_preinstanced_type

from .application_command_option_choice import ApplicationCommandOptionChoice
from .constants import (
    APPLICATION_COMMAND_CHOICES_MAX, APPLICATION_COMMAND_DESCRIPTION_LENGTH_MAX,
    APPLICATION_COMMAND_DESCRIPTION_LENGTH_MIN, APPLICATION_COMMAND_NAME_LENGTH_MAX,
    APPLICATION_COMMAND_NAME_LENGTH_MIN, APPLICATION_COMMAND_OPTIONS_MAX, APPLICATION_COMMAND_OPTION_MAX_LENGTH_MAX,
    APPLICATION_COMMAND_OPTION_MAX_LENGTH_MIN, APPLICATION_COMMAND_OPTION_MIN_LENGTH_MAX,
    APPLICATION_COMMAND_OPTION_MIN_LENGTH_MIN
)
from .helpers import apply_translation_into
from .preinstanced import ApplicationCommandOptionType


def _validate_max_length(max_length, type_):
    """
    Validates the given ``ApplicationCommandOption`` option's `max_length` value.
    
    Parameters
    ----------
    max_length : `None`, `int`
        The maximum input length allowed for this option.
        
        Only applicable for string options.
    
    type_ : ``ApplicationCommandOptionType``
        Respective application command option type.
    
    Returns
    -------
    max_length : `int`
    
    Raises
    ------
    TypeError
        - If `max_length`'s type is incorrect.
    ValueError
        - If `max_length` is not applicable for the given type.
    """
    if (max_length is None):
        return 0
    
    if not isinstance(max_length, int):
        raise TypeError(
            f'`max_length` can be `None`, `int`, got {max_length.__class__.__name__}; {max_length!r}.'
        )
        
    if max_length == 0:
        return 0
    
    if type_ is not ApplicationCommandOptionType.string:
        raise ValueError(
            f'`max_length` is only meaningful if `type` is {ApplicationCommandOptionType.string!r}, got '
            f'type_={type_!r}; max_length = {max_length!r}.'
        )
    
    if max_length < APPLICATION_COMMAND_OPTION_MAX_LENGTH_MIN:
        max_length = APPLICATION_COMMAND_OPTION_MAX_LENGTH_MIN
    
    elif max_length >= APPLICATION_COMMAND_OPTION_MAX_LENGTH_MAX:
        max_length = 0

    return max_length


def _validate_min_length(min_length, type_):
    """
    Validates the given ``ApplicationCommandOption`` option's `min_length` value.
    
    Parameters
    ----------
    min_length : `None`, `int`
        The minimum input length allowed for this option.
        
        Only applicable for string options.
    
    type_ : ``ApplicationCommandOptionType``
        Respective application command option type.
    
    Returns
    -------
    min_length : `int`
    
    Raises
    ------
    TypeError
        - If `min_length`'s type is incorrect.
    ValueError
        - If `min_length` is not applicable for the given type.
    """
    if (min_length is None):
        return 0
    
    if not isinstance(min_length, int):
        raise TypeError(
            f'`min_length` can be `None`, `int`, got {min_length.__class__.__name__}; {min_length!r}.'
        )
        
    if min_length == 0:
        return 0
    
    if type_ is not ApplicationCommandOptionType.string:
        raise ValueError(
            f'`min_length` is only meaningful if `type` is {ApplicationCommandOptionType.string!r}, got '
            f'type_={type_!r}; {min_length!r}.'
        )
    
    if min_length < APPLICATION_COMMAND_OPTION_MIN_LENGTH_MIN:
        min_length = APPLICATION_COMMAND_OPTION_MIN_LENGTH_MIN
    
    elif min_length > APPLICATION_COMMAND_OPTION_MIN_LENGTH_MAX:
        min_length = APPLICATION_COMMAND_OPTION_MIN_LENGTH_MAX

    return min_length


def _assert__application_command_option__autocomplete(autocomplete):
    """
    Asserts the `autocomplete` parameter of ``ApplicationCommandOption.__new__`` method.
    
    Parameters
    ----------
    autocomplete : `bool`
        Whether the application command option is autocompleted.
    
    Raises
    ------
    AssertionError
        - If `autocomplete` is not `bool`.
    """
    if not isinstance(autocomplete, bool):
        raise AssertionError(
            f'`autocomplete` can be `bool`, got {autocomplete.__class__.__name__}; {autocomplete!r}.'
        )
    
    return True


def _assert__application_command_option__default(default):
    """
    Asserts the `default` parameter of ``ApplicationCommandOption.__new__`` method.
    
    Parameters
    ----------
    default : `bool`
        Whether the application command option is the default one in it's group.
    
    Raises
    ------
    AssertionError
        - If `default` is not `bool`.
    """
    if not isinstance(default, bool):
        raise AssertionError(
            f'`default` can be `bool`, got {default.__class__.__name__}; {default!r}.'
        )
    
    return True


def _assert__application_command_option__description(description):
    """
    Asserts the `description` parameter of ``ApplicationCommandOption.__new__`` method.
    
    Parameters
    ----------
    description : `str`
        The application command option's description.
    
    Raises
    ------
    AssertionError
        - If `description` is not `str`.
        - if `description`'s length is out of the expected range.
    """
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

    return True


def _assert__application_command_option__name(name):
    """
    Asserts the `name` parameter of ``ApplicationCommandOption.__new__`` method.
    
    Parameters
    ----------
    name : `str`
        The application command option's name.
    
    Raises
    ------
    AssertionError
        - If `name` is not `str`.
        - if `name`'s length is out of the expected range.
    """
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
    
    return True


def _assert__application_command_option__required(required):
    """
    Asserts the `required` parameter of ``ApplicationCommandOption.__new__`` method.
    
    Parameters
    ----------
    required : `bool`
        Whether the application command option is required.
    
    Raises
    ------
    AssertionError
        - If `required` is not `bool`.
    """
    if not isinstance(required, bool):
        raise AssertionError(
            f'`required` can be `bool`, got {required.__class__.__name__}; {required!r}.'
        )
    
    return True


def _assert__application_command_option__autocomplete__applicability(autocomplete, choices, type_):
    """
    Asserts whether the `autocomplete` parameter of the of ``ApplicationCommandOption.__new__`` method
    is applicable for the given `choices` and `type_` combinations.
    
    Parameters
    ----------
    autocomplete : `bool`
        Whether the option supports auto completion.
    choices : `None`, `list` of ``ApplicationCommandOptionChoice``
        The choices of the command for string or integer types.
    type_ : ``ApplicationCommandOptionType``
        The application command option's type.

    Raises
    ------
    AssertionError
        - If both `autocomplete` and `choices` are defined.
        - If `autocomplete` is defined, but the parameters' type is not string.
    """
    if autocomplete:
        if (choices is not None):
            raise AssertionError(
                f'`autocomplete` and `choices` parameters are mutually exclusive, got '
                f'autocomplete={autocomplete!r}; choices={choices!r}.'
            )
        
        if (type_ is not ApplicationCommandOptionType.string):
            raise AssertionError(
                f'`autocomplete` is only available for string option type, got type={type_!r}.'
            )
    
    return True


def _assert__application_command_option__channel_types__applicability(channel_types, type_):
    """
    Asserts whether the `autocomplete` parameter of the of ``ApplicationCommandOption.__new__`` method
    is applicable for the given `choices` and `type_` combinations.
    
    Parameters
    ----------
    channel_types : `None`, `tuple` of `int`
        The accepted channel types by the option.
    type_ : ``ApplicationCommandOptionType``
        The application command option's type.

    Raises
    ------
    AssertionError
        - If `channel_types` is given, but `type_` is not `ApplicationCommandOptionType.channel`.
    """
    if (channel_types is not None) and (type_ is not ApplicationCommandOptionType.channel):
        raise AssertionError(
            f'`channel_types` is only meaningful if `type_` is `{ApplicationCommandOptionType.__name__}.channel`, got '
            f'type_={type_!r}; channel_types = {channel_types!r}.'
        )

    return True


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
    
    choices : `None`, `list` of ``ApplicationCommandOptionChoice``
        Choices for `str` and `int` types for the user to pick from.
        
        Mutually exclusive with the ``.autocomplete``.
    
    default : `bool`
        Whether the option is the default one. Only one option can be `default`.
    
    description : `str`
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
    
    options : `None`, `list` of ``ApplicationCommandOption``
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
        cls, name, description, type_, *, autocomplete=False, channel_types = None, choices=None, default = False,
        description_localizations=None, max_length = None, max_value = None, min_length = None, min_value = None,
        name_localizations=None, options=None, required=False
    ):
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
        
        channel_types : `None`, `iterable` of (``ChannelType``, `int`) = `None`, Optional (Keyword only)
            The accepted channel types by the option.
            
            Only applicable if ``.type`` is set to `ApplicationCommandOptionType.channel`.
        
        choices : `None`, `iterable` of ``ApplicationCommandOptionChoice`` = `None`, Optional (Keyword only)
            The choices of the command for string or integer types. It's length can be in range [0:25].
            
            Mutually exclusive with the `autocomplete` parameter.
        
        default : `bool` = `False`, Optional (Keyword only)
            Whether the option is the default one.
        
        description_localizations : `None`, `dict` of ((`str`, ``Locale``), `str`) items,
                (`list`, `set`, `tuple`) of `tuple` ((`str`, ``Locale``), `str`) = `None`, Optional (Keyword only)
            Localized descriptions of the option.
            
        max_length : `None`, `int` = `None`, Optional (Keyword only)
            The maximum input length allowed for this option.
            
            Only applicable for string options.
        
        max_value : `None`, `int`, `float` = `None`, Optional (Keyword only)
            The maximal value permitted for this option.
            
            Only applicable for integer as `int`, and for float options as `float`.
        
        min_length : `None`, `int` = `None`, Optional (Keyword only)
            The minimum input length allowed for this option.
            
            Only applicable for string options.
            
        min_value : `None`, `int`, `float` = `None`, Optional (Keyword only)
            The minimum value permitted for this option.
            
            Only applicable for integer as `int`, and for float options as `float`.
        
        name_localizations : `None`, `dict` of ((`str`, ``Locale``), `str`) items,
                (`list`, `set`, `tuple`) of `tuple` ((`str`, ``Locale``), `str`) = `None`, Optional (Keyword only)
            Localized names of the option.
        
        options : `None`, `iterable` of ``ApplicationCommandOption`` = `None`, Optional (Keyword only)
            The parameters of the command. It's length can be in range [0:25]. Only applicable for sub command groups.
        
        required : `bool` = `False`, Optional (Keyword only)
            Whether the parameter is required.
        
        Raises
        ------
        TypeError
            - If a parameter's type is unexpected.
            - If `options` was given meanwhile `type_` is not a sub-command group option type.
            - If a choice's value's type not matched the expected type described `type_`.
        ValueError
            - If `type_` was given as `int`, but it do not matches any of the precreated
                ``ApplicationCommandOptionType``-s.
            - If `channel_types` contains an unknown channel type value.
            - If `max_value` or `min_value` is given, but it is not applicable for the given `type_`.
            - If `name_localizations` has an item with incorrect structure.
            - If `description_localizations` has an item with incorrect structure.
            - If `max_length` or `min_length` is given, but it is not applicable for the given `type_`.
        """
        # autocomplete
        assert _assert__application_command_option__autocomplete(autocomplete)
        
        # channel_types
        channel_types_processed = None
        
        if (channel_types is not None):
            channel_types_processed = None
            
            if getattr(type(channel_types), '__iter__', None) is None:
                raise TypeError(
                    f'`channel_types` can be `None`, `iterable`, got '
                    f'{channel_types.__class__.__anme__}; {channel_types!r}.'
                )
            
            for channel_type in channel_types:
                if isinstance(channel_type, ChannelType):
                    pass
                
                elif isinstance(channel_type, ChannelType.VALUE_TYPE):
                    channel_type = ChannelType.get(channel_type)
                
                else:
                    raise TypeError(
                        f'`channel_types` can have `{ChannelType.__name__}`, `int` elements, '
                        f'got {channel_type.__class__.__name__}; {channel_type!r}; channel_types = {channel_types!r}.'
                    )
                
                if channel_types_processed is None:
                    channel_types_processed = set()
                
                channel_types_processed.add(channel_type)
            
            if (channel_types_processed is not None):
                channel_types_processed = tuple(sorted(channel_types_processed))
        
        
        # choices
        choices_processed = None
        
        if (choices is not None):
            if (getattr(choices, '__iter__', None) is None):
                raise TypeError(
                    f'`choices` can be `iterable of `{ApplicationCommandOptionChoice.__name__}`, '
                    f'got {choices.__class__.__name__}; {choices!r}.'
                )
            
            for choice in choices:
                if not isinstance(choice, ApplicationCommandOptionChoice):
                    raise TypeError(
                        f'`choices` can contain `{ApplicationCommandOptionChoice.__name__}` elements, got '
                        f'{choice.__class__.__name__}; {choice!r}; choices={choices!r}.'
                    )
                
                if choices_processed is None:
                    choices_processed = []
                
                choices_processed.append(choice)
            
            if (choices_processed is not None) and (len(choices_processed) > APPLICATION_COMMAND_CHOICES_MAX):
                del choices_processed[APPLICATION_COMMAND_CHOICES_MAX:]
        
        
        # default
        assert _assert__application_command_option__default(default)
        
        # description
        assert _assert__application_command_option__description(description)
        
        # description_localizations
        description_localizations = localized_dictionary_builder(description_localizations, 'description_localizations')
        
        # max_length
        # requires `type`
        
        # max_value
        # requires `type`
        
        # min_length
        # requires `type`
        
        # min_value
        # requires `type`
        
        # name
        assert _assert__application_command_option__name(name)
        
        # name_localizations
        name_localizations = localized_dictionary_builder(name_localizations, 'name_localizations')
        
        # options
        options_processed = None
        
        if (options is not None):
            if getattr(options, '__iter__', None) is None:
                raise TypeError(
                    f'`options` can be `None`, `iterable` of `{ApplicationCommandOption.__name__}`, '
                    f'got {options.__class__.__name__}; {options!r}.'
                )
            
            for option in options:
                if not isinstance(option, ApplicationCommandOption):
                    raise TypeError(
                        f'`options` contains a non `{ApplicationCommandOption.__name__}` element, got '
                        f'{option.__class__.__name__}; {option!r}; options={options!r}.'
                    )
                
                if (options_processed is None):
                    options_processed = []
                
                options_processed.append(option)
            
            if (options_processed is not None) and (len(options_processed) > APPLICATION_COMMAND_OPTIONS_MAX):
                # Deleting the excess should be fine.
                del options_processed[APPLICATION_COMMAND_OPTIONS_MAX:]
        
        
        # required
        assert _assert__application_command_option__required(required)
        
        # type
        type_ = preconvert_preinstanced_type(type_, 'type_', ApplicationCommandOptionType)
        
        # Postprocessing
        
        # max_length
        max_length = _validate_max_length(max_length, type_)
        
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
                    f'type_={type_!r}; max_value = {max_value!r}.'
                )
        
        # min_length
        min_length = _validate_min_length(min_length, type_)
        
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
                    f'type_={type_!r}; min_value = {min_value!r}.'
                )
        
        # postprocessing | autocomplete
        assert _assert__application_command_option__autocomplete__applicability(autocomplete, choices_processed, type_)

        
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
        assert _assert__application_command_option__channel_types__applicability(channel_types_processed, type_)
        
        
        self = object.__new__(cls)
        
        self.autocomplete = autocomplete
        self.channel_types = channel_types_processed
        self.choices = choices_processed
        self.default = default
        self.description = description
        self.description_localizations = description_localizations
        self.max_length = max_length
        self.max_value = max_value
        self.min_length = min_length
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
            - If the source application command's type is not a sub-command group type.
            - If `option` is not ``ApplicationCommandOption``.
            - If `option` is a sub command group option.
        """
        if self.type is not ApplicationCommandOptionType.sub_command_group:
            raise TypeError(
                f'`option` can be added only if the command option\s type is sub command option, '
                f'got option={option!r}, self={self!r}.'
            )
        
        if not isinstance(option, ApplicationCommandOption):
            raise TypeError(
                f'`option` can be `{ApplicationCommandOption.__name__}`, got '
                f'{option.__class__.__name__}; {option!r}.'
            )
    
        if option.type is ApplicationCommandOptionType.sub_command_group:
            raise TypeError(
                f'`option`\'s type is sub-command group option, but sub-command groups cannot be '
                f'added under sub-command groups; got {option!r}; self={self!r}.'
            )
        
        options = self.options
        if options is None:
            options = []
            self.options = options
        
        if len(options) < APPLICATION_COMMAND_OPTIONS_MAX:
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
                and `.value`.
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
            choices = []
            self.choices = choices
        
        if len(choices) < APPLICATION_COMMAND_CHOICES_MAX:
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
            channel_types = tuple(sorted(ChannelType.get(channel_type) for channel_type in channel_types))
        
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
        
        # max_length
        max_length = data.get('max_length', None)
        if (max_length is None) or (max_length == APPLICATION_COMMAND_OPTION_MAX_LENGTH_MAX):
            max_length = 0
        
        # max_value
        max_value = data.get('max_value', None)
        
        # min_length
        min_length = data.get('min_length', None)
        if (min_length is None):
            min_length = 0
        
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
        self.max_length = max_length
        self.max_value = max_value
        self.min_length = min_length
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
            data['channel_types'] = [channel_type.value for channel_type in channel_types]
        
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
        
        type_ = self.type
        
        # max_length
        if (type_ is ApplicationCommandOptionType.string):
            max_length = self.max_length
            if (max_length == 0):
                max_length = APPLICATION_COMMAND_OPTION_MAX_LENGTH_MAX
            
            data['max_length'] = max_length
        
        # max_value
        max_value = self.max_value
        if (max_value is not None):
            data['max_value'] = max_value
        
        # min_length
        if (type_ is ApplicationCommandOptionType.string):
            data['min_length'] = self.min_length
        
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
        data['type'] = type_.value
        
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
        #    `.name_localizations`, `.description_localizations`, `.min_length`, `.max_length`
        
        # autocomplete
        if self.autocomplete:
            repr_parts.append(', autocomplete=True')
        
        # default
        if self.default:
            repr_parts.append(', default = True')
        
        # required
        if self.required:
            repr_parts.append(', required=True')
        
        if type_ is ApplicationCommandOptionType.string:
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
        
        
        if type_ is ApplicationCommandOptionType.integer or type_ is ApplicationCommandOptionType.float:
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
    
    
    def apply_translation(self, translation_table, replace=False):
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
