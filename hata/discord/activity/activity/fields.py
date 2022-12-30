__all__ = ()

from ...field_parsers import preinstanced_parser_factory
from ...field_putters import preinstanced_putter_factory
from ...field_validators import preinstanced_validator_factory

from .preinstanced import ActivityType

# type

parse_type = preinstanced_parser_factory('type', ActivityType, ActivityType.game)
put_type_into = preinstanced_putter_factory('type')
validate_type = preinstanced_validator_factory('type', ActivityType)
