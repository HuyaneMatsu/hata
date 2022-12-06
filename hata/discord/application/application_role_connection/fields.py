__all__ = ()

from ...field_parsers import nullable_string_parser_factory
from ...field_putters import nullable_string_putter_factory
from ...field_validators import nullable_string_validator_factory

from .constants import PLATFORM_NAME_LENGTH_MIN, PLATFORM_NAME_LENGTH_MAX, PLATFORM_USER_NAME_LENGTH_MIN, \
    PLATFORM_USER_NAME_LENGTH_MAX

# platform_name

parse_platform_name = nullable_string_parser_factory('platform_name')
put_platform_name_into = nullable_string_putter_factory('platform_name')
validate_platform_name = nullable_string_validator_factory(
    'platform_name', PLATFORM_NAME_LENGTH_MIN, PLATFORM_NAME_LENGTH_MAX
)


# platform_user_name

parse_platform_user_name = nullable_string_parser_factory('platform_username')
put_platform_user_name_into = nullable_string_putter_factory('platform_username')
validate_platform_user_name = nullable_string_validator_factory(
    'platform_username', PLATFORM_USER_NAME_LENGTH_MIN, PLATFORM_USER_NAME_LENGTH_MAX
)

# metadata_values

def parse_metadata_values(data):
    """
    Parsers out metadata values from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `object`) items
        Application role connection data.
    
    Returns
    -------
    metadata_values : `None`, `dict` of (`str`, `str`) items
    """
    metadata_values = data.get('metadata', None)
    if (metadata_values is not None) and metadata_values:
        return metadata_values


def put_metadata_values_into(metadata_values, data, defaults):
    """
    Puts the application role connection metadata values into the given data.
    
    Parameters
    ----------
    metadata_values : `None`, `dict` of (`str`, `str`) items
        Metadata values.
    data : `dict` of (`str`, `object`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `object`) items
    """
    if defaults or (metadata_values is not None):
        if metadata_values is None:
            metadata_values = {}
        
        data['metadata'] = metadata_values
    
    return data


def validate_metadata_values(metadata_values):
    """
    Validates the given application role connection metadata values.
    
    Parameters
    ----------
    metadata_values : `None`, `dict` of (`str`, `str`) items
        Metadata values.
    
    Returns
    -------
    metadata_values : `None`, `dict` of (`str`, `str`) items
        Metadata values.
    
    TypeError
        - If `metadata_values`'s type or structure is incorrect.
    """
    if metadata_values is None:
        return None
    
    if not isinstance(metadata_values, dict):
        raise TypeError(
            f'`metadata_values` can be `dict`, got {metadata_values.__class__.__name__}; {metadata_values!r}.'
        )
    
    if not metadata_values:
        return None
    
    for key, value in metadata_values.items():
        if not isinstance(key, str):
            raise TypeError(
                f'`metadata_values` keys can be `str`, got {key.__class__.__name__}; {key!r}, '
                f'metadata_values = {metadata_values!r}.'
            )
        
        if not isinstance(value, str):
            raise TypeError(
                f'`metadata_values` values can be `str`, got {value.__class__.__name__}; {value!r}, '
                f'metadata_values = {metadata_values!r}.'
            )
    
    return metadata_values
