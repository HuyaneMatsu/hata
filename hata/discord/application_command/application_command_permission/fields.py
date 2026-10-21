__all__ = ()

from ...application import Application
from ...fields.field_parsers import entity_id_parser_factory, nullable_entity_array_parser_factory
from ...fields.field_putters import entity_id_putter_factory, nullable_entity_array_putter_factory
from ...fields.field_validators import entity_id_validator_factory, nullable_entity_array_validator_factory
from ...fields.fields_common import parse_guild_id, put_guild_id, validate_guild_id

from ..application_command import ApplicationCommand
from ..application_command_permission_overwrite import ApplicationCommandPermissionOverwrite

# application_command_id

parse_application_command_id = entity_id_parser_factory('id')
put_application_command_id = entity_id_putter_factory('id')
validate_application_command_id = entity_id_validator_factory(
    'application_command_id', ApplicationCommand
)

# application_id

parse_application_id = entity_id_parser_factory('application_id')
put_application_id = entity_id_putter_factory('application_id')
validate_application_id = entity_id_validator_factory('application_id', Application)

# permission_overwrites

parse_permission_overwrites = nullable_entity_array_parser_factory('permissions', ApplicationCommandPermissionOverwrite)
put_permission_overwrites = nullable_entity_array_putter_factory(
    'permissions', ApplicationCommandPermissionOverwrite
)
validate_permission_overwrites = nullable_entity_array_validator_factory(
    'permission_overwrites', ApplicationCommandPermissionOverwrite
)
