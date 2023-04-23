import vampytest

from ....interaction import InteractionType
from ....user import GuildProfile, User

from ..message_interaction import MessageInteraction

from .test__MessageInteraction__constructor import _assert_fields_set


def test__MessageInteraction__from_data():
    """
    Tests whether ``MessageInteraction.from_data`` works as intended.
    """
    message_interaction_id = 202304230015
    
    interaction_type = InteractionType.application_command
    user = User.precreate(202304230016, name = 'Kobayashi')
    sub_command_name_stack = ('Afraid', 'Darkness')
    name = 'Chata'
    
    guild_profile = GuildProfile(nick = 'Tohru')
    guild_id = 202304230017
    
    data = {
        'id': str(message_interaction_id),
        'type': interaction_type.value,
        'user': user.to_data(include_internals = True),
        'member': guild_profile.to_data(include_internals = True),
        'name': ' '.join([name, *sub_command_name_stack]),
    }
    
    message_interaction = MessageInteraction.from_data(data, guild_id)
    
    _assert_fields_set(message_interaction)
    vampytest.assert_eq(message_interaction.id, message_interaction_id)
    
    vampytest.assert_eq(message_interaction.name, name)
    vampytest.assert_eq(message_interaction.sub_command_name_stack, sub_command_name_stack)
    vampytest.assert_is(message_interaction.type, interaction_type)
    vampytest.assert_is(message_interaction.user, user)
    vampytest.assert_eq(message_interaction.user.guild_profiles, {guild_id: guild_profile})


def test__MessageInteraction__to_data():
    """
    Tests whether ``MessageInteraction.to_data`` works as intended.
    
    Case: defaults & include internals with guild id.
    """
    message_interaction_id = 202304230018
    
    interaction_type = InteractionType.application_command
    user = User.precreate(202304230019, name = 'Kobayashi')
    sub_command_name_stack = ('Afraid', 'Darkness')
    name = 'Chata'
    
    guild_profile = GuildProfile(nick = 'Tohru')
    guild_id = 202304230020
    user.guild_profiles[guild_id] = guild_profile
    
    message_interaction = MessageInteraction.precreate(
        message_interaction_id,
        interaction_type = interaction_type,
        name = name,
        sub_command_name_stack = sub_command_name_stack,
        user = user,
    )
    
    expected_output = {
        'id': str(message_interaction_id),
        'type': interaction_type.value,
        'user': user.to_data(defaults = True, include_internals = True),
        'member': guild_profile.to_data(defaults = True, include_internals = True),
        'name': ' '.join([name, *sub_command_name_stack]),
    }
    
    vampytest.assert_eq(
        message_interaction.to_data(
            defaults = True,
            include_internals = True,
            guild_id = guild_id,
        ),
        expected_output,
    )
