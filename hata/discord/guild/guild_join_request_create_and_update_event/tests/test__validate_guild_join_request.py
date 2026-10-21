import vampytest

from ...guild_join_request import GuildJoinRequest, guild_join_request_create

from ..fields import validate_guild_join_request


def _iter_options__passing():
    guild_join_request = guild_join_request_create(
        guild_join_request_id = 202610100092,
    )
    
    yield (
        None,
        None,
    )
    
    yield (
        guild_join_request,
        guild_join_request,
    )


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_guild_join_request(input_value):
    output = validate_guild_join_request(input_value)
    vampytest.assert_instance(output, GuildJoinRequest, nullable = True)
    return output
