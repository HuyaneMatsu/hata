__all__ = ()

from ...channel import Channel
from ...emoji import Emoji, create_partial_emoji_data, create_partial_emoji_from_data
from ...field_parsers import (
    entity_id_array_parser_factory, entity_id_parser_factory, force_string_parser_factory,
    nullable_functional_parser_factory, nullable_string_parser_factory
)
from ...field_putters import (
    entity_id_putter_factory, force_string_putter_factory, optional_entity_id_array_optional_putter_factory,
    nullable_functional_optional_putter_factory, nullable_string_putter_factory
)
from ...field_validators import (
    entity_id_array_validator_factory, entity_id_validator_factory, force_string_validator_factory,
    nullable_entity_validator_factory, nullable_string_validator_factory
)
from ...role import Role

# channel_ids

parse_channel_ids = entity_id_array_parser_factory('channel_ids')
put_channel_ids_into = optional_entity_id_array_optional_putter_factory('channel_ids')
validate_channel_ids = entity_id_array_validator_factory('channel_ids', Channel)

# description

parse_description = nullable_string_parser_factory('description')
put_description_into = nullable_string_putter_factory('description')
validate_description = nullable_string_validator_factory('description', 0, 1024)

# emoji

parse_emoji = nullable_functional_parser_factory('emoji', create_partial_emoji_from_data)
put_emoji_into = nullable_functional_optional_putter_factory('emoji', create_partial_emoji_data)
validate_emoji = nullable_entity_validator_factory('emoji', Emoji)

# id

parse_id = entity_id_parser_factory('id')
put_id_into = entity_id_putter_factory('id')
validate_id = entity_id_validator_factory('option_id')

# name

parse_name = force_string_parser_factory('title')
put_name_into = force_string_putter_factory('title')
validate_name = force_string_validator_factory('name', 0, 1024)

# role_ids

parse_role_ids = entity_id_array_parser_factory('role_ids')
put_role_ids_into = optional_entity_id_array_optional_putter_factory('role_ids')
validate_role_ids = entity_id_array_validator_factory('role_ids', Role)
