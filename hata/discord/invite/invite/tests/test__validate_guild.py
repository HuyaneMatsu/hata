import vampytest

from ....guild import Guild

from ..fields import validate_guild


def _iter_options__passing():
    guild_id = 202307290013
    guild = Guild.precreate(guild_id)
    yield guild, guild
    yield None, None


def _iter_options__type_error():
    yield 12.65


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_guild__passing(input_value):
    """
    Tests whether `validate_guild` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : ``None | Guild``
    
    Raises
    ------
    TypeError
    """
    output = validate_guild(input_value)
    vampytest.assert_instance(output, Guild, nullable = True)
    return output
