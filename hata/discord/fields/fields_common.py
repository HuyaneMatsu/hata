__all__ = ()

from .field_parsers import bool_parser_factory, entity_id_parser_factory, nullable_string_parser_factory
from .field_putters import (
    bool_optional_putter_factory, entity_id_optional_putter_factory, entity_id_putter_factory,
    force_bool_putter_factory, nullable_string_optional_putter_factory, nullable_string_putter_factory
)
from .field_validators import bool_validator_factory, entity_id_validator_factory, nullable_string_validator_factory


# guild_id

parse_guild_id = entity_id_parser_factory('guild_id')
put_guild_id = entity_id_putter_factory('guild_id')
put_guild_id__optional = entity_id_optional_putter_factory('guild_id')
validate_guild_id = entity_id_validator_factory('guild_id')


# user_id

parse_user_id = entity_id_parser_factory('user_id')
put_user_id = entity_id_putter_factory('user_id')
put_user_id__optional = entity_id_optional_putter_factory('user_id')
validate_user_id = entity_id_validator_factory('user_id')


# title

parse_title = nullable_string_parser_factory('title')
parse_title__from_label = nullable_string_parser_factory('label')
put_title__optional = nullable_string_optional_putter_factory('title')
put_title__to_label = nullable_string_putter_factory('label')
validate_title__range_0_1024 = nullable_string_validator_factory('title', 0, 1024)


# description

parse_description = nullable_string_parser_factory('description')
put_description = nullable_string_putter_factory('description')
put_description__optional = nullable_string_optional_putter_factory('description')
validate_description__range_0_1024 = nullable_string_validator_factory('description', 0, 1024)


# placeholder

parse_placeholder = nullable_string_parser_factory('placeholder')
put_placeholder__optional = nullable_string_optional_putter_factory('placeholder')
validate_placeholder__range_0_1024 = nullable_string_validator_factory('placeholder', 0, 1024)


# required

parse_required = bool_parser_factory('required', False)
put_required = force_bool_putter_factory('required')
put_required__optional = bool_optional_putter_factory('required', False)
validate_required = bool_validator_factory('required', False)
