__all__ = ()

from ...field_parsers import flag_parser_factory, int_parser_factory, nullable_string_parser_factory
from ...field_putters import flag_optional_putter_factory, int_putter_factory, url_optional_putter_factory
from ...field_validators import (
    flag_validator_factory, int_conditional_validator_factory, nullable_string_validator_factory,
    url_optional_validator_factory
)

from ..embed_field_base import EmbedMediaFlag

from .constants import URL_LENGTH_MAX


# flags

parse_flags = flag_parser_factory('flags', EmbedMediaFlag)
put_flags = flag_optional_putter_factory('flags', EmbedMediaFlag())
validate_flags = flag_validator_factory('flags', EmbedMediaFlag)


# height

parse_height = int_parser_factory('height', 0)
put_height = int_putter_factory('height')
validate_height = int_conditional_validator_factory(
    'height',
    0,
    lambda height : height >= 0,
    '>= 0',
)

# icon_proxy_url

parse_proxy_url = nullable_string_parser_factory('proxy_url')
put_proxy_url = url_optional_putter_factory('proxy_url')
validate_proxy_url = url_optional_validator_factory('proxy_url')


# url

parse_url = nullable_string_parser_factory('url')
put_url = url_optional_putter_factory('url')
# url validator doesnt allow attachment:\\image.png formats
validate_url = nullable_string_validator_factory('url', 0, URL_LENGTH_MAX)

# width

parse_width = int_parser_factory('width', 0)
put_width = int_putter_factory('width')
validate_width = int_conditional_validator_factory(
    'width',
    0,
    lambda width : width >= 0,
    '>= 0',
)
