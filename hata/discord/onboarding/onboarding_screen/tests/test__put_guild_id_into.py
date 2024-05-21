import vampytest

from ..fields import put_guild_id_into


def _iter_options():
    guild_id = 202303040026
    
    yield 0, False, {'guild_id': None}
    yield 0, True, {'guild_id': None}
    yield guild_id, False, {'guild_id': str(guild_id)}
    yield guild_id, True, {'guild_id': str(guild_id)}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_guild_id_into(input_value, defaults):
    """
    Tests whether ``put_guild_id_into`` works as intended.
    
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
    return put_guild_id_into(input_value, {}, defaults)
