__all__ = ()

from enum import Enum
from functools import partial as partial_func

from ...field_parsers import field_parser_factory, force_string_parser_factory, nullable_functional_parser_factory
from ...field_putters import (
    field_putter_factory, force_string_putter_factory, nullable_functional_optional_putter_factory
)
from ...localization.helpers import localized_dictionary_builder
from ...localization.utils import build_locale_dictionary, destroy_locale_dictionary

from .constants import (
    APPLICATION_COMMAND_CHOICE_NAME_LENGTH_MAX, APPLICATION_COMMAND_CHOICE_NAME_LENGTH_MIN,
    APPLICATION_COMMAND_CHOICE_VALUE_LENGTH_MAX, APPLICATION_COMMAND_CHOICE_VALUE_LENGTH_MIN
)

# name

parse_name = force_string_parser_factory('name')
put_name_into = force_string_putter_factory('name')


def validate_name(name):
    """
    Validates the given application command choice name.
    
    Parameters
    ----------
    name : `str`, `Enum`
        The name to validate.
    
    Returns
    -------
    name : `str`
        The validated name.
    
    Raises
    ------
    TypeError
        - If `name`'s type is incorrect.
    ValueError
        - If `name's length is out of the expected range.
    """
    if isinstance(name, Enum):
        processed_name = name.name
    else:
        processed_name = name
    
    # Check name type again in case enum name is not string, lol
    if not isinstance(processed_name, str):
        raise TypeError(
            f'`name` type can be `str`, `{Enum.__name__}`, '
            f'got {processed_name.__class__.__name__}; {processed_name!r}.'
        )
    
    name_length = len(processed_name)
    if (
        (name_length < APPLICATION_COMMAND_CHOICE_NAME_LENGTH_MIN) or
        (name_length > APPLICATION_COMMAND_CHOICE_NAME_LENGTH_MAX)
    ):
        raise ValueError(
            f'`name` length` can be in range '
            f'[{APPLICATION_COMMAND_CHOICE_NAME_LENGTH_MIN}:{APPLICATION_COMMAND_CHOICE_NAME_LENGTH_MAX}]'
            f'got {name_length!r}; {name!r}.'
        )
    
    return processed_name


# name_localizations

parse_name_localizations = nullable_functional_parser_factory(
    'name_localizations', build_locale_dictionary
)
put_name_localizations_into = nullable_functional_optional_putter_factory(
    'name_localizations', destroy_locale_dictionary
)
validate_name_localizations = partial_func(localized_dictionary_builder, parameter_name = 'name_localizations')



# value

parse_value = field_parser_factory('value')
put_value_into = field_putter_factory('value')


def validate_value(value):
    """
    Validates the given application command choice value.
    
    Parameters
    ----------
    value : `str`, `int`, `float`, `Enum`
        The value to validate.
    
    Returns
    -------
    value : `str`, `int`, `float`
        The validated value.
    
    Raises
    ------
    TypeError
        - If `value`'s type is incorrect.
    ValueError
        - If `value's length is out of the expected range.
    """
    if isinstance(value, Enum):
        processed_value = value.value
    else:
        processed_value = value
    
    if isinstance(processed_value, str):
        value_length = len(processed_value)
        if (
            (value_length < APPLICATION_COMMAND_CHOICE_VALUE_LENGTH_MIN) or
            (value_length > APPLICATION_COMMAND_CHOICE_VALUE_LENGTH_MAX)
        ):
            raise ValueError(
                f'`value` length` can be in range '
                f'[{APPLICATION_COMMAND_CHOICE_VALUE_LENGTH_MIN}:{APPLICATION_COMMAND_CHOICE_VALUE_LENGTH_MAX}]'
                f'got {value_length!r}; {value!r}.'
            )
    
    elif isinstance(processed_value, int):
        # No extra checks
        pass
    
    elif isinstance(processed_value, float):
        # No extra checks
        pass
    
    else:
        raise TypeError(
            f'`value` type can be `str`, `int`, `float`, `{Enum.__name__}`, '
            f'got {value.__class__.__name__}; {value!r}.'
        )
    
    return processed_value
