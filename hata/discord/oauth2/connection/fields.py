__all__ = ()

from ...field_parsers import (
    bool_parser_factory, entity_id_parser_factory, force_string_parser_factory, nullable_entity_array_parser_factory,
    preinstanced_parser_factory
)
from ...field_putters import (
    bool_optional_putter_factory, entity_id_putter_factory, force_string_putter_factory,
    nullable_entity_array_putter_factory, preinstanced_optional_putter_factory, preinstanced_putter_factory
)
from ...field_validators import (
    bool_validator_factory, entity_id_validator_factory, force_string_validator_factory,
    nullable_entity_array_validator_factory, preinstanced_validator_factory
)

from .constants import NAME_LENGTH_MAX, NAME_LENGTH_MIN
from .preinstanced import ConnectionType, ConnectionVisibility


# parse_friend_sync

parse_friend_sync = bool_parser_factory('friend_sync', False)
put_friend_sync_into = bool_optional_putter_factory('friend_sync', False)
validate_friend_sync = bool_validator_factory('friend_sync', False)

# id

parse_id = entity_id_parser_factory('id')
put_id_into = entity_id_putter_factory('id')
validate_id = entity_id_validator_factory('connection_id')

# integrations

parse_integrations = nullable_entity_array_parser_factory('integrations', NotImplemented, include = 'Integration')
put_integrations_into = nullable_entity_array_putter_factory(
    'integrations', NotImplemented, can_include_internals = True, include = 'Integration'
)
validate_integrations = nullable_entity_array_validator_factory('integrations', NotImplemented, include = 'Integration')

# metadata_visibility

parse_metadata_visibility = preinstanced_parser_factory(
    'metadata_visibility', ConnectionVisibility, ConnectionVisibility.user_only
)
put_metadata_visibility_into = preinstanced_optional_putter_factory(
    'metadata_visibility', ConnectionVisibility.user_only
)
validate_metadata_visibility = preinstanced_validator_factory('metadata_visibility', ConnectionVisibility)

# name

parse_name = force_string_parser_factory('name')
put_name_into = force_string_putter_factory('name')
validate_name = force_string_validator_factory('name', NAME_LENGTH_MIN, NAME_LENGTH_MAX)

# revoked

parse_revoked = bool_parser_factory('revoked', False)
put_revoked_into = bool_optional_putter_factory('revoked', False)
validate_revoked = bool_validator_factory('revoked', False)

# show_activity

parse_show_activity = bool_parser_factory('show_activity', False)
put_show_activity_into = bool_optional_putter_factory('show_activity', False)
validate_show_activity = bool_validator_factory('show_activity', False)

# two_way_link

parse_two_way_link = bool_parser_factory('two_way_link', False)
put_two_way_link_into = bool_optional_putter_factory('two_way_link', False)
validate_two_way_link = bool_validator_factory('two_way_link', False)

# type

parse_type = preinstanced_parser_factory('type', ConnectionType, ConnectionType.unknown)
put_type_into = preinstanced_putter_factory('type')
validate_type = preinstanced_validator_factory('type', ConnectionType)

# verified

parse_verified = bool_parser_factory('verified', False)
put_verified_into = bool_optional_putter_factory('verified', False)
validate_verified = bool_validator_factory('verified', False)

# visibility

parse_visibility = preinstanced_parser_factory('visibility', ConnectionVisibility, ConnectionVisibility.user_only)
put_visibility_into = preinstanced_optional_putter_factory('visibility', ConnectionVisibility.user_only)
validate_visibility = preinstanced_validator_factory('visibility', ConnectionVisibility)
