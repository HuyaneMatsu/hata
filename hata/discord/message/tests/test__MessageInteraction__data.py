import vampytest

from ...interaction import InteractionType
from ...user import ZEROUSER, User

from .. import MessageInteraction


def test__MessageInteraction__from_data__0():
    """
    Tests whether ``MessageInteraction``'s `from_data` method works as expected.
    This test tests default case.
    """
    data = {
        'name': 'name',
        'id': '2',
        'user': ZEROUSER.to_data(),
        'type': InteractionType.application_command.value,
    }
    
    message_interaction = MessageInteraction(data, 0)
    
    vampytest.assert_eq(message_interaction.name, 'name')
    vampytest.assert_eq(message_interaction.id, 2)
    vampytest.assert_is(message_interaction.user, ZEROUSER)
    vampytest.assert_is(message_interaction.type, InteractionType.application_command)
    vampytest.assert_eq(message_interaction.sub_command_name_stack, None)


def test__MessageInteraction__from_data__1():
    """
    Tests whether ``MessageInteraction``'s `from_data` method works as expected.
    This test tests missing fields.
    """
    data = {
        'id': '2',
        'user': ZEROUSER.to_data(),
        'type': InteractionType.application_command.value,
    }
    
    message_interaction = MessageInteraction(data, 0)
    
    vampytest.assert_eq(message_interaction.name, '')


def test__MessageInteraction__from_data__2():
    """
    Tests whether ``MessageInteraction``'s `from_data` method works as expected.
    This test tests stuffed fields.
    """
    user = User.precreate(44)
    
    data = {
        'name': 'test sub command',
        'id': '2',
        'user': user.to_data(),
        'member': {},
        'type': InteractionType.application_command.value,
    }
    
    message_interaction = MessageInteraction(data, 0)
    
    vampytest.assert_eq(message_interaction.name, 'test')
    vampytest.assert_eq(message_interaction.sub_command_name_stack, ('sub', 'command'))
    vampytest.assert_is(message_interaction.user, user)
