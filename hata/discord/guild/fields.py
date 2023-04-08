__all__ = ()

from ..channel import Channel
from ..field_parsers import entity_id_parser_factory, int_parser_factory, preinstanced_array_parser_factory
from ..field_putters import entity_id_optional_putter_factory, int_putter_factory, preinstanced_array_putter_factory
from ..field_validators import (
    entity_id_validator_factory, int_conditional_validator_factory, int_options_validator_factory,
    preinstanced_array_validator_factory
)

from .constants import MAX_STAGE_CHANNEL_VIDEO_USERS_DEFAULT, MAX_VOICE_CHANNEL_VIDEO_USERS_DEFAULT
from .preinstanced import GuildFeature

# features

parse_features = preinstanced_array_parser_factory('features', GuildFeature)
put_features_into = preinstanced_array_putter_factory('features')
validate_features = preinstanced_array_validator_factory('features', GuildFeature)

# max_stage_channel_video_users

parse_max_stage_channel_video_users = int_parser_factory(
    'max_stage_video_channel_users', MAX_STAGE_CHANNEL_VIDEO_USERS_DEFAULT
)
put_max_stage_channel_video_users_into = int_putter_factory('max_stage_video_channel_users')
validate_max_stage_channel_video_users = int_conditional_validator_factory(
    'max_stage_channel_video_users',
    MAX_STAGE_CHANNEL_VIDEO_USERS_DEFAULT,
    (lambda max_stage_channel_video_users : max_stage_channel_video_users >= 0),
    '>= 0',
)

# max_voice_channel_video_users

parse_max_voice_channel_video_users = int_parser_factory(
    'max_video_channel_users', MAX_VOICE_CHANNEL_VIDEO_USERS_DEFAULT
)
put_max_voice_channel_video_users_into = int_putter_factory('max_video_channel_users')
validate_max_voice_channel_video_users = int_conditional_validator_factory(
    'max_voice_channel_video_users',
    MAX_VOICE_CHANNEL_VIDEO_USERS_DEFAULT,
    (lambda max_voice_channel_video_users : max_voice_channel_video_users >= 0),
    '>= 0',
)

# premium_tier

parse_premium_tier = int_parser_factory('premium_tier', 0)
put_premium_tier_into = int_putter_factory('premium_tier')
validate_premium_tier = int_options_validator_factory('premium_tier', frozenset((range(4))))

# safety_alerts_channel_id

parse_safety_alerts_channel_id = entity_id_parser_factory('safety_alerts_channel_id')
put_safety_alerts_channel_id_into = entity_id_optional_putter_factory('safety_alerts_channel_id')
validate_safety_alerts_channel_id = entity_id_validator_factory('safety_alerts_channel_id', Channel)
