import vampytest

from ....user import GuildProfile, User

from ...message_interaction import MessageInteraction

from ..fields import put_interaction_into


def test__put_interaction_into__0():
    """
    Tests whether ``put_interaction_into`` is working as intended.
    
    Case: Without guild identifier.
    """
    interaction_id = 202304300004
    interaction = MessageInteraction.precreate(interaction_id, name = 'Orin')
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (interaction, False, {'interaction': interaction.to_data(include_internals = True)}),
        (interaction, True, {'interaction': interaction.to_data(defaults = True, include_internals = True)}),
    ):
        data = put_interaction_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)


def test__put_interaction_into__1():
    """
    Tests whether ``put_interaction_into`` works as intended.
    
    Case: With guild identifier.
    """
    user_id = 202304300010
    interaction_id = 202304300011
    guild_id = 202304300012
    
    user = User.precreate(user_id, name = 'Hell')
    guild_profile = GuildProfile(nick = 'Rose')
    user.guild_profiles[guild_id] = guild_profile
    
    interaction = MessageInteraction.precreate(interaction_id, user = user)
    
    expected_output = {
        'interaction': interaction.to_data(include_internals = True, guild_id = guild_id)
    }
    
    output = put_interaction_into(interaction, {}, False, guild_id = guild_id)
    
    vampytest.assert_eq(output, expected_output)
