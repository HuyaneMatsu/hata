__all__ = ()

from ...field_parsers import nullable_string_parser_factory
from ...field_putters import nullable_string_optional_putter_factory
from ...field_validators import nullable_string_validator_factory

# join

parse_join = nullable_string_parser_factory('join')
put_join_into = nullable_string_optional_putter_factory('join')
validate_join = nullable_string_validator_factory('join', 0, 1024)

# match

parse_match = nullable_string_parser_factory('match')
put_match_into = nullable_string_optional_putter_factory('match')
validate_match = nullable_string_validator_factory('match', 0, 1024)

# spectate

parse_spectate = nullable_string_parser_factory('spectate')
put_spectate_into = nullable_string_optional_putter_factory('spectate')
validate_spectate = nullable_string_validator_factory('spectate', 0, 1024)
