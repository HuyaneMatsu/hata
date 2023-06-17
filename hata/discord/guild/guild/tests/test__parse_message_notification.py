import vampytest

from ..fields import parse_message_notification
from ..preinstanced import MessageNotificationLevel


def test__parse_message_notification():
    """
    Tests whether ``parse_message_notification`` works as intended.
    """
    for input_data, expected_output in (
        ({}, MessageNotificationLevel.all_messages),
        ({'default_message_notifications': MessageNotificationLevel.null.value}, MessageNotificationLevel.null),
    ):
        output = parse_message_notification(input_data)
        vampytest.assert_eq(output, expected_output)
