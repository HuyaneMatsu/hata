import vampytest

from ......discord.guild import Guild

from ..helpers import _validate_guild


def _iter_options__passing():
    guild_id_0 = 20241020007
    guild_id_1 = 20241020008
    
    yield guild_id_0, {guild_id_0}
    yield Guild.precreate(guild_id_0), {guild_id_0}
    yield str(guild_id_0), {guild_id_0}
    yield [guild_id_0], {guild_id_0}
    yield [Guild.precreate(guild_id_0)], {guild_id_0}
    yield [str(guild_id_0)], {guild_id_0}
    yield [guild_id_0, guild_id_0], {guild_id_0}
    yield [guild_id_0, guild_id_1], {guild_id_0, guild_id_1}


def _iter_options__type_error():
    yield object()
    yield [object()]
    yield None
    yield [None]
    yield [20241020009, None]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_guild(input_value):
    """
    Tests whether `_validate_guild` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value to validate.
    
    Returns
    -------
    output : `set<int>`
    
    Raises
    ------
    TypeError
    ValueError
    """
    return _validate_guild(input_value)
