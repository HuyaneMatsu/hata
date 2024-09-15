import vampytest

from ....guild import Guild

from ..fields import validate_guild_id


def _iter_options__passing():
    guild_id = 202409010032
    
    yield None, 0
    yield 0, 0
    yield guild_id, guild_id
    yield Guild.precreate(guild_id), guild_id
    yield str(guild_id), guild_id


def _iter_options__type_error():
    yield 12.6


def _iter_options__value_error():
    yield '-1'
    yield '1111111111111111111111'
    yield -1
    yield 1111111111111111111111
    

@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_guild_id(input_value):
    """
    Tests whether `validate_guild_id` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : `int`
    
    Raises
    ------
    TypeError
    ValueError
    """
    output = validate_guild_id(input_value)
    vampytest.assert_instance(output, int)
    return output
