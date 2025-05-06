__all__ = ()

from ...field_parsers import force_string_parser_factory, int_parser_factory,  nullable_string_parser_factory
from ...field_putters import int_putter_factory, nullable_string_putter_factory, url_optional_putter_factory
from ...field_validators import (
    force_string_validator_factory, int_conditional_validator_factory, nullable_string_validator_factory,
    url_optional_validator_factory
)

# content_type

parse_content_type = nullable_string_parser_factory('content_type')
put_content_type = nullable_string_putter_factory('content_type')
validate_content_type = nullable_string_validator_factory('content_type', 0, 1024)


# height

parse_height = int_parser_factory('height', 0)
put_height = int_putter_factory('height')
validate_height = int_conditional_validator_factory(
    'height',
    0,
    lambda height : height >= 0,
    '>= 0',
)


# proxy_url

parse_proxy_url = nullable_string_parser_factory('proxy_url')
put_proxy_url = url_optional_putter_factory('proxy_url')
validate_proxy_url = url_optional_validator_factory('proxy_url')


# url

parse_url = force_string_parser_factory('url')
put_url = url_optional_putter_factory('url')
validate_url = force_string_validator_factory('url', 0, 1024)


# width

parse_width = int_parser_factory('width', 0)
put_width = int_putter_factory('width')
validate_width = int_conditional_validator_factory(
    'width',
    0,
    lambda width : width >= 0,
    '>= 0',
)
