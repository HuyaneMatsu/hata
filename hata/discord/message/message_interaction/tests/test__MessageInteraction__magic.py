import vampytest

from ....interaction import InteractionType
from ....user import User

from ..message_interaction import MessageInteraction


def test__MessageInteraction__repr():
    """
    tests whether ``MessageInteraction.__repr__`` works as intended.
    """
    message_interaction_id = 202304230021
    
    interaction_type = InteractionType.application_command
    user = User.precreate(202304230022, name = 'Kobayashi')
    sub_command_name_stack = ('Afraid', 'Darkness')
    name = 'Chata'
    
    message_interaction = MessageInteraction.precreate(
        message_interaction_id,
        interaction_type = interaction_type,
        name = name,
        sub_command_name_stack = sub_command_name_stack,
        user = user,
    )
    
    vampytest.assert_instance(repr(message_interaction), str)


def test__MessageInteraction__hash():
    """
    tests whether ``MessageInteraction.__hash__`` works as intended.
    """
    message_interaction_id = 202304230023
    
    interaction_type = InteractionType.application_command
    user = User.precreate(202304230024, name = 'Kobayashi')
    sub_command_name_stack = ('Afraid', 'Darkness')
    name = 'Chata'
    
    message_interaction = MessageInteraction.precreate(
        message_interaction_id,
        interaction_type = interaction_type,
        name = name,
        sub_command_name_stack = sub_command_name_stack,
        user = user,
    )
    
    vampytest.assert_instance(hash(message_interaction), int)


def test__MessageInteraction__eq():
    """
    Tests whether ``MessageInteraction.__eq__`` works as intended.
    """
    message_interaction_id_1 = 202304230025
    message_interaction_id_2 = 202304230026
    
    interaction_type = InteractionType.application_command
    user = User.precreate(202304230027, name = 'Kobayashi')
    sub_command_name_stack = ('Afraid', 'Darkness')
    name = 'Chata'
    
    keyword_parameters = {
        'message_interaction_id': message_interaction_id_1,
        'interaction_type': interaction_type,
        'name': name,
        'sub_command_name_stack': sub_command_name_stack,
        'user': user,
    }
    
    message_interaction = MessageInteraction.precreate(**keyword_parameters)
    vampytest.assert_eq(message_interaction, message_interaction)
    vampytest.assert_ne(message_interaction, object())
    
    for field_name, field_value in (
        ('message_interaction_id', message_interaction_id_2),
        ('name', 'Slayer'),
        ('interaction_type', InteractionType.form_submit),
        ('sub_command_name_stack', None),
        ('user', User.precreate(202304230028, name = 'Kanna')),
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
