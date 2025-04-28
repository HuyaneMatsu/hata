__all__ = ()

from ...field_parsers import int_parser_factory, preinstanced_parser_factory
from ...field_putters import int_putter_factory, preinstanced_putter_factory
from ...field_validators import int_conditional_validator_factory, preinstanced_validator_factory

from .preinstanced import GuildActivityOverviewActivityLevel


# level

parse_level = preinstanced_parser_factory(
    'activity_level', GuildActivityOverviewActivityLevel, GuildActivityOverviewActivityLevel.none
)
put_level = preinstanced_putter_factory('activity_level')
validate_level = preinstanced_validator_factory('level', GuildActivityOverviewActivityLevel)


# score

parse_score = int_parser_factory('activity_score', 0)
put_score = int_putter_factory('activity_score')
validate_score = int_conditional_validator_factory(
    'score',
    0,
    lambda score : score >= 0,
    '>= 0',
)
