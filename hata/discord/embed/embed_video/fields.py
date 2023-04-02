__all__ = ()

from ...field_parsers import int_parser_factory, nullable_string_parser_factory
from ...field_putters import int_putter_factory, url_optional_putter_factory
from ...field_validators import (
    int_conditional_validator_factory, nullable_string_validator_factory, url_optional_validator_factory
)

# height

parse_height = int_parser_factory('height', 0)
put_height_into = int_putter_factory('height')
validate_height = int_conditional_validator_factory(
    'height',
    0,
    lambda height : height >= 0,
    '>= 0',
)

# url

parse_url = nullable_string_parser_factory('url')
put_url_into = url_optional_putter_factory('url')
# url validator doesnt allow attachment:\\image.png formats
validate_url = nullable_string_validator_factory('url', 0, 16384)

# proxy_url

parse_proxy_url = nullable_string_parser_factory('proxy_url')
put_proxy_url_into = url_optional_putter_factory('proxy_url')
validate_proxy_url = url_optional_validator_factory('proxy_url')

# width

parse_width = int_parser_factory('width', 0)
put_width_into = int_putter_factory('width')
validate_width = int_conditional_validator_factory(
    'width',
    0,
    lambda width : width >= 0,
    '>= 0',
)
