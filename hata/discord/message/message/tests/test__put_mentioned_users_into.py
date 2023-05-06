import vampytest

from ....user import GuildProfile, User

from ..fields import put_mentioned_users_into


def test__put_mentioned_users_into():
    """
    Tests whether ``put_mentioned_users_into`` works as intended.
    """
    user_id_0 = 202305010003
    user_id_1 = 202305010004
    guild_id = 202305010005
    name_0 = 'Orin'
    name_1 = 'Okuu'
    nick_0 = 'Dancing cat'
    
    user_0 = User.precreate(user_id_0, name = name_0)
    guild_profile_0 = GuildProfile(nick = nick_0)
    user_0.guild_profiles[guild_id] = guild_profile_0
    user_1 = User.precreate(user_id_1, name = name_1)
    
    for input_value, defaults, guild_id, expected_output in (
        (
            None,
            False,
            0,
            {},
        ), (
            None,
            True,
            0,
            {'mentions': []},
        ),
        (
            (user_0,),
            True,
            0,
            {
                'mentions': [
                    user_0.to_data(defaults = True, include_internals = True),
                ],
            },
        ), (
            (user_0, user_1),
            False,
            guild_id,
            {
                'mentions': [
                    {
                        **user_0.to_data(include_internals = True),
                        'member': guild_profile_0.to_data(include_internals = True),
                    },
                    user_1.to_data(include_internals = True),
                ],
            },
        ),
    ):
        output = put_mentioned_users_into(input_value, {}, defaults, guild_id = guild_id)
        vampytest.assert_eq(output, expected_output)
