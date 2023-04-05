__all__ = ()

from ...emoji import Emoji, create_partial_emoji_data, create_partial_emoji_from_data
from ...field_parsers import entity_id_parser_factory, nullable_functional_parser_factory, preinstanced_parser_factory
from ...field_putters import (
    entity_id_putter_factory, nullable_functional_optional_putter_factory, preinstanced_putter_factory
)
from ...field_validators import (
    entity_id_validator_factory, nullable_entity_validator_factory, preinstanced_validator_factory
)
from ...user import ClientUserBase

from ..channel import Channel

from .preinstanced import VoiceChannelEffectAnimationType

# animation_id

parse_animation_id = entity_id_parser_factory('animation_id')
put_animation_id_into = entity_id_putter_factory('animation_id')
validate_animation_id = entity_id_validator_factory('animation_id')

# animation_type

parse_animation_type = preinstanced_parser_factory(
    'animation_type', VoiceChannelEffectAnimationType, VoiceChannelEffectAnimationType.premium
)
put_animation_type_into = preinstanced_putter_factory('animation_type')
validate_animation_type = preinstanced_validator_factory('animation_type', VoiceChannelEffectAnimationType)

# channel_id

parse_channel_id = entity_id_parser_factory('channel_id')
put_channel_id_into = entity_id_putter_factory('channel_id')
validate_channel_id = entity_id_validator_factory('channel_id', Channel)

# emoji

parse_emoji = nullable_functional_parser_factory('emoji', create_partial_emoji_from_data)
put_emoji_into = nullable_functional_optional_putter_factory('emoji', create_partial_emoji_data)
validate_emoji = nullable_entity_validator_factory('emoji', Emoji)

# guild_id

parse_guild_id = entity_id_parser_factory('guild_id')
put_guild_id_into = entity_id_putter_factory('guild_id')
validate_guild_id = entity_id_validator_factory('guild_id', NotImplemented, include = 'Guild')

# user_id

parse_user_id = entity_id_parser_factory('user_id')
put_user_id_into = entity_id_putter_factory('user_id')
validate_user_id = entity_id_validator_factory('user_id', ClientUserBase)
