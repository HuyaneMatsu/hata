import vampytest

from ...guild_widget_user import GuildWidgetUser

from ..fields import validate_users


def _iter_options():
    user_id_0 = 10
    user_id_1 = 11
    
    user_0 = GuildWidgetUser(user_id = user_id_0)
    user_1 = GuildWidgetUser(user_id = user_id_1)

    yield (None, None)
    yield ([], None)
    yield ([user_0], (user_0,))
    yield ([user_1, user_0], (user_0, user_1))


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_users__passing(input_value):
    """
    Validates whether ``validate_users`` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : `None | tuple<GuildWidgetUser>`
    """
    return validate_users(input_value)


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
def test__validate_users__type_error(input_value):
    """
    Validates whether ``validate_users`` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Raises
    ------
    TypeError
    """
    validate_users(input_value)
