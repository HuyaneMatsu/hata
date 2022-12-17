__all__ = ()

from ...field_parsers import nullable_string_parser_factory, preinstanced_parser_factory
from ...field_putters import nullable_string_putter_factory, preinstanced_putter_factory
from ...field_validators import nullable_string_validator_factory, preinstanced_validator_factory

from .preinstanced import MessageActivityType

# party_id

parse_party_id = nullable_string_parser_factory('party_id')
put_party_id_into = nullable_string_putter_factory('party_id')
validate_party_id = nullable_string_validator_factory('party_id', 0, 1024)

# type

parse_type = preinstanced_parser_factory('type', MessageActivityType, MessageActivityType.none)
put_type_into = preinstanced_putter_factory('type')
validate_type = preinstanced_validator_factory('type', MessageActivityType)
