import vampytest

from ....application import ApplicationIntegrationType
from ....interaction import InteractionType

from ..message_interaction import MessageInteraction


def test__MessageInteraction__repr():
    """
    tests whether ``MessageInteraction.__repr__`` works as intended.
    """
    message_interaction_id = 202403250021
    
    interaction_type = InteractionType.application_command
    user_id = 202403250022
    sub_command_name_stack = ('Afraid', 'Darkness')
    name = 'Chata'
    response_message_id = 20240325009
    interacted_message_id = 20240325040
    triggering_interaction = MessageInteraction.precreate(202403260008, name = 'pain')
    authorizer_user_ids = {
        ApplicationIntegrationType.user_install: 202403270018,
        ApplicationIntegrationType.guild_install: 202403270019,
    }
    
    message_interaction = MessageInteraction.precreate(
        message_interaction_id,
        authorizer_user_ids = authorizer_user_ids,
        interacted_message_id = interacted_message_id,
        interaction_type = interaction_type,
        name = name,
        response_message_id = response_message_id,
        sub_command_name_stack = sub_command_name_stack,
        triggering_interaction = triggering_interaction,
        user_id = user_id,
    )
    
    vampytest.assert_instance(repr(message_interaction), str)


def test__MessageInteraction__hash():
    """
    tests whether ``MessageInteraction.__hash__`` works as intended.
    """
    message_interaction_id = 202403250023
    
    interaction_type = InteractionType.application_command
    user_id = 202403250024
    sub_command_name_stack = ('Afraid', 'Darkness')
    name = 'Chata'
    response_message_id = 20240325010
    interacted_message_id = 20240325041
    triggering_interaction = MessageInteraction.precreate(202403260009, name = 'pain')
    authorizer_user_ids = {
        ApplicationIntegrationType.user_install: 202403270020,
        ApplicationIntegrationType.guild_install: 202403270021,
    }
    
    message_interaction = MessageInteraction.precreate(
        message_interaction_id,
        authorizer_user_ids = authorizer_user_ids,
        interacted_message_id = interacted_message_id,
        interaction_type = interaction_type,
        name = name,
        response_message_id = response_message_id,
        sub_command_name_stack = sub_command_name_stack,
        triggering_interaction = triggering_interaction,
        user_id = user_id,
    )
    
    vampytest.assert_instance(hash(message_interaction), int)


def test__MessageInteraction__eq():
    """
    Tests whether ``MessageInteraction.__eq__`` works as intended.
    """
    message_interaction_id_0 = 202403250025
    message_interaction_id_1 = 202403250026
    
    interaction_type = InteractionType.application_command
    user_id = 202403250027
    sub_command_name_stack = ('Afraid', 'Darkness')
    name = 'Chata'
    response_message_id = 20240325011
    interacted_message_id = 20240325042
    triggering_interaction = MessageInteraction.precreate(202403260010, name = 'pain')
    authorizer_user_ids = {
        ApplicationIntegrationType.user_install: 202403270022,
        ApplicationIntegrationType.guild_install: 202403270023,
    }
    
    keyword_parameters = {
        'message_interaction_id': message_interaction_id_0,
        'authorizer_user_ids': authorizer_user_ids,
        'interacted_message_id': interacted_message_id,
        'interaction_type': interaction_type,
        'name': name,
        'response_message_id': response_message_id,
        'sub_command_name_stack': sub_command_name_stack,
        'triggering_interaction': triggering_interaction,
        'user_id': user_id,
    }
    
    message_interaction = MessageInteraction.precreate(**keyword_parameters)
    vampytest.assert_eq(message_interaction, message_interaction)
    vampytest.assert_ne(message_interaction, object())
    
    for field_name, field_value in (
        ('message_interaction_id', message_interaction_id_1),
        ('authorizer_user_ids', None),
        ('interacted_message_id', 0),
        ('name', 'Slayer'),
        ('response_message_id', 0),
        ('interaction_type', InteractionType.form_submit),
        ('sub_command_name_stack', None),
        ('triggering_interaction', None),
        ('user_id', 202403250028),
    ):
        test_message_interaction = MessageInteraction.precreate(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(message_interaction, test_message_interaction)


def test__MessageInteraction__eq__partial():
    """
    Tests whether ``MessageInteraction.__eq__`` works as intended.
    
    Case: Partial with non-partial.
    """
    name = 'Afraid'
    message_interaction_id = 202305040168
    
    message_interaction_0 = MessageInteraction.precreate(message_interaction_id = message_interaction_id, name = name)
    message_interaction_1 = MessageInteraction(name = name)
    
    vampytest.assert_eq(message_interaction_0, message_interaction_1)
