import vampytest

from ...interaction import InteractionType
from ...user import ZEROUSER

from .. import MessageInteraction

def get_data():
    return {
        'name': 'name',
        'id': '2',
        'user': ZEROUSER.to_data(),
        'type': InteractionType.application_command.value,
    }


def test__MessageInteraction__from_data():
    """
    Tests whether ``MessageInteraction``'s `from_data` method works as expected.
    """
    message_interaction = MessageInteraction(get_data(), 0)
    
    vampytest.assert_instance(hash(message_interaction), int)


def test__MessageInteraction__repr():
    """
    Tests whether ``MessageInteraction``'s `__repr__` method works as expected.
    """
    message_interaction = MessageInteraction(get_data(), 0)
    
    vampytest.assert_instance(repr(message_interaction), str)
