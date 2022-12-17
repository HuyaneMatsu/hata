import vampytest

from ..message_activity import MessageActivity
from ..preinstanced import MessageActivityType

from .test__MessageActivity__constructor import _check_is_all_attribute_set


def test__MessageActivity__copy():
    """
    Tests whether ``MessageActivity.copy`` works as intended.
    """
    message_activity_type = MessageActivityType.join
    party_id = 'Nue'
    
    message_activity = MessageActivity(
        message_activity_type = message_activity_type,
        party_id = party_id,
    )
    copy = message_activity.copy()
    
    _check_is_all_attribute_set(copy)
    vampytest.assert_is_not(message_activity, copy)
    
    vampytest.assert_eq(message_activity, copy)


def test__MessageActivity__copy_with__0():
    """
    Tests whether ``MessageActivity.copy_with`` works as intended.
    
    Case: no fields given.
    """
    message_activity_type = MessageActivityType.join
    party_id = 'Nue'
    
    message_activity = MessageActivity(
        message_activity_type = message_activity_type,
        party_id = party_id,
    )
    copy = message_activity.copy_with()
    
    _check_is_all_attribute_set(copy)
    vampytest.assert_is_not(message_activity, copy)
    
    vampytest.assert_eq(message_activity, copy)


def test__MessageActivity__copy_with__1():
    """
    Tests whether ``MessageActivity.copy_with`` works as intended.
    
    Case: all no fields given.
    """
    old_message_activity_type = MessageActivityType.join
    new_message_activity_type = MessageActivityType.listen
    old_party_id = 'Nue'
    new_party_id = 'Remilia'
    
    message_activity = MessageActivity(
        message_activity_type = old_message_activity_type,
        party_id = old_party_id,
    )
    copy = message_activity.copy_with(
        message_activity_type = new_message_activity_type,
        party_id = new_party_id,
    )
    
    _check_is_all_attribute_set(copy)
    vampytest.assert_is_not(message_activity, copy)
    
    vampytest.assert_eq(copy.party_id, new_party_id)
    vampytest.assert_is(copy.type, new_message_activity_type)
