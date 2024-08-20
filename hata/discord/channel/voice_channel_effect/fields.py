__all__ = ()

from ...emoji import Emoji, create_partial_emoji_data, create_partial_emoji_from_data
from ...field_parsers import (
    entity_id_parser_factory, float_parser_factory, nullable_functional_parser_factory, preinstanced_parser_factory
)
from ...field_putters import (
    entity_id_optional_putter_factory, entity_id_putter_factory, float_optional_putter_factory,
    nullable_functional_optional_putter_factory, preinstanced_optional_putter_factory
)
from ...field_validators import (
    entity_id_validator_factory, float_conditional_validator_factory, nullable_entity_validator_factory,
    preinstanced_validator_factory
)
from ...soundboard import SoundboardSound
from ...user import ClientUserBase

from ..channel import Channel

from .preinstanced import VoiceChannelEffectAnimationType


# animation_id

parse_animation_id = entity_id_parser_factory('animation_id')
put_animation_id_into = entity_id_optional_putter_factory('animation_id')
validate_animation_id = entity_id_validator_factory('animation_id')


# animation_type

parse_animation_type = preinstanced_parser_factory(
    'animation_type', VoiceChannelEffectAnimationType, VoiceChannelEffectAnimationType.premium
)
put_animation_type_into = preinstanced_optional_putter_factory(
    'animation_type', VoiceChannelEffectAnimationType.premium
)
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


# sound_id

parse_sound_id = entity_id_parser_factory('sound_id')
put_sound_id_into = entity_id_optional_putter_factory('sound_id')
validate_sound_id = entity_id_validator_factory('sound_id', SoundboardSound)


# sound_volume

parse_sound_volume = float_parser_factory('sound_volume', 1.0)
put_sound_volume_into = float_optional_putter_factory('sound_volume', 1.0)
validate_sound_volume = float_conditional_validator_factory(
    'sound_volume',
    1.0,
    lambda sound_volume : sound_volume >= 0.0 and sound_volume <= 1.0,
    '>= 0.0 and <= 1.0',
)


# user_id

parse_user_id = entity_id_parser_factory('user_id')
put_user_id_into = entity_id_putter_factory('user_id')
validate_user_id = entity_id_validator_factory('user_id', ClientUserBase)
