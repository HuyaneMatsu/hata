import vampytest

from ..fields import put_event_type_into
from ..preinstanced import AutoModerationEventType


def test__put_event_type_into():
    """
    Tests whether ``put_event_type_into`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (AutoModerationEventType.message_send, True, {'event_type': AutoModerationEventType.message_send.value}),
    ):
        data = put_event_type_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
