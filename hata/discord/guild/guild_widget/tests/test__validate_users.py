import vampytest

from ...guild_widget_user import GuildWidgetUser

from ..fields import validate_users


def test__validate_users__0():
    """
    Validates whether ``validate_users`` works as intended.
    
    Case: passing.
    """
    user_id_0 = 10
    user_id_1 = 11
    
    user_0 = GuildWidgetUser(user_id = user_id_0)
    user_1 = GuildWidgetUser(user_id = user_id_1)
    
    for input_value, expected_output in (
        ([], None),
        ([user_0], (user_0,)),
        ([user_1, user_0], (user_0, user_1)),
    ):
        output = validate_users(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_users__1():
    """
    Validates whether ``validate_users`` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_users(input_value)
