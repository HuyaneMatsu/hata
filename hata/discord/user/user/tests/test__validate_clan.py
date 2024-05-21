import vampytest

from ....bases import Icon, IconType

from ...user_clan import UserClan

from ..fields import validate_clan


def _iter_options__passing():
    clan = UserClan(guild_id = 202405180002, icon = Icon(IconType.static, 2))
    
    yield None, None
    yield clan, clan


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_clan(input_value):
    """
    Tests whether `validate_clan` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | UserClan`
    
    Raises
    ------
    TypeError
    """
    return validate_clan(input_value)
