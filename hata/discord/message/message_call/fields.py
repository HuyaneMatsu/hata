__all__ = ()

from ...field_parsers import entity_id_array_parser_factory, nullable_date_time_parser_factory
from ...field_putters import nullable_date_time_optional_putter_factory, nullable_entity_id_array_putter_factory
from ...field_validators import entity_id_array_validator_factory, nullable_date_time_validator_factory
from ...user import ClientUserBase

# ended_at

parse_ended_at = nullable_date_time_parser_factory('ended_timestamp')
put_ended_at_into = nullable_date_time_optional_putter_factory('ended_timestamp')
validate_ended_at = nullable_date_time_validator_factory('ended_at')

# user_ids

parse_user_ids = entity_id_array_parser_factory('participants')
put_user_ids_into = nullable_entity_id_array_putter_factory('participants')
validate_user_ids = entity_id_array_validator_factory('user_ids', ClientUserBase)
