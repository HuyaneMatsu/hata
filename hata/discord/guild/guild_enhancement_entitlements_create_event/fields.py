__all__ = ()

from ...field_parsers import entity_id_parser_factory, nullable_entity_array_parser_factory
from ...field_putters import entity_id_putter_factory, nullable_entity_array_putter_factory
from ...field_validators import entity_id_validator_factory, nullable_entity_array_validator_factory

from ..guild import Guild


# entitlements

parse_entitlements = nullable_entity_array_parser_factory(
    'entitlements', NotImplemented, include = 'Entitlement'
)
put_entitlements = nullable_entity_array_putter_factory(
    'entitlements', NotImplemented, include = 'Entitlement', force_include_internals = True
)
validate_entitlements = nullable_entity_array_validator_factory(
    'entitlements', NotImplemented, include = 'Entitlement'
)


# guild_id

parse_guild_id = entity_id_parser_factory('guild_id')
put_guild_id = entity_id_putter_factory('guild_id')
validate_guild_id = entity_id_validator_factory('guild_id', Guild)
