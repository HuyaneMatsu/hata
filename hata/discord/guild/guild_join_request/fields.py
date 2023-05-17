__all__ = ()

from ...field_parsers import (
    default_entity_parser_factory, entity_id_parser_factory, nullable_date_time_parser_factory,
    nullable_entity_parser_factory, nullable_object_array_parser_factory, nullable_string_parser_factory,
    preinstanced_parser_factory
)
from ...field_putters import (
    entity_id_putter_factory, entity_putter_factory, nullable_date_time_optional_putter_factory,
    nullable_entity_optional_putter_factory, nullable_object_array_optional_putter_factory, preinstanced_putter_factory,
    url_optional_putter_factory
)
from ...field_validators import (
    default_entity_validator, entity_id_validator_factory, nullable_date_time_validator_factory,
    nullable_entity_validator_factory, nullable_object_array_validator_factory, nullable_string_validator_factory,
    preinstanced_validator_factory
)
from ...user import ClientUserBase, User, ZEROUSER

from ..guild import Guild
from ..guild_join_request_form_response import GuildJoinRequestFormResponse

from .preinstanced import GuildJoinRequestStatus

# actioned_at

parse_actioned_at = nullable_date_time_parser_factory('actioned_at')
put_actioned_at_into = nullable_date_time_optional_putter_factory('actioned_at')
validate_actioned_at = nullable_date_time_validator_factory('actioned_at')

# actioned_by

parse_actioned_by = nullable_entity_parser_factory('actioned_by_user', User)
put_actioned_by_into = nullable_entity_optional_putter_factory('actioned_by_user', User, force_include_internals = True)
validate_actioned_by = nullable_entity_validator_factory('actioned_by', ClientUserBase)

# created_at

parse_created_at = nullable_date_time_parser_factory('created_at')
put_created_at_into = nullable_date_time_optional_putter_factory('created_at')
validate_created_at = nullable_date_time_validator_factory('created_at')

# form_responses

parse_form_responses = nullable_object_array_parser_factory('form_responses', GuildJoinRequestFormResponse)
put_form_responses_into = nullable_object_array_optional_putter_factory('form_responses')
validate_form_responses = nullable_object_array_validator_factory('form_responses', GuildJoinRequestFormResponse)

# guild_id

parse_guild_id = entity_id_parser_factory('guild_id')
put_guild_id_into = entity_id_putter_factory('guild_id')
validate_guild_id = entity_id_validator_factory('guild_id', Guild)

# last_seen_at

parse_last_seen_at = nullable_date_time_parser_factory('last_seen')
put_last_seen_at_into = nullable_date_time_optional_putter_factory('last_seen')
validate_last_seen_at = nullable_date_time_validator_factory('last_seen')

# rejection_reason

parse_rejection_reason = nullable_string_parser_factory('rejection_reason')
put_rejection_reason_into = url_optional_putter_factory('rejection_reason')
validate_rejection_reason = nullable_string_validator_factory('rejection_reason', 0, 1024)

# status

parse_status = preinstanced_parser_factory('application_status', GuildJoinRequestStatus, GuildJoinRequestStatus.started)
put_status_into = preinstanced_putter_factory('application_status')
validate_status = preinstanced_validator_factory('application_status', GuildJoinRequestStatus)

# user

parse_user = default_entity_parser_factory('user', User, default = ZEROUSER)
put_user_into = entity_putter_factory('user', ClientUserBase, force_include_internals = True)
validate_user = default_entity_validator('user', ClientUserBase, default = ZEROUSER)

# user_id

put_user_id_into = entity_id_putter_factory('user_id')
