__all__ = ()

from ...fields.field_parsers import int_parser_factory, nullable_functional_array_parser_factory
from ...fields.field_putters import int_putter_factory, nullable_functional_array_optional_putter_factory_with_defaults
from ...fields.field_validators import int_conditional_validator_factory, nullable_object_array_validator_factory

from ..guild_join_request import (
    GuildJoinRequest, guild_join_request_convert_to_data, guild_join_request_create_from_data
)

# total

parse_total = int_parser_factory('total', 0)
put_total = int_putter_factory('total')
validate_total = int_conditional_validator_factory(
    'total',
    0,
    (lambda total : total >= 0),
    '>= 0',
)

# guild_join_requests

parse_guild_join_requests = nullable_functional_array_parser_factory(
    'guild_join_requests', guild_join_request_create_from_data
)
put_guild_join_requests = nullable_functional_array_optional_putter_factory_with_defaults(
    'guild_join_requests', guild_join_request_convert_to_data
)
validate_guild_join_requests = nullable_object_array_validator_factory(
    'guild_join_requests', GuildJoinRequest
)
