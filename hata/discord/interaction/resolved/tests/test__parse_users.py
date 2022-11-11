import vampytest

from ....user import User, GuildProfile

from ...interaction_event import InteractionEvent

from ..fields import parse_users


def test__parse_users():
    """
    Tests whether ``parse_users`` works as intended.
    """
    user_id = 202211050025
    guild_id = 202211050026
    user_name = 'Faker'
    user_nick = 'COLORS'
    
    user = User.precreate(
        user_id,
        name = user_name,
    )
    
    guild_profile = GuildProfile(nick = user_nick)
    
    interaction_event = InteractionEvent(guild_id = guild_id)
    
    
    for input_value, expected_output in (
        ({}, None),
        ({'users': {}}, None),
        ({'users': {}, 'members': {}}, None),
        ({'members': {}}, None),
        (
            {
                'users': {
                    str(user_id): user.to_data(defaults = True, include_internals = True),
                }
            },
            {
                user_id: user,
            }
        ),
        (
            {
                'users': {
                    str(user_id): user.to_data(defaults = True, include_internals = True),
                },
                'members': {
                     str(user_id): guild_profile.to_data(defaults = True, include_internals = True),
                },
            },
            {
                user_id: user,
            }
        )
    ):
        output = parse_users(input_value, interaction_event)
        vampytest.assert_eq(output, expected_output)
        
        if output and 'members' in input_value:
            vampytest.assert_eq(output[user_id].guild_profiles.get(guild_id, None), guild_profile)
