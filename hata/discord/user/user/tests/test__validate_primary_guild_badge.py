import vampytest

from ....bases import Icon, IconType
from ....guild import GuildBadge

from ..fields import validate_primary_guild_badge


def _iter_options__passing():
    clan = GuildBadge(guild_id = 202405180002, icon = Icon(IconType.static, 2))
    
    yield None, None
    yield clan, clan


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_primary_guild_badge(input_value):
    """
    Tests whether `validate_primary_guild_badge` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | GuildBadge`
    
    Raises
    ------
    TypeError
    """
    output = validate_primary_guild_badge(input_value)
    vampytest.assert_instance(output, GuildBadge, nullable = True)
    return output
