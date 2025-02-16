import vampytest

from ..fields import put_event_type
from ..preinstanced import AutoModerationEventType


def test__put_event_type():
    """
    Tests whether ``put_event_type`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (AutoModerationEventType.message_send, True, {'event_type': AutoModerationEventType.message_send.value}),
    ):
        data = put_event_type(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
