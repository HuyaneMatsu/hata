__all__ = ()

from ...channel import Channel
from ...field_parsers import entity_id_parser_factory, preinstanced_parser_factory
from ...field_putters import entity_id_optional_putter_factory, preinstanced_putter_factory
from ...field_validators import entity_id_validator_factory, preinstanced_validator_factory

from .preinstanced import EmbeddedActivityLocationType


# channel_id

parse_channel_id = entity_id_parser_factory('channel_id')
put_channel_id_into = entity_id_optional_putter_factory('channel_id')
validate_channel_id = entity_id_validator_factory('channel_id', Channel)


# guild_id

parse_guild_id = entity_id_parser_factory('guild_id')
put_guild_id_into = entity_id_optional_putter_factory('guild_id')
validate_guild_id = entity_id_validator_factory('guild_id', NotImplemented, include = 'Guild')


# type

parse_type = preinstanced_parser_factory('kind', EmbeddedActivityLocationType, EmbeddedActivityLocationType.none)
put_type_into = preinstanced_putter_factory('kind')
validate_type = preinstanced_validator_factory('type', EmbeddedActivityLocationType)
