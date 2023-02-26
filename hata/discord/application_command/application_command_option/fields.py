__all__ = ()

from functools import partial as partial_func

from ...channel import ChannelType
from ...field_parsers import (
    bool_parser_factory, field_parser_factory, force_string_parser_factory, int_parser_factory,
    nullable_functional_parser_factory, nullable_object_array_parser_factory, nullable_string_parser_factory,
    preinstanced_array_parser_factory, preinstanced_parser_factory
)
from ...field_putters import (
    bool_optional_putter_factory, force_string_putter_factory, int_optional_putter_factory,
    nullable_entity_array_optional_putter_factory, nullable_field_optional_putter_factory,
    nullable_functional_optional_putter_factory, nullable_string_putter_factory, preinstanced_array_putter_factory,
    preinstanced_putter_factory
)
from ...field_validators import (
    bool_validator_factory, force_string_validator_factory, nullable_object_array_validator_factory,
    nullable_string_validator_factory, preinstanced_array_validator_factory, preinstanced_validator_factory
)
from ...localization.helpers import localized_dictionary_builder
from ...localization.utils import build_locale_dictionary, destroy_locale_dictionary

from ..application_command_option_choice import ApplicationCommandOptionChoice

from .constants import (
    APPLICATION_COMMAND_OPTION_CHOICES_MAX, APPLICATION_COMMAND_OPTION_DESCRIPTION_LENGTH_MAX,
    APPLICATION_COMMAND_OPTION_DESCRIPTION_LENGTH_MIN, APPLICATION_COMMAND_OPTION_MAX_LENGTH_DEFAULT,
    APPLICATION_COMMAND_OPTION_MAX_LENGTH_MAX, APPLICATION_COMMAND_OPTION_MAX_LENGTH_MIN,
    APPLICATION_COMMAND_OPTION_MIN_LENGTH_DEFAULT, APPLICATION_COMMAND_OPTION_MIN_LENGTH_MAX,
    APPLICATION_COMMAND_OPTION_MIN_LENGTH_MIN, APPLICATION_COMMAND_OPTION_NAME_LENGTH_MAX,
    APPLICATION_COMMAND_OPTION_NAME_LENGTH_MIN, APPLICATION_COMMAND_OPTION_OPTIONS_MAX
)
from .preinstanced import ApplicationCommandOptionType


APPLICATION_COMMAND_OPTION_TYPE_CHANNEL = ApplicationCommandOptionType.channel
APPLICATION_COMMAND_OPTION_TYPE_FLOAT = ApplicationCommandOptionType.float
APPLICATION_COMMAND_OPTION_TYPE_INTEGER = ApplicationCommandOptionType.integer
APPLICATION_COMMAND_OPTION_TYPE_NONE = ApplicationCommandOptionType.none
APPLICATION_COMMAND_OPTION_TYPE_STRING = ApplicationCommandOptionType.string
APPLICATION_COMMAND_OPTION_TYPE_SUB_COMMAND = ApplicationCommandOptionType.sub_command
APPLICATION_COMMAND_OPTION_TYPE_SUB_COMMAND_GROUP = ApplicationCommandOptionType.sub_command_group

# autocomplete

parse_autocomplete = bool_parser_factory('autocomplete', False)
put_autocomplete_into = bool_optional_putter_factory('autocomplete', False)
_pre_validate_autocomplete = bool_validator_factory('autocomplete', False)


def validate_autocomplete(autocomplete, option_type = APPLICATION_COMMAND_OPTION_TYPE_NONE):
    """
    Validates an application command option's `autocomplete` field.
    
    Parameters
    ----------
    autocomplete : `bool`
        Whether the field is auto completed.
        
        Only applicable for string options.
    
    option_type : ``ApplicationCommandOptionType`` = `ApplicationCommandOptionType.none`, Optional
        Respective application command option type.
    
    Returns
    -------
    autocomplete : `bool`
    
    Raises
    ------
    TypeError
        - If `autocomplete`'s type is incorrect.
    ValueError
        - If `autocomplete`'s value is incorrect.
        - If `autocomplete` is not applicable for the given type.
    """
    autocomplete = _pre_validate_autocomplete(autocomplete)
    if autocomplete:
        if (
            (option_type is not APPLICATION_COMMAND_OPTION_TYPE_NONE) and
            (option_type is not APPLICATION_COMMAND_OPTION_TYPE_STRING) and
            (option_type is not APPLICATION_COMMAND_OPTION_TYPE_INTEGER) and
            (option_type is not APPLICATION_COMMAND_OPTION_TYPE_FLOAT)
        ):
            raise ValueError(
                f'`channel_types` is only meaningful if '
                f'`option_type` is `{ApplicationCommandOptionType.__name__}.string`, '
                f'`{ApplicationCommandOptionType.__name__}.integer`, `{ApplicationCommandOptionType.__name__}.float`,'
                f'got option_type = {option_type!r}; autocomplete = {autocomplete!r}.'
            )
    
    return autocomplete


# channel_types

parse_channel_types = preinstanced_array_parser_factory('channel_types', ChannelType)
put_channel_types_into = preinstanced_array_putter_factory('channel_types')

_pre_validate_channel_types = preinstanced_array_validator_factory('channel_types', ChannelType)


def validate_channel_types(channel_types, option_type = APPLICATION_COMMAND_OPTION_TYPE_NONE):
    """
    Validates an application command option's `channel_types` field.
    
    Parameters
    ----------
    channel_types : `None`, `iterable` of (`int`, ``ChannelType``)
        The allowed channel types by the option.
        
        Only applicable for string options.
    
    option_type : ``ApplicationCommandOptionType`` = `ApplicationCommandOptionType.none`, Optional
        Respective application command option type.
    
    Returns
    -------
    channel_types : `None`, `tuple` of ``ChannelType``
    
    Raises
    ------
    TypeError
        - If `channel_types`'s type is incorrect.
    ValueError
        - If `channel_types` is not applicable for the given type.
    """
    channel_types = _pre_validate_channel_types(channel_types)
    if (channel_types is not None):
        if (
            (option_type is not APPLICATION_COMMAND_OPTION_TYPE_NONE) and
            (option_type is not APPLICATION_COMMAND_OPTION_TYPE_CHANNEL)
        ):
            raise ValueError(
                f'`channel_types` is only meaningful if '
                f'`option_type` is `{ApplicationCommandOptionType.__name__}.channel`, got '
                f'option_type = {option_type!r}; channel_types = {channel_types!r}.'
            )
    
    return channel_types


# choices

parse_choices = nullable_object_array_parser_factory('choices', ApplicationCommandOptionChoice)
put_choices_into = nullable_entity_array_optional_putter_factory('choices', ApplicationCommandOptionChoice)

_pre_validate_choices = nullable_object_array_validator_factory('choices', ApplicationCommandOptionChoice)


def validate_choices(choices, option_type = APPLICATION_COMMAND_OPTION_TYPE_NONE):
    """
    Validates the given application command option `choices` field.
    
    Parameters
    ----------
    choices : `None`, `iterable` of ``ApplicationCommandOptionChoice``
        The choices of the command for string or integer types. It's length can be in range [0:25].
    
    option_type : ``ApplicationCommandOptionType`` = `ApplicationCommandOptionType.none`, Optional
        Respective application command option type.
    
    Returns
    -------
    choices : `None`, `tuple` of ``ApplicationCommandOptionChoice``
    
    Returns
    -------
    TypeError
        - If `choices`'s type is incorrect.
    ValueError
        - If `choices`'s value is incorrect.
        - If `choices` is not applicable for the given type.
    """
    choices = _pre_validate_choices(choices)
    
    if (choices is not None):
        if (option_type is not APPLICATION_COMMAND_OPTION_TYPE_NONE):
            if option_type is ApplicationCommandOptionType.string:
                expected_choice_type = str
            elif option_type is ApplicationCommandOptionType.integer:
                expected_choice_type = int
            elif option_type is ApplicationCommandOptionType.float:
                expected_choice_type = float
            else:
                raise ValueError(
                    f'`choices` can be bound either to string, integer or float option types, got '
                    f'choices = {choices!r}, option_type = {option_type!r}.'
                )
        
            for choice in choices:
                if not isinstance(choice.value, expected_choice_type):
                    raise TypeError(
                        f'`choices` contains an element with a non-`{expected_choice_type.__name__}` value. '
                        f'Got {choice.__class__.__name__}; {choice!r}; choices = {choices!r}; '
                        f'option_type = {option_type!r}.'
                    )
        
        choices = choices[:APPLICATION_COMMAND_OPTION_CHOICES_MAX]
    
    return choices


# default

parse_default = bool_parser_factory('default', False)
put_default_into = bool_optional_putter_factory('default', False)
_pre_validate_default = bool_validator_factory('default', False)


def validate_default(default, option_type = APPLICATION_COMMAND_OPTION_TYPE_NONE):
    """
    Validates an application command option's `default` field.
    
    Parameters
    ----------
    default : `bool`
        Whether the option is the default one. Only one option can be `default`.
        
        Only applicable for sub-command and sub-command group options.
    
    option_type : ``ApplicationCommandOptionType`` = `ApplicationCommandOptionType.none`, Optional
        Respective application command option type.
    
    Returns
    -------
    default : `bool`
    
    Raises
    ------
    TypeError
        - If `default`'s type is incorrect.
    ValueError
        - If `default`'s value is incorrect.
        - If `default` is not applicable for the given type.
    """
    default = _pre_validate_default(default)
    if default:
        if (
            (option_type is not APPLICATION_COMMAND_OPTION_TYPE_NONE) and
            (option_type is not APPLICATION_COMMAND_OPTION_TYPE_SUB_COMMAND) and
            (option_type is not APPLICATION_COMMAND_OPTION_TYPE_SUB_COMMAND_GROUP)
        ):
            raise ValueError(
                f'`channel_types` is only meaningful if '
                f'`option_type` is `{ApplicationCommandOptionType.__name__}.sub_command` or '
                f'`{ApplicationCommandOptionType.__name__}.sub_command_group`, got '
                f'option_type = {option_type!r}; default = {default!r}.'
            )
    
    return default

# description

parse_description = nullable_string_parser_factory('description')
put_description_into = nullable_string_putter_factory('description')
validate_description = nullable_string_validator_factory(
    'description', APPLICATION_COMMAND_OPTION_DESCRIPTION_LENGTH_MIN, APPLICATION_COMMAND_OPTION_DESCRIPTION_LENGTH_MAX
)

# description_localizations

parse_description_localizations = nullable_functional_parser_factory(
    'description_localizations', build_locale_dictionary
)
put_description_localizations_into = nullable_functional_optional_putter_factory(
    'description_localizations', destroy_locale_dictionary
)
validate_description_localizations = partial_func(
    localized_dictionary_builder, parameter_name = 'description_localizations'
)

# max_length

def parse_max_length(data):
    """
    Parses out the `max_length` field from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `object`) items
        Channel data.
    
    Returns
    -------
    max_length : `int`
    """
    max_length = data.get('max_length', None)
    if (max_length is None) or (max_length == APPLICATION_COMMAND_OPTION_MAX_LENGTH_MAX):
        max_length = APPLICATION_COMMAND_OPTION_MAX_LENGTH_DEFAULT

    return max_length


def put_max_length_into(max_length, data, defaults):
    """
    Puts the `max_length`'s value into the given `data` json serializable object.
    
    Parameters
    ----------
    max_length : `bool`
        The `max_length` field value.
    data : `dict` of (`str`, `object`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `object`) items
    """
    if (max_length == 0):
        max_length = APPLICATION_COMMAND_OPTION_MAX_LENGTH_MAX
    
    data['max_length'] = max_length
    return data


def validate_max_length(max_length, option_type = APPLICATION_COMMAND_OPTION_TYPE_NONE):
    """
    Validates an application command option's `max_length` field.
    
    Parameters
    ----------
    max_length : `None`, `int`
        The maximum input length allowed for this option.
        
        Only applicable for string options.
    
    option_type : ``ApplicationCommandOptionType`` = `ApplicationCommandOptionType.none`, Optional
        Respective application command option type.
    
    Returns
    -------
    max_length : `int`
    
    Raises
    ------
    TypeError
        - If `max_length`'s type is incorrect.
    ValueError
        - If `max_length`'s value is incorrect.
        - If `max_length` is not applicable for the given type.
    """
    if (max_length is None):
        return APPLICATION_COMMAND_OPTION_MAX_LENGTH_DEFAULT
    
    if not isinstance(max_length, int):
        raise TypeError(
            f'`max_length` can be `None`, `int`, got {max_length.__class__.__name__}; {max_length!r}.'
        )
        
    if max_length == APPLICATION_COMMAND_OPTION_MAX_LENGTH_DEFAULT:
        return APPLICATION_COMMAND_OPTION_MAX_LENGTH_DEFAULT
    
    if (
        (option_type is not APPLICATION_COMMAND_OPTION_TYPE_NONE) and
        (option_type is not APPLICATION_COMMAND_OPTION_TYPE_STRING)
    ):
        raise ValueError(
            f'`max_length` is only meaningful if `type` is {ApplicationCommandOptionType.string!r}, got '
            f'option_type = {option_type!r}; max_length = {max_length!r}.'
        )
    
    if max_length < APPLICATION_COMMAND_OPTION_MAX_LENGTH_MIN:
        max_length = APPLICATION_COMMAND_OPTION_MAX_LENGTH_MIN
    
    elif max_length >= APPLICATION_COMMAND_OPTION_MAX_LENGTH_MAX:
        max_length = APPLICATION_COMMAND_OPTION_MAX_LENGTH_DEFAULT

    return max_length


# max_value

parse_max_value = field_parser_factory('max_value')
put_max_value_into = nullable_field_optional_putter_factory('max_value')

def validate_max_value(max_value, option_type = APPLICATION_COMMAND_OPTION_TYPE_NONE):
    """
    Validates an application command option's `max_value` field.
    
    Parameters
    ----------
    max_value : `None`, `int`, `float`
        The maximum input value allowed for this option.
        
        Only applicable for string options.
    
    option_type : ``ApplicationCommandOptionType`` = `ApplicationCommandOptionType.none`, Optional
        Respective application command option type.
    
    Returns
    -------
    max_value : `None`, `int`, `float`
    
    Raises
    ------
    TypeError
        - If `max_value`'s type is incorrect.
    ValueError
        - If `max_value`'s value is incorrect.
        - If `max_value` is not applicable for the given type.
    """
    if max_value is None:
        return max_value
    
    if not isinstance(max_value, (int, float)):
        raise TypeError(
            f'`max_value` can be either `None`, `int`, `float` depending on the option\'s type. '
            f'Got {max_value.__class__.__name__}; max_value = {max_value!r}.'
        )
    
    if option_type is APPLICATION_COMMAND_OPTION_TYPE_NONE:
        return max_value
    
    if option_type is APPLICATION_COMMAND_OPTION_TYPE_INTEGER:
        if not isinstance(max_value, int):
            raise ValueError(
                f'`max_value` can be `int`, if `option_type` is defined as {option_type!r}, got '
                f'{max_value.__class__.__name__}; {max_value!r}.'
            )
        
        return max_value
    
    if option_type is APPLICATION_COMMAND_OPTION_TYPE_FLOAT:
        if not isinstance(max_value, float):
            raise ValueError(
                f'`max_value` can be `float`, if `option_type` is defined as {option_type!r}, got '
                f'{max_value.__class__.__name__}; {max_value!r}.'
            )
        
        return max_value
    
    raise ValueError(
        f'`max_value` is only meaningful if `type` is either '
        f'{ApplicationCommandOptionType.integer!r}, or {ApplicationCommandOptionType.float!r}, got '
        f'option_type = {option_type!r}; max_value = {max_value!r}.'
    )

# min_length

parse_min_length = int_parser_factory('min_length', APPLICATION_COMMAND_OPTION_MIN_LENGTH_DEFAULT)
put_min_length_into = int_optional_putter_factory('min_length', APPLICATION_COMMAND_OPTION_MIN_LENGTH_MIN)


def validate_min_length(min_length, option_type = APPLICATION_COMMAND_OPTION_TYPE_NONE):
    """
    Validates an application command option's `min_length` field.
    
    Parameters
    ----------
    min_length : `None`, `int`
        The minimum input length allowed for this option.
        
        Only applicable for string options.
    
    
    option_type : ``ApplicationCommandOptionType`` = `ApplicationCommandOptionType.none`, Optional
        Respective application command option type.
    
    Returns
    -------
    min_length : `int`
    
    Raises
    ------
    TypeError
        - If `min_length`'s type is incorrect.
    ValueError
        - If `min_length`'s value is incorrect.
        - If `min_length` is not applicable for the given type.
    """
    if (min_length is None):
        return APPLICATION_COMMAND_OPTION_MIN_LENGTH_DEFAULT
    
    if not isinstance(min_length, int):
        raise TypeError(
            f'`min_length` can be `None`, `int`, got {min_length.__class__.__name__}; {min_length!r}.'
        )
        
    if min_length == APPLICATION_COMMAND_OPTION_MIN_LENGTH_DEFAULT:
        return APPLICATION_COMMAND_OPTION_MIN_LENGTH_DEFAULT
    
    if (
        (option_type is not APPLICATION_COMMAND_OPTION_TYPE_NONE) and
        (option_type is not APPLICATION_COMMAND_OPTION_TYPE_STRING)
    ):
        raise ValueError(
            f'`min_length` is only meaningful if `type` is {ApplicationCommandOptionType.string!r}, got '
            f'option_type = {option_type!r}; {min_length!r}.'
        )
    
    if min_length < APPLICATION_COMMAND_OPTION_MIN_LENGTH_MIN:
        min_length = APPLICATION_COMMAND_OPTION_MIN_LENGTH_MIN
    
    elif min_length > APPLICATION_COMMAND_OPTION_MIN_LENGTH_MAX:
        min_length = APPLICATION_COMMAND_OPTION_MIN_LENGTH_MAX

    return min_length


# min_value

parse_min_value = field_parser_factory('min_value')
put_min_value_into = nullable_field_optional_putter_factory('min_value')

def validate_min_value(min_value, option_type = APPLICATION_COMMAND_OPTION_TYPE_NONE):
    """
    Validates an application command option's `min_value` field.
    
    Parameters
    ----------
    min_value : `None`, `int`, `float`
        The maximum input value allowed for this option.
        
        Only applicable for string options.
    
    option_type : ``ApplicationCommandOptionType`` = `ApplicationCommandOptionType.none`, Optional
        Respective application command option type.
    
    Returns
    -------
    min_value : `None`, `int`, `float`
    
    Raises
    ------
    TypeError
        - If `min_value`'s type is incorrect.
    ValueError
        - If `min_value`'s value is incorrect.
        - If `min_value` is not applicable for the given type.
    """
    if min_value is None:
        return None
    
    if not isinstance(min_value, (int, float)):
        raise TypeError(
            f'`min_value` can be either `None`, `int`, `float` depending on the option\'s type. '
            f'Got {min_value.__class__.__name__}; min_value = {min_value!r}.'
        )

    if option_type is APPLICATION_COMMAND_OPTION_TYPE_NONE:
        return min_value
    
    if option_type is ApplicationCommandOptionType.integer:
        if not isinstance(min_value, int):
            raise ValueError(
                f'`min_value` can be `int` if `option_type` is defined as {option_type!r}, got '
                f'{min_value.__class__.__name__}; {min_value!r}.'
            )
        
        return min_value
    
    if option_type is ApplicationCommandOptionType.float:
        if not isinstance(min_value, float):
            raise ValueError(
                f'`min_value` can be `float` if `option_type` is defined as {option_type!r}, got '
                f'{min_value.__class__.__name__}; {min_value!r}.'
            )
        
        return min_value
    
    raise ValueError(
        f'`min_value` is only meaningful if `type` is either '
        f'{ApplicationCommandOptionType.integer!r}, or {ApplicationCommandOptionType.float!r}, got '
        f'option_type = {option_type!r}; min_value = {min_value!r}.'
    )

# name

parse_name = force_string_parser_factory('name')
put_name_into = force_string_putter_factory('name')
validate_name = force_string_validator_factory(
    'name', APPLICATION_COMMAND_OPTION_NAME_LENGTH_MIN, APPLICATION_COMMAND_OPTION_NAME_LENGTH_MAX
)

# name_localizations

parse_name_localizations = nullable_functional_parser_factory(
    'name_localizations', build_locale_dictionary
)
put_name_localizations_into = nullable_functional_optional_putter_factory(
    'name_localizations', destroy_locale_dictionary
)
validate_name_localizations = partial_func(
    localized_dictionary_builder, parameter_name = 'name_localizations'
)

# options

parse_options = nullable_object_array_parser_factory('options', NotImplemented, include = 'ApplicationCommandOption')
put_options_into = nullable_entity_array_optional_putter_factory(
    'options', NotImplemented, can_include_internals = False, include = 'ApplicationCommandOption'
)

_pre_validate_options = nullable_object_array_validator_factory(
    'options', NotImplemented, include = 'ApplicationCommandOption'
)


def validate_options(options):
    """
    Validates the given application command option `options` field.
    
    Parameters
    ----------
    options : `None`, `iterable` of ``ApplicationCommandOption``
        The parameters or sub-commands of the command option. It's length can be in range [0:25].
    
    Returns
    -------
    options : `None`, `tuple` of ``ApplicationCommandOption``
    
    Returns
    -------
    TypeError
        - If `options`'s type is incorrect.
    ValueError
        - If `options`'s value is incorrect.
        - If `options` is not applicable for the given type.
    """
    options = _pre_validate_options(options)
    if (options is not None):
        options = options[:APPLICATION_COMMAND_OPTION_OPTIONS_MAX]
    
    return options


# required

parse_required = bool_parser_factory('required', False)
put_required_into = bool_optional_putter_factory('required', False)
validate_required = bool_validator_factory('required', False)

# type

parse_type = preinstanced_parser_factory('type', ApplicationCommandOptionType, ApplicationCommandOptionType.none)
put_type_into = preinstanced_putter_factory('type')
validate_type = preinstanced_validator_factory('option_type', ApplicationCommandOptionType)
