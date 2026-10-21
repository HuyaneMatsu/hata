import vampytest

from ...guild_join_request import GuildJoinRequest, guild_join_request_convert_to_data, guild_join_request_create

from ..fields import parse_guild_join_request


def _iter_options():
    guild_join_request = guild_join_request_create(
        guild_join_request_id = 202610100090,
    )
    
    yield (
        {},
        None,
    )
    
    yield (
        {
            'request': None,
        },
        None,
    )
    
    yield (
        {
            'request': guild_join_request_convert_to_data(guild_join_request),
        },
        guild_join_request,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_guild_join_request(input_data):
    output = parse_guild_join_request(input_data)
    vampytest.assert_instance(output, GuildJoinRequest, nullable = True)
    return output
