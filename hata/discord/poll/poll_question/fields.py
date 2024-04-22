__all__ = ()

from ...field_parsers import nullable_string_parser_factory
from ...field_putters import nullable_string_putter_factory
from ...field_validators import nullable_string_validator_factory

from .constants import TEXT_LENGTH_MAX


# text

parse_text = nullable_string_parser_factory('text')
put_text_into = nullable_string_putter_factory('text')
validate_text = nullable_string_validator_factory('text', 0, TEXT_LENGTH_MAX)
