__all__ = ()

from ...fields.field_parsers import preinstanced_parser_factory
from ...fields.field_putters import preinstanced_putter_factory
from ...fields.field_validators import preinstanced_validator_factory

from .preinstanced import ActivityType

# type

parse_type = preinstanced_parser_factory('type', ActivityType, ActivityType.playing)
put_type = preinstanced_putter_factory('type')
validate_type = preinstanced_validator_factory('type', ActivityType)
