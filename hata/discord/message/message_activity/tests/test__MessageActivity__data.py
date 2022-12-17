import vampytest

from ..message_activity import MessageActivity
from ..preinstanced import MessageActivityType

from .test__MessageActivity__constructor import _check_is_all_attribute_set


def test__MessageActivity__from_data():
    """
    Tests whether ``MessageActivity.from_data`` works as intended.
    """
    message_activity_type = MessageActivityType.join
    party_id = 'Nue'
    
    data = {
        'type': message_activity_type.value,
        'party_id': party_id,
    }
    
    message_activity = MessageActivity.from_data(data)
    _check_is_all_attribute_set(message_activity)

    vampytest.assert_eq(message_activity.party_id, party_id)
    vampytest.assert_is(message_activity.type, message_activity_type)


def test__MessageActivity__to_data():
    """
    Tests whether ``MessageActivity.to_data`` works as intended.
    
    Case: include defaults.
    """
    message_activity_type = MessageActivityType.join
    party_id = 'Nue'
    
    message_activity = MessageActivity(
        message_activity_type = message_activity_type,
        party_id = party_id,
    )
    
    vampytest.assert_eq(
        message_activity.to_data(
            defaults = True,
        ),
        {
            'type': message_activity_type.value,
            'party_id': party_id,
        },
    )
