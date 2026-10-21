__all__ = ()

from ...fields.field_parsers import nullable_string_parser_factory
from ...fields.field_putters import nullable_string_putter_factory
from ...fields.field_validators import nullable_string_validator_factory

from .constants import TEXT_LENGTH_MAX


# text

parse_text = nullable_string_parser_factory('text')
put_text = nullable_string_putter_factory('text')
validate_text = nullable_string_validator_factory('text', 0, TEXT_LENGTH_MAX)
