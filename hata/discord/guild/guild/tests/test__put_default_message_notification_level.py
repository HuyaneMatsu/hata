import vampytest

from ..fields import put_default_message_notification_level
from ..preinstanced import MessageNotificationLevel


def _iter_options():
    yield (
        MessageNotificationLevel.none,
        False,
        {'default_message_notifications': MessageNotificationLevel.none.value},
    )
    yield (
        MessageNotificationLevel.none,
        True,
        {'default_message_notifications': MessageNotificationLevel.none.value},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_default_message_notification_level(input_value, defaults):
    """
    Tests whether ``put_default_message_notification_level`` works as intended.
    
    Parameters
    ----------
    input_value : ``MessageNotificationLevel``
        Value to serialize.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_default_message_notification_level(input_value, {}, defaults)
