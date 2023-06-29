import vampytest

from ..fields import put_message_notification_into
from ..preinstanced import MessageNotificationLevel


def test__put_message_notification_into():
    """
    Tests whether ``put_message_notification_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (
            MessageNotificationLevel.none,
            False,
            {'default_message_notifications': MessageNotificationLevel.none.value},
        ),
    ):
        data = put_message_notification_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
