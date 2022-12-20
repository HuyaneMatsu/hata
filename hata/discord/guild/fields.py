__all__ = ()

from ..field_parsers import preinstanced_array_parser_factory, int_parser_factory
from ..field_putters import preinstanced_array_putter_factory, int_putter_factory
from ..field_validators import preinstanced_array_validator_factory, int_options_validator_factory

from .preinstanced import GuildFeature

# features

parse_features = preinstanced_array_parser_factory('features', GuildFeature)
put_features_into = preinstanced_array_putter_factory('features')
validate_features = preinstanced_array_validator_factory('features', GuildFeature)

# premium_tier

parse_premium_tier = int_parser_factory('premium_tier', 0)
put_premium_tier_into = int_putter_factory('premium_tier')
validate_premium_tier = int_options_validator_factory('premium_tier', frozenset((range(4))))
