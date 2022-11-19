import vampytest

from ..fields import parse_event_type
from ..preinstanced import AutoModerationEventType


def test__parse_event_type():
    """
    Tests whether `parse_event_type` works as intended.
    """
    for input_value, expected_output in (
        ({}, AutoModerationEventType.none),
        ({'event_type': AutoModerationEventType.message_send.value}, AutoModerationEventType.message_send),
    ):
        output = parse_event_type(input_value)
        vampytest.assert_eq(output, expected_output)
