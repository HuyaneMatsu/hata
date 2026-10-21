import vampytest

from ...guild_join_request import (
    guild_join_request_convert_to_data, guild_join_request_create
)

from ..fields import put_guild_join_requests


def _iter_options():
    guild_join_requests = (
        guild_join_request_create(guild_join_request_id = 202610180002),
        guild_join_request_create(guild_join_request_id = 202610180003),
    )
    
    yield (
        None,
        False,
        {},
    )
    
    yield (
        None,
        True,
        {
            'guild_join_requests': [],
        },
    )
    
    yield (
        guild_join_requests,
        False,
        {
            'guild_join_requests': [
                guild_join_request_convert_to_data(request, defaults = False)
                for request in guild_join_requests
            ],
        },
    )
    
    yield (
        guild_join_requests,
        True,
        {
            'guild_join_requests': [
                guild_join_request_convert_to_data(request, defaults = True)
                for request in guild_join_requests
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_guild_join_requests(inout_data, defaults):
    return put_guild_join_requests(inout_data, {}, defaults)
