import vampytest

from ...guild_widget_user import GuildWidgetUser

from ..fields import put_users_into


def test__put_users_into():
    """
    Tests whether ``put_users_into`` works as intended.
    """
    user_id_0 = 10
    user_name_0 = 'Far'
    
    user_id_1 = 11
    user_name_1 = 'East'
    
    user_0 = GuildWidgetUser(
        user_id = user_id_0,
        name = user_name_0,
    )
    
    user_1 = GuildWidgetUser(
        user_id = user_id_1,
        name = user_name_1,
    )
    
    for input_value, defaults, expected_output in (
        (None, False, {'members': []}),
        (None, True, {'members': []}),
        (
            (user_0, user_1),
            False,
            {
                'members': [
                    user_0.to_data(defaults = False),
                    user_1.to_data(defaults = False),
                ],
            },
        ),
        (
            (user_0, user_1),
            True,
            {
                'members': [
                    user_0.to_data(defaults = True),
                    user_1.to_data(defaults = True),
                ],
            },
        ),
    ):
        output = put_users_into(input_value, {}, defaults)
        vampytest.assert_eq(output, expected_output)
