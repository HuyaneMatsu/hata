__all__ = ()

from ...fields.field_parsers import nullable_entity_array_parser_factory
from ...fields.field_putters import nullable_entity_array_putter_factory
from ...fields.field_validators import nullable_entity_array_validator_factory
from ...fields.fields_common import parse_guild_id, put_guild_id, validate_guild_id

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
