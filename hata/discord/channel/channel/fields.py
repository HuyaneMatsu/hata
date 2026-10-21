__all__ = ()

from ...fields.field_parsers import entity_id_parser_factory, preinstanced_parser_factory
from ...fields.field_putters import entity_id_putter_factory, preinstanced_putter_factory
from ...fields.field_validators import entity_id_validator_factory, preinstanced_validator_factory
from ...fields.fields_common import parse_guild_id, put_guild_id, validate_guild_id

from .preinstanced import ChannelType


# id

parse_id = entity_id_parser_factory('id')
put_id = entity_id_putter_factory('id')
validate_id = entity_id_validator_factory('channel_id')

# type

parse_type = preinstanced_parser_factory('type', ChannelType, ChannelType.unknown)
put_type = preinstanced_putter_factory('type')
validate_type = preinstanced_validator_factory('channel_type', ChannelType)
