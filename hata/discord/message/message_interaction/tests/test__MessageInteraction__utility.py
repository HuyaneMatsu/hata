import vampytest

from ....interaction import InteractionType
from ....user import User

from ..message_interaction import MessageInteraction

from .test__MessageInteraction__constructor import _assert_fields_set


def test__MessageInteraction__partial():
    """
    Tests whether ``MessageInteraction.partial`` works as intended.
    """
    for message_interaction, expected_value in (
        (MessageInteraction.precreate(202304230029), False),
        (MessageInteraction(), True),
    ):
        vampytest.assert_eq(message_interaction.partial, expected_value)


def test__MessageInteraction__copy():
    """
    Tests whether ``MessageInteraction.copy`` works as intended.
    """
    interaction_type = InteractionType.application_command
    user = User.precreate(202304230030, name = 'Kobayashi')
    sub_command_name_stack = ('Afraid', 'Darkness')
    name = 'Chata'
    
    message_interaction = MessageInteraction(
        interaction_type = interaction_type,
        name = name,
        sub_command_name_stack = sub_command_name_stack,
        user = user,
    )
    
    copy = message_interaction.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, message_interaction)
    vampytest.assert_eq(copy, message_interaction)


def test__MessageInteraction__copy_with__0():
    """
    Tests whether ``MessageInteraction.copy_with`` works as intended.
    
    Case: No fields given.
    """
    interaction_type = InteractionType.application_command
    user = User.precreate(202304230031, name = 'Kobayashi')
    sub_command_name_stack = ('Afraid', 'Darkness')
    name = 'Chata'
    
    message_interaction = MessageInteraction(
        interaction_type = interaction_type,
        name = name,
        sub_command_name_stack = sub_command_name_stack,
        user = user,
    )
    
    copy = message_interaction.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, message_interaction)
    vampytest.assert_eq(copy, message_interaction)


def test__MessageInteraction__copy_with__1():
    """
    Tests whether ``MessageInteraction.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_interaction_type = InteractionType.application_command
    old_user = User.precreate(202304230032, name = 'Kobayashi')
    old_sub_command_name_stack = ('Afraid', 'Darkness')
    old_name = 'Chata'
    
    new_interaction_type = InteractionType.application_command
    new_user = User.precreate(202304230033, name = 'Tohru')
    new_sub_command_name_stack = ('Dragon', 'Maid')
    new_name = 'Suika'
    
    message_interaction = MessageInteraction(
        interaction_type = old_interaction_type,
        name = old_name,
        sub_command_name_stack = old_sub_command_name_stack,
        user = old_user,
    )
    
    copy = message_interaction.copy_with(
        interaction_type = new_interaction_type,
        name = new_name,
        sub_command_name_stack = new_sub_command_name_stack,
        user = new_user,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, message_interaction)
    
    vampytest.assert_eq(copy.sub_command_name_stack, new_sub_command_name_stack)
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_is(copy.type, new_interaction_type)
    vampytest.assert_eq(copy.user, new_user)


def test__MessageInteraction__joined_name():
    """
    Tests whether ``MessageInteraction.joined_name`` works as intended.
    """
    for input_name, input_sub_command_name_stack, expected_output in (
        ('Kobayashi', None, 'Kobayashi'),
        ('Kobayashi', ('to',), 'Kobayashi to'),
        ('Kobayashi', ('to', 'Tohru',), 'Kobayashi to Tohru'),
    ):
        message_interaction = MessageInteraction(
            name = input_name,
            sub_command_name_stack = input_sub_command_name_stack,
        )
        
        output = message_interaction.joined_name
        vampytest.assert_instance(output, str)
        vampytest.assert_eq(output, expected_output)
