import vampytest

from ....user import GuildProfile, User, ZEROUSER

from ..fields import parse_user


def test__parse_user():
    """
    Tests whether ``parse_user`` works as intended.
    """
    user_0 = User.precreate(202304230000, name = 'Yuuka')
    user_1 = User.precreate(202304230001, name = 'Yuuka')
    guild_profile_0 = GuildProfile(nick = 'Yukkuri')
    guild_id_0 = 202304230002
    
    for input_data, guild_id, expected_output, expected_guild_profiles in (
        ({}, 0, ZEROUSER, {}),
        ({'user': None}, 0, ZEROUSER, {}),
        ({'user': user_0.to_data(include_internals = True)}, 0, user_0, {}),
        ({'user': user_0.to_data(include_internals = True)}, guild_id_0, user_0, {}),
        (
            {
                'user': user_0.to_data(include_internals = True),
                'member': guild_profile_0.to_data(include_internals = True),
            },
            0,
            user_0,
            {},
        ),
        (
            {
                'user': user_1.to_data(include_internals = True),
                'member': guild_profile_0.to_data(include_internals = True),
            },
            guild_id_0,
            user_1,
            {guild_id_0: guild_profile_0},
        ),
    ):
        output = parse_user(input_data, guild_id = guild_id)
        vampytest.assert_is(output, expected_output)
        vampytest.assert_eq(output.guild_profiles, expected_guild_profiles)
