__all__ = ()

from ...field_parsers import (
    bool_parser_factory, entity_id_array_parser_factory, flag_parser_factory, nullable_date_time_parser_factory,
    nullable_entity_parser_factory, nullable_string_parser_factory
)
from ...field_putters import (
    bool_optional_putter_factory, flag_optional_putter_factory, nullable_date_time_optional_putter_factory,
    optional_entity_id_array_optional_putter_factory, nullable_entity_optional_putter_factory,
    nullable_string_optional_putter_factory
)
from ...field_validators import (
    bool_validator_factory, duration_validator_factory, flag_validator_factory, entity_id_array_validator_factory,
    nullable_date_time_validator_factory, nullable_entity_validator_factory, nullable_string_validator_factory
)

from ..avatar_decoration import AvatarDecoration

from .constants import NICK_LENGTH_MAX, NICK_LENGTH_MIN
from .flags import GuildProfileFlag

# avatar_decoration

parse_avatar_decoration = nullable_entity_parser_factory('avatar_decoration_data', AvatarDecoration)
put_avatar_decoration = nullable_entity_optional_putter_factory('avatar_decoration_data', AvatarDecoration)
validate_avatar_decoration = nullable_entity_validator_factory('avatar_decoration', AvatarDecoration)

# boosts_since

parse_boosts_since = nullable_date_time_parser_factory('premium_since')
put_boosts_since = nullable_date_time_optional_putter_factory('premium_since')
validate_boosts_since = nullable_date_time_validator_factory('boosts_since')

# bypasses_verification | required for audit logs

validate_bypasses_verification = bool_validator_factory('bypasses_verification', False)

# flags

parse_flags = flag_parser_factory('flags', GuildProfileFlag)
put_flags = flag_optional_putter_factory('flags', GuildProfileFlag())
validate_flags = flag_validator_factory('flags', GuildProfileFlag)

# joined_at

parse_joined_at = nullable_date_time_parser_factory('joined_at')
put_joined_at = nullable_date_time_optional_putter_factory('joined_at')
validate_joined_at = nullable_date_time_validator_factory('joined_at')

# nick

parse_nick = nullable_string_parser_factory('nick')
put_nick = nullable_string_optional_putter_factory('nick')
validate_nick = nullable_string_validator_factory('nick', NICK_LENGTH_MIN, NICK_LENGTH_MAX)

# pending

parse_pending = bool_parser_factory('pending', False)
put_pending = bool_optional_putter_factory('pending', False)
validate_pending = bool_validator_factory('pending', False)

# role_ids

parse_role_ids = entity_id_array_parser_factory('roles')
put_role_ids = optional_entity_id_array_optional_putter_factory('roles')
validate_role_ids = entity_id_array_validator_factory('role_ids', NotImplemented, include = 'Role')

# timeout_duration

validate_timeout_duration = duration_validator_factory('timeout_duration')

# timed_out_until

parse_timed_out_until = nullable_date_time_parser_factory('communication_disabled_until')
put_timed_out_until = nullable_date_time_optional_putter_factory('communication_disabled_until')
validate_timed_out_until = nullable_date_time_validator_factory('timed_out_until')
