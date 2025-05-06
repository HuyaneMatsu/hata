__all__ = ()

from ...field_parsers import bool_parser_factory, entity_id_parser_factory, force_string_parser_factory
from ...field_putters import entity_id_putter_factory, force_bool_putter_factory, force_string_putter_factory
from ...field_validators import bool_validator_factory, entity_id_validator_factory, force_string_validator_factory

from ..guild import Guild

from .constants import BADGE_TAG_LENGTH_MAX, BADGE_TAG_LENGTH_MIN

# enabled

parse_enabled = bool_parser_factory('identity_enabled', True)
put_enabled = force_bool_putter_factory('identity_enabled')
validate_enabled = bool_validator_factory('enabled', True)

# guild_id

parse_guild_id = entity_id_parser_factory('identity_guild_id')
put_guild_id = entity_id_putter_factory('identity_guild_id')
validate_guild_id = entity_id_validator_factory('guild_id', Guild)

# tag

parse_tag = force_string_parser_factory('tag')
put_tag = force_string_putter_factory('tag')
validate_tag = force_string_validator_factory('tag', BADGE_TAG_LENGTH_MIN, BADGE_TAG_LENGTH_MAX)
