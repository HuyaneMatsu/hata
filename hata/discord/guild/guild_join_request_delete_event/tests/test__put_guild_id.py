import vampytest

from ..fields import put_guild_id


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
    """
    Tests whether ``put_guild_id`` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        Value to serialize.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_guild_id(input_value, {}, defaults)
