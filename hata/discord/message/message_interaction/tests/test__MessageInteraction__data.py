import vampytest

from ....application import ApplicationIntegrationType
from ....interaction import InteractionType
from ....user import User

from ..message_interaction import MessageInteraction

from .test__MessageInteraction__constructor import _assert_fields_set


def test__MessageInteraction__from_data():
    """
    Tests whether ``MessageInteraction.from_data`` works as intended.
    """
    message_interaction_id = 202403250015
    
    interaction_type = InteractionType.application_command
    user = User.precreate(202403250016)
    sub_command_name_stack = ('Afraid', 'Darkness')
    name = 'Chata'
    response_message_id = 20240325007
    interacted_message_id = 20240325022
    target_message_id = 202410060010
    target_user = User.precreate(202410060011)
    triggering_interaction = MessageInteraction.precreate(202403260005, name = 'pain')
    authorizer_user_ids = {
        ApplicationIntegrationType.user_install: 202403270014,
        ApplicationIntegrationType.guild_install: 202403270015,
    }
    
    data = {
        'id': str(message_interaction_id),
        'type': interaction_type.value,
        'user': user.to_data(include_internals = True),
        'name': ' '.join([name, *sub_command_name_stack]),
        'original_response_message_id': str(response_message_id),
        'interacted_message_id': str(interacted_message_id),
        'target_message_id': str(target_message_id),
        'target_user': target_user.to_data(include_internals = True),
        'triggering_interaction_metadata': triggering_interaction.to_data(include_internals = True),
        'authorizing_integration_owners': {
            str(integration_type.value): str(user_id) for integration_type, user_id in authorizer_user_ids.items()
        },
    }
    
    message_interaction = MessageInteraction.from_data(data)
    
    _assert_fields_set(message_interaction)
    vampytest.assert_eq(message_interaction.id, message_interaction_id)
    
    vampytest.assert_eq(message_interaction.authorizer_user_ids, authorizer_user_ids)
    vampytest.assert_eq(message_interaction.interacted_message_id, interacted_message_id)
    vampytest.assert_eq(message_interaction.name, name)
    vampytest.assert_eq(message_interaction.response_message_id, response_message_id)
    vampytest.assert_eq(message_interaction.sub_command_name_stack, sub_command_name_stack)
    vampytest.assert_eq(message_interaction.target_message_id, target_message_id)
    vampytest.assert_is(message_interaction.target_user, target_user)
    vampytest.assert_eq(message_interaction.triggering_interaction, triggering_interaction)
    vampytest.assert_is(message_interaction.type, interaction_type)
    vampytest.assert_is(message_interaction.user, user)


def test__MessageInteraction__to_data():
    """
    Tests whether ``MessageInteraction.to_data`` works as intended.
    
    Case: defaults & include internals with guild id.
    """
    message_interaction_id = 202403250052
    
    interaction_type = InteractionType.application_command
    user = User.precreate(202403250019)
    sub_command_name_stack = ('Afraid', 'Darkness')
    name = 'Chata'
    response_message_id = 20240325008
    interacted_message_id = 2023030023
    target_message_id = 202410060012
    target_user = User.precreate(202410060013)
    triggering_interaction = MessageInteraction.precreate(202403260007, name = 'pain')
    authorizer_user_ids = {
        ApplicationIntegrationType.user_install: 202403270016,
        ApplicationIntegrationType.guild_install: 202403270017,
    }
    
    message_interaction = MessageInteraction.precreate(
        message_interaction_id,
        authorizer_user_ids = authorizer_user_ids,
        interacted_message_id = interacted_message_id,
        interaction_type = interaction_type,
        name = name,
        response_message_id = response_message_id,
        sub_command_name_stack = sub_command_name_stack,
        target_message_id = target_message_id,
        target_user = target_user,
        triggering_interaction = triggering_interaction,
        user = user,
    )
    
    expected_output = {
        'id': str(message_interaction_id),
        'type': interaction_type.value,
        'user': user.to_data(defaults = True, include_internals = True),
        'name': ' '.join([name, *sub_command_name_stack]),
        'original_response_message_id': str(response_message_id),
        'interacted_message_id': str(interacted_message_id),
        'target_message_id': str(target_message_id),
        'target_user': target_user.to_data(defaults = True, include_internals = True),
        'triggering_interaction_metadata': triggering_interaction.to_data(defaults = True, include_internals = True),
        'authorizing_integration_owners': {
            str(integration_type.value): str(user_id) for integration_type, user_id in authorizer_user_ids.items()
        },
    }
    
    vampytest.assert_eq(
        message_interaction.to_data(
            defaults = True,
            include_internals = True,
        ),
        expected_output,
    )
