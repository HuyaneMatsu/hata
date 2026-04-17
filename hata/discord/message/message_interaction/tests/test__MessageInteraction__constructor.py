import vampytest

from ....application import ApplicationIntegrationType
from ....interaction import InteractionType
from ....user import ClientUserBase, User

from ..message_interaction import MessageInteraction


def _assert_fields_set(message_interaction):
    """
    Checks whether every attributes are set of the message interaction.
    
    Parameters
    ----------
    message_interaction : ``MessageInteraction``
        The message interaction to check.
    """
    vampytest.assert_instance(message_interaction, MessageInteraction)
    
    vampytest.assert_instance(message_interaction.authorizer_user_ids, dict, nullable = True)
    vampytest.assert_instance(message_interaction.id, int)
    vampytest.assert_instance(message_interaction.interacted_message_id, int)
    vampytest.assert_instance(message_interaction.name, str)
    vampytest.assert_instance(message_interaction.response_message_id, int)
    vampytest.assert_instance(message_interaction.sub_command_name_stack, tuple, nullable = True)
    vampytest.assert_instance(message_interaction.target_message_id, int)
    vampytest.assert_instance(message_interaction.target_user, ClientUserBase, nullable = True)
    vampytest.assert_instance(message_interaction.triggering_interaction, MessageInteraction, nullable = True)
    vampytest.assert_instance(message_interaction.type, InteractionType)
    vampytest.assert_instance(message_interaction.user, ClientUserBase)


def test__MessageInteraction__new__no_fields():
    """
    Tests whether ``MessageInteraction.__new__`` works as intended.
    
    Case: no parameters.
    """
    message_interaction = MessageInteraction()
    _assert_fields_set(message_interaction)


def test__MessageInteraction__new__all_fields():
    """
    Tests whether ``MessageInteraction.__new__`` works as intended.
    
    Case: all fields given.
    """
    interaction_type = InteractionType.application_command
    user = User.precreate(202403250010)
    sub_command_name_stack = ('Afraid', 'Darkness')
    name = 'Chata'
    response_message_id = 202403250005
    interacted_message_id = 202403250020
    target_message_id = 202410060006
    target_user = User.precreate(202410060007)
    triggering_interaction = MessageInteraction.precreate(202403260003, name = 'pain')
    authorizer_user_ids = {
        ApplicationIntegrationType.user_install: 202403270010,
        ApplicationIntegrationType.guild_install: 202403270011,
    }
    
    message_interaction = MessageInteraction(
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
    
    _assert_fields_set(message_interaction)
    
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


def test__MessageInteraction__create_empty():
    """
    Tests whether ``MessageInteraction._create_empty`` works as intended.
    """
    message_interaction_id = 202403250011
    
    message_interaction = MessageInteraction._create_empty(message_interaction_id)
    
    _assert_fields_set(message_interaction)
    vampytest.assert_eq(message_interaction.id, message_interaction_id)


def test__MessageInteraction__precreate__no_fields():
    """
    Tests whether ``MessageInteraction.precreate`` works as intended.
    
    Case: no fields given.
    """
    message_interaction_id = 202403250012
    
    message_interaction = MessageInteraction.precreate(message_interaction_id)
    
    _assert_fields_set(message_interaction)
    vampytest.assert_eq(message_interaction.id, message_interaction_id)


def test__MessageInteraction__precreate__all_fields():
    """
    Tests whether ``MessageInteraction.precreate`` works as intended.
    
    Case: all fields given.
    """
    message_interaction_id = 202403250013
    
    interaction_type = InteractionType.application_command
    user = User.precreate(202403250014)
    name = 'Chata'
    sub_command_name_stack = ('Afraid', 'Darkness')
    response_message_id = 20240325006
    interacted_message_id = 202403250057
    target_message_id = 202410060008
    target_user = User.precreate(202410060009)
    triggering_interaction = MessageInteraction.precreate(202403260004, name = 'pain')
    authorizer_user_ids = {
        ApplicationIntegrationType.user_install: 202403270012,
        ApplicationIntegrationType.guild_install: 202403270013,
    }
    
    message_interaction = MessageInteraction.precreate(
        message_interaction_id,
        authorizer_user_ids = authorizer_user_ids,
        interaction_type = interaction_type,
        response_message_id = response_message_id,
        interacted_message_id = interacted_message_id,
        name = name,
        sub_command_name_stack = sub_command_name_stack,
        target_message_id = target_message_id,
        target_user = target_user,
        triggering_interaction = triggering_interaction,
        user = user,
    )
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
