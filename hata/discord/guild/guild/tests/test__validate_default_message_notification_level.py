import vampytest

from ..fields import validate_default_message_notification_level
from ..preinstanced import MessageNotificationLevel

def _iter_options__passing():
    yield None, MessageNotificationLevel.all_messages
    yield MessageNotificationLevel.none, MessageNotificationLevel.none
    yield MessageNotificationLevel.none.value, MessageNotificationLevel.none


def _iter_options__type_error():
    yield 12.6
    yield ''


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_default_message_notification_level(input_value):
    """
    Tests whether `validate_default_message_notification_level` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : ``MessageNotificationLevel``
    
    Raises
    ------
    TypeError
    """
    output = validate_default_message_notification_level(input_value)
    vampytest.assert_instance(output, MessageNotificationLevel)
    return output
