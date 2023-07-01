import vampytest

from ....guild import Guild

from ..fields import validate_guild_id


def _iter_options__passing():
    guild_id = 202305260002
    
    yield None, 0
    yield 0, 0
    yield guild_id, guild_id
    yield Guild.precreate(guild_id), guild_id
    yield str(guild_id), guild_id


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
def test__validate_guild_id__passing(input_value):
    """
    Tests whether `validate_guild_id` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value to get `guild_id` of.
    
    Returns
    -------
    output : `int`
    """
    return validate_guild_id(input_value)


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
def test__validate_guild_id__type_error():
    """
    Tests whether `validate_guild_id` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        Input value to get `guild_id` of.
    
    Raises
    ------
    TypeError
        The occurred exception.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_guild_id(input_value)


@vampytest.raising(ValueError)
@vampytest.call_with('-1')
@vampytest.call_with('1111111111111111111111')
@vampytest.call_with(-1)
@vampytest.call_with(1111111111111111111111)
def test__validate_guild_id__value_error(input_value):
    """
    Tests whether `validate_guild_id` works as intended.
    
    Case: `ValueError`.
    
    Parameters
    ----------
    input_value : `object`
        Input value to get `guild_id` of.
    
    Raises
    ------
    ValueError
        The occurred exception.
    """
    validate_guild_id(input_value)
