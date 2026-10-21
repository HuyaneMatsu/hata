import vampytest

from ..fields import put_guild_join_request_id


def _iter_options():
    guild_join_request_id = 202610100060
    
    yield (
        0,
        False,
        {
            'id': None,
        },
    )
    
    yield (
        0,
        True,
        {
            'id': None,
        },
    )
    
    yield (
        guild_join_request_id,
        False,
        {
            'id': str(guild_join_request_id),
        },
    )
    
    yield (
        guild_join_request_id,
        True,
        {
            'id': str(guild_join_request_id),
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_guild_join_request_id(input_value, defaults):
    return put_guild_join_request_id(input_value, {}, defaults)
