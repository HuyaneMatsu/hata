__all__ = ()

from ..field_parsers import preinstanced_array_parser_factory, int_parser_factory, entity_id_parser_factory
from ..field_putters import preinstanced_array_putter_factory, int_putter_factory, entity_id_optional_putter_factory
from ..field_validators import preinstanced_array_validator_factory, int_options_validator_factory, \
    entity_id_validator_factory

from ..channel import Channel
from .preinstanced import GuildFeature

# features

parse_features = preinstanced_array_parser_factory('features', GuildFeature)
put_features_into = preinstanced_array_putter_factory('features')
validate_features = preinstanced_array_validator_factory('features', GuildFeature)

# premium_tier

parse_premium_tier = int_parser_factory('premium_tier', 0)
put_premium_tier_into = int_putter_factory('premium_tier')
validate_premium_tier = int_options_validator_factory('premium_tier', frozenset((range(4))))

# safety_alerts_channel_id

parse_safety_alerts_channel_id = entity_id_parser_factory('safety_alerts_channel_id')
put_safety_alerts_channel_id_into = entity_id_optional_putter_factory('safety_alerts_channel_id')
validate_safety_alerts_channel_id = entity_id_validator_factory('safety_alerts_channel_id', Channel)
