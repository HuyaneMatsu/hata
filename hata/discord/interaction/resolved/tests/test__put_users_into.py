import vampytest

from ....user import User, GuildProfile

from ...interaction_event import InteractionEvent

from ..fields import put_users_into


def test__put_users_into():
    """
    Tests whether ``put_users_into`` works as intended.
    """
    user_id = 202211050023
    guild_id = 202211050024
    user_name = 'Faker'
    user_nick = 'COLORS'
    
    user = User.precreate(
        user_id,
        name = user_name,
    )
    
    guild_profile = GuildProfile(nick = user_nick)
    user.guild_profiles[guild_id] = guild_profile
    
    interaction_event_instance = InteractionEvent(guild_id = guild_id)
    
    
    for input_value, defaults, interaction_event, expected_output in (
        (None, False, None, {}),
        (None, True, None, {'users': {}, 'members': {}}),
        (
            {
                user_id: user,
            },
                True,
                None,
            {
                'users': {
                    str(user_id): user.to_data(defaults = True, include_internals = True),
                },
                'members': {},
            },
        ), (
            {
                user_id: user,
            },
                True,
                interaction_event_instance,
            {
                'users': {
                    str(user_id): user.to_data(defaults = True, include_internals = True),
                },
                'members': {
                    str(user_id): guild_profile.to_data(defaults = True, include_internals = True),
                },
            },
        )
    ):
        output = put_users_into(input_value, {}, defaults, interaction_event = interaction_event)
        vampytest.assert_eq(output, expected_output)
