import vampytest

from ....guild import Guild

from ..fields import validate_guild


def _iter_options():
    guild_id = 202310100006
    guild = Guild.precreate(guild_id)
    yield guild, guild
    yield None, None


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_guild__passing(input_value):
    """
    Tests whether `validate_guild` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `None`, ``Guild``
        The guild to validate.
    
    Returns
    -------
    output : `None`, ``Guild``
    """
    return validate_guild(input_value)


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
def test__validate_guild__type_error(input_value):
    """
    Tests whether `validate_guild` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        Value to pass.
    
    Raises
    ------
    TypeError
    """
    validate_guild(input_value)
