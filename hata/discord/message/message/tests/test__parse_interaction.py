import vampytest

from ....user import GuildProfile, User

from ...message_interaction import MessageInteraction

from ..fields import parse_interaction


def test__parse_interaction__0():
    """
    Tests whether ``parse_interaction`` works as intended.
    
    Case: No guild identifier.
    """
    interaction_id = 202304300003
    interaction = MessageInteraction.precreate(interaction_id, name = 'orin')
    
    for input_data, expected_output in (
        ({}, None),
        ({'interaction': None}, None),
        ({'interaction': interaction.to_data(include_internals = True)}, interaction),
    ):
        output = parse_interaction(input_data)
        vampytest.assert_eq(output, expected_output)


def test__parse_interaction__1():
    """
    Tests whether ``parse_interaction`` works as intended.
    
    Case: With guild identifier.
    """
    user_id = 202304300007
    interaction_id = 202304300008
    guild_id = 202304300009
    
    user = User.precreate(user_id, name = 'Hell')
    guild_profile = GuildProfile(nick = 'Rose')
    
    data = {
        'interaction': {
            'id': str(interaction_id),
            'user': user.to_data(include_internals = True),
            'member': guild_profile.to_data(include_internals = True),
        }
    }
    output = parse_interaction(data, guild_id)
    vampytest.assert_instance(output, MessageInteraction)
    
    vampytest.assert_is(output.user, user)
    vampytest.assert_eq(output.user.guild_profiles, {guild_id: guild_profile})
