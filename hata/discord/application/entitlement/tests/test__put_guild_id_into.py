import vampytest

from ..fields import put_guild_id_into


def _iter_options():
    guild_id = 202310020011
    
    yield 0, False, {}
    yield 0, True, {'guild_id': None}
    yield guild_id, False, {'guild_id': str(guild_id)}
    yield guild_id, True, {'guild_id': str(guild_id)}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_guild_id_into(guild_id, defaults):
    """
    Tests whether ``put_guild_id_into`` works as intended.
    
    Parameters
    ----------
    guild_id : `int`
        The guild's identifier to serialise.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_guild_id_into(guild_id, {}, defaults)
