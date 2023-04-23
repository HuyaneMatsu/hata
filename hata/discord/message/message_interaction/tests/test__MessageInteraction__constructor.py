import vampytest

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
    
    vampytest.assert_instance(message_interaction.id, int)
    vampytest.assert_instance(message_interaction.name, str)
    vampytest.assert_instance(message_interaction.sub_command_name_stack, tuple, nullable = True)
    vampytest.assert_instance(message_interaction.type, InteractionType)
    vampytest.assert_instance(message_interaction.user, ClientUserBase)


def test__MessageInteraction__new__0():
    """
    Tests whether ``MessageInteraction.__new__`` works as intended.
    
    Case: no parameters.
    """
    message_interaction = MessageInteraction()
    _assert_fields_set(message_interaction)


def test__MessageInteraction__new__1():
    """
    Tests whether ``MessageInteraction.__new__`` works as intended.
    
    Case: all fields given.
    """
    interaction_type = InteractionType.application_command
    user = User.precreate(202304230010, name = 'Kobayashi')
    sub_command_name_stack = ('Afraid', 'Darkness')
    name = 'Chata'
    
    message_interaction = MessageInteraction(
        interaction_type = interaction_type,
        name = name,
        sub_command_name_stack = sub_command_name_stack,
        user = user,
    )
    
    _assert_fields_set(message_interaction)
    
    vampytest.assert_eq(message_interaction.name, name)
    vampytest.assert_eq(message_interaction.sub_command_name_stack, sub_command_name_stack)
    vampytest.assert_is(message_interaction.type, interaction_type)
    vampytest.assert_eq(message_interaction.user, user)


def test__MessageInteraction__create_empty():
    """
    Tests whether ``MessageInteraction._create_empty`` works as intended.
    """
    message_interaction_id = 202304230011
    
    message_interaction = MessageInteraction._create_empty(message_interaction_id)
    
    _assert_fields_set(message_interaction)
    vampytest.assert_eq(message_interaction.id, message_interaction_id)


def test__MessageInteraction__precreate__0():
    """
    Tests whether ``MessageInteraction.precreate`` works as intended.
    
    Case: no fields given.
    """
    message_interaction_id = 202304230012
    
    message_interaction = MessageInteraction.precreate(message_interaction_id)
    
    _assert_fields_set(message_interaction)
    vampytest.assert_eq(message_interaction.id, message_interaction_id)


def test__MessageInteraction__precreate__1():
    """
    Tests whether ``MessageInteraction.precreate`` works as intended.
    
    Case: all fields given.
    """
    message_interaction_id = 202304230013
    
    interaction_type = InteractionType.application_command
    user = User.precreate(202304230014, name = 'Kobayashi')
    sub_command_name_stack = ('Afraid', 'Darkness')
    name = 'Chata'
    
    message_interaction = MessageInteraction.precreate(
        message_interaction_id,
        interaction_type = interaction_type,
        name = name,
        sub_command_name_stack = sub_command_name_stack,
        user = user,
    )
    _assert_fields_set(message_interaction)
    vampytest.assert_eq(message_interaction.id, message_interaction_id)
    
    vampytest.assert_eq(message_interaction.name, name)
    vampytest.assert_eq(message_interaction.sub_command_name_stack, sub_command_name_stack)
    vampytest.assert_is(message_interaction.type, interaction_type)
    vampytest.assert_eq(message_interaction.user, user)
