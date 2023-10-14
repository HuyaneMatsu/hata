__all__ = ()

from ...field_parsers import entity_id_parser_factory, preinstanced_parser_factory
from ...field_putters import entity_id_putter_factory, preinstanced_putter_factory
from ...field_validators import entity_id_validator_factory, preinstanced_validator_factory

from .preinstanced import EntitySelectDefaultValueType

# id

parse_id = entity_id_parser_factory('id')
put_id_into = entity_id_putter_factory('id')
validate_id = entity_id_validator_factory('entity_id')

# type

parse_type = preinstanced_parser_factory('type', EntitySelectDefaultValueType, EntitySelectDefaultValueType.none)
put_type_into = preinstanced_putter_factory('type')
validate_type = preinstanced_validator_factory('option_type', EntitySelectDefaultValueType)
