__all__ = ()

from ...channel import ChannelType
from ...field_parsers import (
    bool_parser_factory, field_parser_factory, int_parser_factory, nullable_object_array_parser_factory,
    preinstanced_array_parser_factory
)
from ...field_putters import (
    bool_optional_putter_factory, int_optional_putter_factory, nullable_entity_array_optional_putter_factory,
    nullable_field_optional_putter_factory, preinstanced_array_putter_factory,
)
from ...field_validators import (
    bool_validator_factory, nullable_object_array_validator_factory, preinstanced_array_validator_factory
)

from ..application_command_option_choice import ApplicationCommandOptionChoice

from .constants import (
    APPLICATION_COMMAND_OPTION_CHOICES_MAX, APPLICATION_COMMAND_OPTION_MAX_LENGTH_DEFAULT,
    APPLICATION_COMMAND_OPTION_MAX_LENGTH_MAX, APPLICATION_COMMAND_OPTION_MAX_LENGTH_MIN,
    APPLICATION_COMMAND_OPTION_MIN_LENGTH_DEFAULT, APPLICATION_COMMAND_OPTION_MIN_LENGTH_MAX,
    APPLICATION_COMMAND_OPTION_MIN_LENGTH_MIN, APPLICATION_COMMAND_OPTION_OPTIONS_MAX
)

# autocomplete

parse_autocomplete = bool_parser_factory('autocomplete', False)
put_autocomplete_into = bool_optional_putter_factory('autocomplete', False)
validate_autocomplete = bool_validator_factory('autocomplete', False)


# channel_types

parse_channel_types = preinstanced_array_parser_factory('channel_types', ChannelType)
put_channel_types_into = preinstanced_array_putter_factory('channel_types')
validate_channel_types = preinstanced_array_validator_factory('channel_types', ChannelType)


# choices

parse_choices = nullable_object_array_parser_factory('choices', ApplicationCommandOptionChoice)
put_choices_into = nullable_entity_array_optional_putter_factory('choices', ApplicationCommandOptionChoice)
validate_choices = nullable_object_array_validator_factory('choices', ApplicationCommandOptionChoice)


def validate_choices_postprocessed(choices, expected_choice_type):
    """
    Validates the given application command option `choices` field. 
    
    Parameters
    ----------
    choices : `None`, `iterable` of ``ApplicationCommandOptionChoice``
        The choices of the command for string or integer types. It's length can be in range [0:25].
    
    expected_choice_type : `type`
        The expected option value type.
    
    Returns
    -------
    choices : `None`, `tuple` of ``ApplicationCommandOptionChoice``
    
    Returns
    -------
    TypeError
        - If `choices`'s type is incorrect.
    ValueError
        - If `choices`'s value is incorrect.
    """
    choices = validate_choices(choices)
    
    if (choices is not None):
        for choice in choices:
            if not isinstance(choice.value, expected_choice_type):
                raise TypeError(
                    f'`choices` contains an element with a non-`{expected_choice_type.__name__}` value. '
                    f'Got {choice.__class__.__name__}; {choice!r}; choices = {choices!r}.'
                )
        
        choices = choices[:APPLICATION_COMMAND_OPTION_CHOICES_MAX]
    
    return choices


# default

parse_default = bool_parser_factory('default', False)
put_default_into = bool_optional_putter_factory('default', False)
validate_default = bool_validator_factory('default', False)


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


def validate_max_length(max_length):
    """
    Validates an application command option's `max_length` field.
    
    Parameters
    ----------
    max_length : `None`, `int`
        The maximum input length allowed for this option.
        
        Only applicable for string options.
    
    Returns
    -------
    max_length : `int`
    
    Raises
    ------
    TypeError
        - If `max_length`'s type is incorrect.
    ValueError
        - If `max_length`'s value is incorrect.
    """
    if (max_length is None):
        return APPLICATION_COMMAND_OPTION_MAX_LENGTH_DEFAULT
    
    if not isinstance(max_length, int):
        raise TypeError(
            f'`max_length` can be `None`, `int`, got {max_length.__class__.__name__}; {max_length!r}.'
        )
        
    if max_length == APPLICATION_COMMAND_OPTION_MAX_LENGTH_DEFAULT:
        return APPLICATION_COMMAND_OPTION_MAX_LENGTH_DEFAULT
    
    if max_length < APPLICATION_COMMAND_OPTION_MAX_LENGTH_MIN:
        max_length = APPLICATION_COMMAND_OPTION_MAX_LENGTH_MIN
    
    elif max_length >= APPLICATION_COMMAND_OPTION_MAX_LENGTH_MAX:
        max_length = APPLICATION_COMMAND_OPTION_MAX_LENGTH_DEFAULT

    return max_length


# max_value

parse_max_value = field_parser_factory('max_value')
put_max_value_into = nullable_field_optional_putter_factory('max_value')

def validate_max_value(max_value):
    """
    Validates an application command option's `max_value` field.
    
    Parameters
    ----------
    max_value : `None`, `int`, `float`
        The maximum input value allowed for this option.
    
    Returns
    -------
    max_value : `None`, `int`, `float`
    
    Raises
    ------
    TypeError
        - If `max_value`'s type is incorrect.
    ValueError
        - If `max_value`'s value is incorrect.
    """
    if (max_value is None) or isinstance(max_value, (int, float)):
        return max_value
    
    raise TypeError(
        f'`max_value` can be either `None`, `int`, `float` depending on the option\'s type. '
        f'Got {max_value.__class__.__name__}; max_value = {max_value!r}.'
    )
    

def validate_max_value_postprocessed(max_value, expected_value_type):
    """
    Validates an application command option's `max_value` field.
    
    Parameters
    ----------
    max_value : `None`, `int`, `float`
        The maximum input value allowed for this option.
    expected_value_type : `type`
        The expected value type of `max_value`
    
    Returns
    -------
    max_value : `None`, `instance<expected_value_type>`
    
    Raises
    ------
    TypeError
        - If `max_value`'s type is incorrect.
    ValueError
        - If `max_value`'s value is incorrect.
        - if `max_value`'s type is not expected.
    """
    max_value = validate_max_value(max_value)
    if (max_value is None) or isinstance(max_value, expected_value_type):
        return max_value
    
    raise ValueError(
        f'`max_value` was expected either as `None`, `{expected_value_type.__name__}`, got '
        f'{max_value.__class__.__name__}; max_value = {max_value!r}.'
    )


# min_length

parse_min_length = int_parser_factory('min_length', APPLICATION_COMMAND_OPTION_MIN_LENGTH_DEFAULT)
put_min_length_into = int_optional_putter_factory('min_length', APPLICATION_COMMAND_OPTION_MIN_LENGTH_MIN)


def validate_min_length(min_length):
    """
    Validates an application command option's `min_length` field.
    
    Parameters
    ----------
    min_length : `None`, `int`
        The minimum input length allowed for this option.
    
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
    
    if min_length < APPLICATION_COMMAND_OPTION_MIN_LENGTH_MIN:
        min_length = APPLICATION_COMMAND_OPTION_MIN_LENGTH_MIN
    
    elif min_length > APPLICATION_COMMAND_OPTION_MIN_LENGTH_MAX:
        min_length = APPLICATION_COMMAND_OPTION_MIN_LENGTH_MAX

    return min_length


# min_value

parse_min_value = field_parser_factory('min_value')
put_min_value_into = nullable_field_optional_putter_factory('min_value')


def validate_min_value(min_value):
    """
    Validates an application command option's `min_value` field.
    
    Parameters
    ----------
    min_value : `None`, `int`, `float`
        The maximum input value allowed for this option.
        
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
    if min_value is None or isinstance(min_value, (int, float)):
        return min_value
        
    raise TypeError(
        f'`min_value` can be either `None`, `int`, `float` depending on the option\'s type. '
        f'Got {min_value.__class__.__name__}; min_value = {min_value!r}.'
    )
    

def validate_min_value_postprocessed(min_value, expected_value_type):
    """
    Validates an application command option's `min_value` field.
    
    Parameters
    ----------
    min_value : `None`, `int`, `float`
        The minimal input value allowed for this option.
    expected_value_type : `type`
        The expected value type of `min_value`
    
    Returns
    -------
    min_value : `None`, `instance<expected_value_type>`
    
    Raises
    ------
    TypeError
        - If `min_value`'s type is incorrect.
    ValueError
        - If `min_value`'s value is incorrect.
        - if `min_value`'s type is not expected.
    """
    min_value = validate_min_value(min_value)
    if (min_value is None) or isinstance(min_value, expected_value_type):
        return min_value
    
    raise ValueError(
        f'`min_value` was expected either as `None`, `{expected_value_type.__name__}`, got '
        f'{min_value.__class__.__name__}; min_value = {min_value!r}.'
    )

# options

parse_options = nullable_object_array_parser_factory('options', NotImplemented, include = 'ApplicationCommandOption')
put_options_into = nullable_entity_array_optional_putter_factory(
    'options', NotImplemented, can_include_internals = False, include = 'ApplicationCommandOption'
)

validate_options = nullable_object_array_validator_factory(
    'options', NotImplemented, include = 'ApplicationCommandOption'
)


def validate_options_postprocessed(options):
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
    options = validate_options(options)
    if (options is not None):
        options = options[:APPLICATION_COMMAND_OPTION_OPTIONS_MAX]
    
    return options

# required

parse_required = bool_parser_factory('required', False)
put_required_into = bool_optional_putter_factory('required', False)
validate_required = bool_validator_factory('required', False)
