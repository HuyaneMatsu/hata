__all__ = ()

from ...field_parsers import nullable_string_parser_factory
from ...field_putters import nullable_string_putter_factory, url_optional_putter_factory
from ...field_validators import nullable_string_validator_factory, url_optional_validator_factory

from .constants import EMBED_AUTHOR_NAME_LENGTH_MAX

# icon_url

parse_icon_url = nullable_string_parser_factory('icon_url')
put_icon_url_into = url_optional_putter_factory('icon_url')
# url validator doesnt allow attachment:\\image.png formats
validate_icon_url = nullable_string_validator_factory('icon_url', 0, 16384)

# icon_proxy_url

parse_icon_proxy_url = nullable_string_parser_factory('proxy_icon_url')
put_icon_proxy_url_into = url_optional_putter_factory('proxy_icon_url')
validate_icon_proxy_url = url_optional_validator_factory('icon_proxy_url')

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
    
    if name_length > EMBED_AUTHOR_NAME_LENGTH_MAX:
        raise ValueError(
            f'`name` length` must be <= {EMBED_AUTHOR_NAME_LENGTH_MAX}, got {name_length}; name = {name!r}.'
        )
    
    return name

# url

parse_url = nullable_string_parser_factory('url')
put_url_into = url_optional_putter_factory('url')
validate_url = url_optional_validator_factory('url')
