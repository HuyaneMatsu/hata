__all__ = ()

from ...field_parsers import int_parser_factory, nullable_entity_parser_factory
from ...field_putters import int_putter_factory, nullable_entity_optional_putter_factory
from ...field_validators import int_conditional_validator_factory, nullable_entity_validator_factory

from ..sku_enhancement_guild import SKUEnhancementGuild


# boost_cost

parse_boost_cost = int_parser_factory('boost_price', 0)
put_boost_cost = int_putter_factory('boost_price')
validate_boost_cost = int_conditional_validator_factory(
    'boost_cost',
    0,
    (lambda boost_cost : boost_cost >= 0),
    '>= 0',
)


# guild

parse_guild = nullable_entity_parser_factory('guild_features', SKUEnhancementGuild)
put_guild = nullable_entity_optional_putter_factory('guild_features', SKUEnhancementGuild)
validate_guild = nullable_entity_validator_factory('guild', SKUEnhancementGuild)


# purchase_limit

parse_purchase_limit = int_parser_factory('purchase_limit', 0)
put_purchase_limit = int_putter_factory('purchase_limit')
validate_purchase_limit = int_conditional_validator_factory(
    'purchase_limit',
    0,
    (lambda purchase_limit : purchase_limit >= 0),
    '>= 0',
)
