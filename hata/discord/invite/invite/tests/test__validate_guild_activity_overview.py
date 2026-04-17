import vampytest

from ....guild import GuildActivityOverview

from ..fields import validate_guild_activity_overview


def _iter_options__passing():
    guild_id = 202504270002
    guild_activity_overview = GuildActivityOverview.precreate(guild_id)
    yield guild_activity_overview, guild_activity_overview
    yield None, None


def _iter_options__type_error():
    yield 12.65


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_guild_activity_overview__passing(input_value):
    """
    Tests whether `validate_guild_activity_overview` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : ``None | GuildActivityOverview``
    
    Raises
    ------
    TypeError
    """
    output = validate_guild_activity_overview(input_value)
    vampytest.assert_instance(output, GuildActivityOverview, nullable = True)
    return output
