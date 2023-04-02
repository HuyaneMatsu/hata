__all__ = ()

from ...field_parsers import bool_parser_factory, nullable_string_parser_factory
from ...field_putters import bool_optional_putter_factory, nullable_string_putter_factory
from ...field_validators import bool_validator_factory

from .constants import EMBED_FIELD_NAME_LENGTH_MAX, EMBED_FIELD_VALUE_LENGTH_MAX


# inline

parse_inline = bool_parser_factory('inline', False)
put_inline_into = bool_optional_putter_factory('inline', False)
validate_inline = bool_validator_factory('inline', False)


# name

parse_name = nullable_string_parser_factory('name')
put_name_into = nullable_string_putter_factory('name')


def validate_name(name):
    """
    Validates the given embed author name.
    
    Parameters
    ----------
    name : `None`, `str`, `object`
        Embed author name.
    
    Returns
    -------
    name : `None`, `str`
    
    Raises
    ------
    TypeError
        - If `name`'s type is incorrect.
    ValueError
        - If `name`'s length is out of the expected range.
    """
    if name is None:
        return None
    
    if not isinstance(name, str):
        name = str(name)
    
    name_length = len(name)
    if name_length == 0:
        return None
    
    if name_length > EMBED_FIELD_NAME_LENGTH_MAX:
        raise ValueError(
            f'`name` length` must be <= {EMBED_FIELD_NAME_LENGTH_MAX}, got {name_length}; name = {name!r}.'
        )
    
    return name

# value

parse_value = nullable_string_parser_factory('value')
put_value_into = nullable_string_putter_factory('value')


def validate_value(value):
    """
    Validates the given embed author value.
    
    Parameters
    ----------
    value : `None`, `str`, `object`
        Embed author value.
    
    Returns
    -------
    value : `None`, `str`
    
    Raises
    ------
    TypeError
        - If `value`'s type is incorrect.
    ValueError
        - If `value`'s length is out of the expected range.
    """
    if value is None:
        return None
    
    if not isinstance(value, str):
        value = str(value)
    
    value_length = len(value)
    if value_length == 0:
        return None
    
    if value_length > EMBED_FIELD_VALUE_LENGTH_MAX:
        raise ValueError(
            f'`value` length` must be <= {EMBED_FIELD_VALUE_LENGTH_MAX}, got {value_length}; value = {value!r}.'
        )
    
    return value
