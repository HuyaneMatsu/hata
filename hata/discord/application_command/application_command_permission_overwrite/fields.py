__all__ = ()

from ...field_parsers import bool_parser_factory, entity_id_parser_factory, preinstanced_parser_factory
from ...field_putters import entity_id_putter_factory, force_bool_putter_factory, preinstanced_putter_factory
from ...field_validators import bool_validator_factory, entity_id_validator_factory, preinstanced_validator_factory

from .preinstanced import ApplicationCommandPermissionOverwriteTargetType


# allow

parse_allow = bool_parser_factory('permission', True)
put_allow_into = force_bool_putter_factory('permission')
validate_allow = bool_validator_factory('allow', True)

# target_id

parse_target_id = entity_id_parser_factory('id')
put_target_id_into = entity_id_putter_factory('id')
validate_target_id = entity_id_validator_factory('target_id')

# target_type

parse_target_type = preinstanced_parser_factory(
    'type', ApplicationCommandPermissionOverwriteTargetType, ApplicationCommandPermissionOverwriteTargetType.none
)
put_target_type_into = preinstanced_putter_factory('type')
validate_target_type = preinstanced_validator_factory('target_type', ApplicationCommandPermissionOverwriteTargetType)
