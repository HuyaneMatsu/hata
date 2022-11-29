__all__ = ()

from ...field_parsers import entity_id_parser_factory, force_string_parser_factory, nullable_string_parser_factory
from ...field_putters import entity_id_putter_factory, force_string_putter_factory, nullable_string_putter_factory
from ...field_validators import (
    entity_id_validator_factory, force_string_validator_factory, nullable_string_validator_factory
)

from .constants import CONTENT_LENGTH_MAX, CONTENT_LENGTH_MIN, NAME_LENGTH_MAX, NAME_LENGTH_MIN

# content

parse_content = nullable_string_parser_factory('content')
put_content_into = nullable_string_putter_factory('content')
validate_content = nullable_string_validator_factory('content', CONTENT_LENGTH_MIN, CONTENT_LENGTH_MAX)

# id

parse_id = entity_id_parser_factory('id')
put_id_into = entity_id_putter_factory('id')
validate_id = entity_id_validator_factory('team_id')

# name

parse_name = force_string_parser_factory('name')
put_name_into = force_string_putter_factory('name')
validate_name = force_string_validator_factory('name', NAME_LENGTH_MIN, NAME_LENGTH_MAX)
