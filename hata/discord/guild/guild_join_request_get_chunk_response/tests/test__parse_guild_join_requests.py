import vampytest

from ...guild_join_request import (
    GuildJoinRequest, guild_join_request_convert_to_data,
    guild_join_request_create
)

from ..fields import parse_guild_join_requests


def _iter_options():
    guild_join_requests = (
        guild_join_request_create(guild_join_request_id = 202610180000),
        guild_join_request_create(guild_join_request_id = 202610180001),
    )
    
    yield (
        {},
        None,
    )
    
    yield (
        {
            'form_responses': None,
        },
        None,
    )
    
    yield (
        {
            'form_responses': [],
        },
        None,
    )
    
    yield (
        {
            'form_responses': [
                guild_join_request_convert_to_data(response)
                for response in guild_join_requests
            ],
        },
        None,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_guild_join_requests(input_value):
    output = parse_guild_join_requests(input_value)
    
    vampytest.assert_instance(output, tuple, nullable = True)
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, GuildJoinRequest)
    
    return output
