import vampytest

from ......discord.guild import Guild

from ..helpers import _validate_1_guild


def _iter_options__passing():
    guild_id = 20241020006
    
    yield guild_id, guild_id
    yield Guild.precreate(guild_id), guild_id
    yield str(guild_id), guild_id


def _iter_options__type_error():
    yield None
    yield 12.6


def _iter_options__value_error():
    yield '-1'
    yield '1111111111111111111111'
    yield -1
    yield 1111111111111111111111


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_1_guild(input_value):
    """
    Tests whether `_validate_1_guild` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value to validate.
    
    Returns
    -------
    output : `int`
    
    Raises
    ------
    TypeError
    ValueError
    """
    return _validate_1_guild(input_value)
