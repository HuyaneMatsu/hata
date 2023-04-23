import vampytest

from ....user import GuildProfile, User

from ..fields import put_user_into


def test__put_user_into():
    """
    Tests whether ``put_user_into`` works as intended.
    """
    user_0 = User.precreate(202304230003, name = 'Yuuka')
    user_1 = User.precreate(202304230004, name = 'Yukari')
    guild_profile_0 = GuildProfile(nick = 'Yuuma')
    guild_id_0 = 202304230005
    user_1.guild_profiles[guild_id_0] = guild_profile_0
    
    
    for input_value, guild_id, expected_output in (
        (user_0, 0, {'user': user_0.to_data(include_internals = True)}),
        (user_0, guild_id_0, {'user': user_0.to_data(include_internals = True)}),
        (user_1, 0, {'user': user_1.to_data(include_internals = True)}),
        (
            user_1,
            guild_id_0, 
            {
                'user': user_1.to_data(include_internals = True),
                'member': guild_profile_0.to_data(include_internals = True),
            },
        ),
    ):
        output = put_user_into(input_value, {}, False, guild_id = guild_id)
        vampytest.assert_eq(output, expected_output)
