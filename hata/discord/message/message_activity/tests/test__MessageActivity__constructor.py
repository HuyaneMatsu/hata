import vampytest

from ..message_activity import MessageActivity
from ..preinstanced import MessageActivityType


def _check_is_all_attribute_set(message_activity):
    """
    Tests whether all attributes are set of the given message activity.
    
    Parameters
    ----------
    message_activity : ``MessageActivity``
        The message activity to check.
    """
    vampytest.assert_instance(message_activity, MessageActivity)
    vampytest.assert_instance(message_activity.party_id, str, nullable = True)
    vampytest.assert_instance(message_activity.type, MessageActivityType)


def test__MessageActivity__new__0():
    """
    Tests whether ``MessageActivity.__new__`` works as intended.
    
    Case: No fields given.
    """
    message_activity = MessageActivity()
    _check_is_all_attribute_set(message_activity)


def test__MessageActivity__new__1():
    """
    Tests whether ``MessageActivity.__new__`` works as intended.
    
    Case: All fields given.
    """
    message_activity_type = MessageActivityType.join
    party_id = 'Nue'

    message_activity = MessageActivity(
        message_activity_type = message_activity_type,
        party_id = party_id,
    )
    _check_is_all_attribute_set(message_activity)
    
    vampytest.assert_eq(message_activity.party_id, party_id)
    vampytest.assert_is(message_activity.type, message_activity_type)
