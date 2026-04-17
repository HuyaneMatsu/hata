import vampytest

from ..message_activity import MessageActivity
from ..preinstanced import MessageActivityType


def test__MessageActivity__repr():
    """
    Tests whether ``MessageActivity.__repr__`` works as intended.
    """
    message_activity_type = MessageActivityType.join
    party_id = 'Nue'
    
    message_activity = MessageActivity(
        message_activity_type = message_activity_type,
        party_id = party_id,
    )
    
    vampytest.assert_instance(repr(message_activity), str)


def test__MessageActivity__hash():
    """
    Tests whether ``MessageActivity.__hash__`` works as intended.
    """
    message_activity_type = MessageActivityType.join
    party_id = 'Nue'
    
    message_activity = MessageActivity(
        message_activity_type = message_activity_type,
        party_id = party_id,
    )
    
    vampytest.assert_instance(hash(message_activity), int)


def test__MessageActivity__eq():
    """
    Tests whether ``MessageActivity.__eq__`` works as intended.
    """
    message_activity_type = MessageActivityType.join
    party_id = 'Nue'
    
    keyword_parameters = {
        'message_activity_type': message_activity_type,
        'party_id': party_id,
    }
    
    message_activity = MessageActivity(**keyword_parameters)
    
    vampytest.assert_eq(message_activity, message_activity)
    vampytest.assert_ne(message_activity, object())
    
    for field_name, field_value in (
        ('message_activity_type', MessageActivityType.listen),
        ('party_id', 'Remilia'),
    ):
        test_message_activity = MessageActivity(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(message_activity, test_message_activity)
