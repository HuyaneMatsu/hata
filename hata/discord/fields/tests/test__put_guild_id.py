import vampytest

from ..fields_common import put_guild_id


def _iter_options():
    guild_id = 202305160009
    
    yield (
        0,
        False,
        {
            'guild_id': None,
        },
    )
    
    yield (
        0,
        True,
        {
            'guild_id': None,
        },
    )
    
    yield (
        guild_id,
        False,
        {
            'guild_id': str(guild_id),
        },
    )
    
    yield (
        guild_id,
        True,
        {
            'guild_id': str(guild_id),
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_guild_id(input_value, defaults):
    return put_guild_id(input_value, {}, defaults)
