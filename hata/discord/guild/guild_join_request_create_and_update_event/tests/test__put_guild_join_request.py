import vampytest

from ...guild_join_request import guild_join_request_convert_to_data, guild_join_request_create

from ..fields import put_guild_join_request


def _iter_options():
    guild_join_request = guild_join_request_create(
        guild_join_request_id = 202610100091,
    )
    
    yield (
        None,
        False,
        {
            'request': None,
        },
    )
    
    yield (
        None,
        True,
        {
            'request': None,
        },
    )
    
    yield (
        guild_join_request,
        False,
        {
            'request': guild_join_request_convert_to_data(guild_join_request, defaults = False),
        },
    )
    
    yield (
        guild_join_request,
        True,
        {
            'request': guild_join_request_convert_to_data(guild_join_request, defaults = True),
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_guild_join_request(input_value, defaults):
    return put_guild_join_request(input_value, {}, defaults)
