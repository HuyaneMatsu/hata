__all__ = ()

from ...fields.field_parsers import nullable_functional_parser_factory, preinstanced_parser_factory
from ...fields.field_putters import nullable_functional_putter_factory_with_defaults, preinstanced_putter_factory
from ...fields.field_validators import nullable_entity_validator_factory, preinstanced_validator_factory
from ...fields.fields_common import parse_guild_id, put_guild_id, validate_guild_id

from ..guild_join_request import (
    GuildJoinRequest, GuildJoinRequestStatus, guild_join_request_convert_to_data, guild_join_request_create_from_data
)


# status

parse_status = preinstanced_parser_factory('status', GuildJoinRequestStatus, GuildJoinRequestStatus.started)
put_status = preinstanced_putter_factory('status')
validate_status = preinstanced_validator_factory('status', GuildJoinRequestStatus)


# guild_join_request

parse_guild_join_request = nullable_functional_parser_factory('request', guild_join_request_create_from_data)
put_guild_join_request = nullable_functional_putter_factory_with_defaults('request', guild_join_request_convert_to_data)
validate_guild_join_request = nullable_entity_validator_factory('guild_join_request', GuildJoinRequest)
