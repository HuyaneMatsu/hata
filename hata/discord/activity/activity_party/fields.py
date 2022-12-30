__all__ = ()

from ...field_parsers import nullable_string_parser_factory
from ...field_putters import nullable_string_optional_putter_factory
from ...field_validators import int_conditional_validator_factory, nullable_string_validator_factory

# id

parse_id = nullable_string_parser_factory('id')
put_id_into = nullable_string_optional_putter_factory('id')
validate_id = nullable_string_validator_factory('party_id', 0, 1024)

# size # max

def parse_size_and_max(data):
    """
    Parses out the (current) size and the max (size) fields from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `object`) items
        Activity party data.
    
    Returns
    -------
    size : `int`
    max_ : `int`
    """
    return data.get('size', (0, 0))


def put_size_and_max_into(size_and_max, data, defaults):
    """
    Puts the given size and max value pair into the given data.
    
    Parameters
    ----------
    size_and_max : `tuple` (`int`, `int`)
        Size and max pair.
    data : `dict` of (`str`, `object`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `object`) items
    """
    if defaults or any(size_and_max):
        data['size'] = size_and_max
    return data

# size

validate_size = int_conditional_validator_factory(
    'size',
    0,
    lambda size : size >= 0,
    '>= 0',
)

# max

validate_max = int_conditional_validator_factory(
    'max',
    0,
    lambda max_ : max_ >= 0,
    '>= 0',
)
