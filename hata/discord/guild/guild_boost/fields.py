__all__ = ()

from ...field_parsers import bool_parser_factory, entity_id_parser_factory, nullable_date_time_parser_factory
from ...field_putters import (
    bool_optional_putter_factory, entity_id_putter_factory, nullable_date_time_optional_putter_factory
)
from ...field_validators import bool_validator_factory, entity_id_validator_factory, nullable_date_time_validator_factory
from ...user import ClientUserBase

from ..guild import Guild


# ended

parse_ended = bool_parser_factory('ended', False)
put_ended = bool_optional_putter_factory('ended', False)
validate_ended = bool_validator_factory('ended', False)


# ends_at

parse_ends_at = nullable_date_time_parser_factory('ends_at')
put_ends_at = nullable_date_time_optional_putter_factory('ends_at')
validate_ends_at = nullable_date_time_validator_factory('ends_at')


# guild_id

parse_guild_id = entity_id_parser_factory('guild_id')
put_guild_id = entity_id_putter_factory('guild_id')
validate_guild_id = entity_id_validator_factory('guild_id', Guild)


# id

parse_id = entity_id_parser_factory('id')
put_id = entity_id_putter_factory('id')
validate_id = entity_id_validator_factory('guild_boost_id')


# paused_until

parse_paused_until = nullable_date_time_parser_factory('pause_ends_at')
put_paused_until = nullable_date_time_optional_putter_factory('pause_ends_at')
validate_paused_until = nullable_date_time_validator_factory('paused_until')


# user_id

parse_user_id = entity_id_parser_factory('user_id')
put_user_id = entity_id_putter_factory('user_id')
validate_user_id = entity_id_validator_factory('user_id', ClientUserBase)
