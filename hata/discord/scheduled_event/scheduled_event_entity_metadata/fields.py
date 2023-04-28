__all__ = ()

from ...field_parsers import entity_id_array_parser_factory, nullable_string_parser_factory
from ...field_putters import optional_entity_id_array_optional_putter_factory, nullable_string_putter_factory
from ...field_validators import entity_id_array_validator_factory, nullable_string_validator_factory
from ...user import ClientUserBase

# location

parse_location = nullable_string_parser_factory('location')
put_location_into = nullable_string_putter_factory('location')
validate_location = nullable_string_validator_factory('location', 0, 1024)

# speaker_ids

parse_speaker_ids = entity_id_array_parser_factory('speaker_ids')
put_speaker_ids_into = optional_entity_id_array_optional_putter_factory('speaker_ids')
validate_speaker_ids = entity_id_array_validator_factory('speaker_ids', ClientUserBase)
