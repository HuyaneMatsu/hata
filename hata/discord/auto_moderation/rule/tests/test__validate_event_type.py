import vampytest

from ..fields import validate_event_type
from ..preinstanced import AutoModerationEventType


def test__validate_event_type():
    """
    Tests whether ``validate_event_type`` is working as intended.
    """
    for input_value, expected_output in (
        (AutoModerationEventType.message_send, AutoModerationEventType.message_send.value),
        (AutoModerationEventType.message_send.value, AutoModerationEventType.message_send.value),
    ):
        output = validate_event_type(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_event_type__1():
    """
    Tests whether `validate_event_type` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_event_type(input_value)
