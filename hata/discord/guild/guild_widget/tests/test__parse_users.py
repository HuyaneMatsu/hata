import vampytest

from ...guild_widget_user import GuildWidgetUser

from ..fields import parse_users


def test__parse_users():
    """
    Tests whether ``parse_users`` works as intended.
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
    
    for input_data, expected_output in (
        ({}, None),
        ({'members': None}, None),
        ({'members': []}, None),
        (
            {
                'members': [
                    user_0.to_data(),
                ],
            },
            (user_0,),
        ),
        (
            {
                'members': [
                    user_0.to_data(),
                    user_1.to_data(),
                ],
            },
            (user_0, user_1),
        ),
    ):
        output = parse_users(input_data)
        vampytest.assert_eq(output, expected_output)
