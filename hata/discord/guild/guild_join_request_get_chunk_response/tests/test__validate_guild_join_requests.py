import vampytest

from ...guild_join_request import (
    GuildJoinRequest, guild_join_request_create
)

from ..fields import validate_guild_join_requests


def _iter_options():
    guild_join_requests = (
        guild_join_request_create(guild_join_request_id = 202610180004),
        guild_join_request_create(guild_join_request_id = 202610180005),
    )
    
    yield (
        None,
        None,
    )
    
    
    yield (
        (),
        None,
    )
    
    yield (
        guild_join_requests,
        guild_join_requests,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_guild_join_requests(input_value):
    output = validate_guild_join_requests(input_value)
    
    vampytest.assert_instance(output, tuple, nullable = True)
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, GuildJoinRequest)
    
    return output
