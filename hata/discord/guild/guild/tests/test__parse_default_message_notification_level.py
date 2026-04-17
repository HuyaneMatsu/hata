import vampytest

from ..fields import parse_default_message_notification_level
from ..preinstanced import MessageNotificationLevel


def _iter_options():
    yield {}, MessageNotificationLevel.all_messages
    yield {'default_message_notifications': MessageNotificationLevel.none.value}, MessageNotificationLevel.none


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_default_message_notification_level(input_data):
    """
    Tests whether ``parse_default_message_notification_level`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``MessageNotificationLevel``
    """
    output = parse_default_message_notification_level(input_data)
    vampytest.assert_instance(output, MessageNotificationLevel)
    return output
