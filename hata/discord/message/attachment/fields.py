__all__ = ()

from ...field_parsers import (
    bool_parser_factory, entity_id_parser_factory, force_string_parser_factory, int_parser_factory,
    nullable_string_parser_factory
)
from ...field_putters import (
    bool_optional_putter_factory, entity_id_putter_factory, force_string_putter_factory, int_putter_factory,
    nullable_string_putter_factory, url_optional_putter_factory
)
from ...field_validators import (
    bool_validator_factory, entity_id_validator_factory, force_string_validator_factory,
    int_conditional_validator_factory, nullable_string_validator_factory, url_optional_validator_factory,
    url_required_validator_factory
)

from .constants import DESCRIPTION_LENGTH_MAX

# content_type

parse_content_type = nullable_string_parser_factory('content_type')
put_content_type_into = nullable_string_putter_factory('content_type')
validate_content_type = nullable_string_validator_factory('content_type', 0, 1024)

# description

parse_description = nullable_string_parser_factory('description')
put_description_into = nullable_string_putter_factory('description')
validate_description = nullable_string_validator_factory('description', 0, DESCRIPTION_LENGTH_MAX)

# height

parse_height = int_parser_factory('height', 0)
put_height_into = int_putter_factory('height')
validate_height = int_conditional_validator_factory(
    'height',
    0,
    lambda height : height >= 0,
    '>= 0',
)

# id

parse_id = entity_id_parser_factory('id')
put_id_into = entity_id_putter_factory('id')
validate_id = entity_id_validator_factory('id')

# name

parse_name = force_string_parser_factory('filename')
put_name_into = force_string_putter_factory('filename')
validate_name = force_string_validator_factory('name', 0, 1024)

# proxy_url

parse_proxy_url = nullable_string_parser_factory('proxy_url')
put_proxy_url_into = url_optional_putter_factory('proxy_url')
validate_proxy_url = url_optional_validator_factory('proxy_url')

# size

parse_size = int_parser_factory('size', 0)
put_size_into = int_putter_factory('size')
validate_size = int_conditional_validator_factory(
    'size',
    0,
    lambda size : size >= 0,
    '>= 0',
)

# temporary

parse_temporary = bool_parser_factory('ephemeral', False)
put_temporary_into = bool_optional_putter_factory('ephemeral', False)
validate_temporary = bool_validator_factory('temporary')

# url

parse_url = force_string_parser_factory('url')
put_url_into = url_optional_putter_factory('url')
validate_url = url_required_validator_factory('url')

# width

parse_width = int_parser_factory('width', 0)
put_width_into = int_putter_factory('width')
validate_width = int_conditional_validator_factory(
    'width',
    0,
    lambda width : width >= 0,
    '>= 0',
)
